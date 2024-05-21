from jira import JIRA
import os
import vault

# set JIRA credentials from vault

JIRA_API_TOKEN = vault.JIRA_API_TOKEN

def set_up_jira_client(jira_url, jira_user):
    """ Instantiates an JIRA client with the API key stored in the vault module. """
    jira_options = {'server': jira_url}
    jira_client = JIRA(options=jira_options, basic_auth=(jira_user, JIRA_API_TOKEN))
    # print("Connected to Jira server")
    return jira_client

def create_jira_issue(jira_client, task_details, jira_user, jira_project_key):
    """
    Creates a Jira issue using the detailed task scope.

    Parameters:
    - task_details (dict): The task details, structured appropriately.

    Returns:
    - A string message indicating the result of the issue creation attempt.
    """
    try:
        issue_dict = {
            'project': {'key': jira_project_key},
            'summary': task_details["Task Title"],
            'description': format_description(task_details),
            'issuetype': {'name': 'Task'},
            'assignee': {'name': jira_user},
        }
        new_issue = jira_client.create_issue(fields=issue_dict)
        return f"Successfully created Jira issue: {new_issue.key}"
    except Exception as e:
        return f"Failed to create Jira issue due to: {str(e)}"

def format_description(task_details):
    """
    Formats the task details into a string suitable for the Jira issue description.

    Parameters:
    - task_details: The structured task details.

    Returns:
    - A formatted string for the description field in the Jira issue.
    """
    description = ""
    for key, value in task_details["Detailed Scope"].items():
        description += f"*{key}*: "
        if isinstance(value, list):  
            if key == "Sub-Tasks":  
                description += "\n"  
                for subtask in value:  
                    description += f"{subtask}\n"
            else: 
                description += "\n"  
                for item in value:
                    description += f"- {item}\n"
        else:
            description += f"{value}\n" 
        description += "\n"  
    return description

if __name__ == "__main__":
    # Initialize JIRA client with options and authentication
    jira_user = "your-jira-username"
    jira_project_key = "your-jira-project-key"  
    jira_url = "your-jira-url"
    
    jira_client = set_up_jira_client(jira_url, jira_user)
    raw_quality_response = {
    "Task Title": "Write evaluation module for MNIST classifier",
    "Detailed Scope": {
        "Description": "Develop an evaluation module for an MNIST classifier to assess the model's performance using metrics such as accuracy, precision, recall, and F1-score.",
            "Acceptance Criteria": [
            "The module correctly calculates and reports accuracy, precision, recall, and F1-score.",
            "Integration with the existing MNIST classifier is seamless and does not disrupt current functionalities.",
            "Performance metrics are logged and can be exported for further analysis."
        ],
        "Sub-Tasks": [
            "1. Define metrics calculation functions.",
            "2. Integrate the evaluation module with the existing MNIST classifier.",
            "3. Design and implement a logging system for the evaluation results.",
            "4. Develop unit tests for each metric calculation to ensure accuracy.",
            "5. Conduct integration testing to validate module with the classifier."
        ],
        "Assumptions": "The MNIST classifier is already developed and functioning correctly.",
            "Dependencies": [
            "Python environment",
            "Access to the existing MNIST classifier codebase",
            "Libraries such as NumPy, Pandas, matplotlib for data manipulation and visualization"
        ],
        "Resources Needed": [
            "Development environment setup with Python and necessary libraries",
            "Access to the code repository and documentation of the existing classifier"
        ],
        "Estimated Effort": "3 weeks for a team of 2 engineers.",
        "Potential Risks/Challenges": [
            "Potential discrepancies in metric calculations due to errors in integration.",
            "Delays in development due to unforeseen complexity in accessing and manipulating the classifier outputs."
        ],
        "Points for the Task": "8 points",
        "Recommended Number of Engineers": "2"
        },
    "Scope Quality": "Well-scoped"
    }
    response = create_jira_issue(jira_client, raw_quality_response, jira_project_key)
    print(response)
