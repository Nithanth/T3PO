import streamlit as st
from ticket_generator import generate_task_details, evaluate_task_scope, set_up_openai_client, is_valid_task_title
from utils import *
from jira_integration import create_jira_issue, format_description, set_up_jira_client
import json

def main():
    st.title("T3PO: The Task Manager Droid You Are Looking For")

    # Sidebar for JIRA configuration
    st.sidebar.title("JIRA Configuration")
    if 'jira_url' not in st.session_state:
        st.session_state.jira_url = "https://your-domain.atlassian.net"
    if 'jira_user' not in st.session_state:
        st.session_state.jira_user = "your-email@example.com"
    if 'jira_project_key' not in st.session_state:
        st.session_state.jira_project_key = "PROJ-123"

    jira_url = st.sidebar.text_input("JIRA URL", value=st.session_state.jira_url)
    jira_user = st.sidebar.text_input("JIRA Username", value=st.session_state.jira_user)
    jira_project_key = st.sidebar.text_input("JIRA Project Key", value=st.session_state.jira_project_key)

    # Update session state when user changes input
    st.session_state.jira_url = jira_url
    st.session_state.jira_user = jira_user
    st.session_state.jira_project_key = jira_project_key

    # Input field for the task title
    task_title = st.text_input("Task Ticket Generator", "Enter the title of the task you want to generate a ticket for here: Ex. 'Create evaluation module for MNIST classifier'")

    # Instantiate clients
    openai_client = set_up_openai_client()
    jira_client = set_up_jira_client(jira_url, jira_user)

    # Button to generate task details
    if st.button("Generate Ticket"):
        if task_title and is_valid_task_title(task_title):
            response = generate_task_details(openai_client, task_title)
            if "error" in response:
                st.error(response["error"])
                return

            response_with_quality = evaluate_task_scope(openai_client, task_title, response["details"])
            if "error" in response_with_quality:
                st.error(response_with_quality["error"])
                return

            if response_with_quality["Scope Quality"] == "Poorly-scoped":
                st.error("The generated task details are not well-scoped. Please try again.")
                return

            st.session_state.task_details_structured = response_with_quality
            formatted_description = format_description(response_with_quality)
            st.session_state.task_details_formatted = formatted_description

            st.subheader("Generated Task Details")
            st.write(formatted_description)
        else:
            st.error("Please enter a valid task title.")

    if st.button("Create Jira Ticket"):
        if 'task_details_structured' in st.session_state and st.session_state.task_details_structured:
            try:
                message = create_jira_issue(jira_client, st.session_state.task_details_structured, jira_user, jira_project_key)
                st.success(message)
            except Exception as e:
                st.error(f"Failed to create Jira ticket due to: {str(e)}")
                st.error(type(st.session_state.task_details_structured))
                st.error(st.session_state.task_details_structured)
        else:
            st.error("Please generate task details before creating a Jira ticket.")

if __name__ == "__main__":
    main()
