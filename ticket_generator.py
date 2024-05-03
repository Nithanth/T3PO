import openai
from vault import OPENAI_API_KEY
from utils import *
import json

def set_up_openai_client():
    """ Instantiates an OpenAI client with the API key stored in the vault module. """
    return openai.OpenAI(api_key=OPENAI_API_KEY)

def generate_task_details(client,task_title):
    """Generates detailed task scope from a given task title using an LLM."""

    # Validate the task title again to ensure it's likely relevant to engineering tasks - sanity check
    if not is_valid_task_title(task_title):
        return {
            "error": "The provided task title does not seem to be relevant to engineering tasks."
        }

    # Construct the prompt for the Language Model
    prompt = f"""
    Given an engineering task title, expand it into a detailed task scope including descriptions, 
    acceptance criteria/testing, sub-tasks, assumptions, dependencies, resources needed, estimated effort, 
    potential risks/challenges, points for the task, and recommended number of engineers. Ensure 
    the scope is comprehensive and ready for implementation.

    Task Title: {task_title}
    Detailed Scope:
    <Split by each appropriate section>

    Here are some examples of the output followed by the quality of the scope:
    # Example 1:
    Task Title: Implement OAuth2 Authentication in Service
    Detailed Scope:
    - Description: Implement OAuth2 to secure the REST API by authenticating users and services.
    - Acceptance Criteria: API must reject calls without valid authentication tokens; OAuth2 flow must be implemented according to RFC 6749.
    - Sub-Tasks: 1. Set up OAuth2 framework; 2. Integrate with user database for credentials verification; 3. Implement token generation and expiration logic; 4. Write unit and integration tests.
    - Assumptions: User database supports OAuth integrations and has necessary schema for OAuth2.
    - Dependencies: OAuth2 library (e.g., OAuthLib), User database.
    - Resources Needed: Access to development and testing environments, OAuth2 library licenses.
    - Estimated Effort: 2 weeks for a team of 2 engineers.
    - Potential Risks/Challenges: Delays in third-party library integration, potential security vulnerabilities in token handling.
    - Points for the Task: 8 points.
    - Recommended Number of Engineers: 2
    Scope Quality: Well-scoped.

    # Example 2:
    Task Title: Update UI Colors
    Detailed Scope:
    - Description: Update the user interface colors to match the new brand guidelines.
    - Acceptance Criteria: All primary and secondary colors should be updated across all pages, consistent with the new brand palette.
    - Sub-Tasks: 1. Identify all CSS files and UI components affected; 2. Replace color values; 3. Conduct cross-browser testing.
    - Assumptions: Brand guidelines are finalized and approved.
    - Dependencies: Access to UI codebase and brand guideline documents.
    - Resources Needed: UI/UX designer, front-end developer.
    - Estimated Effort: 1 week for a team of 1 designer and 1 developer.
    - Potential Risks/Challenges: Possible inconsistencies in color perception across different displays.
    - Points for the Task: 3 points.
    - Recommended Number of Engineers: 2
    Scope Quality: Well-scoped.

    # Example 3:
    Task Title: Update UI
    Detailed Scope:
    - Description: Make the UI better.
    Scope Quality: Poorly-scoped.

    IMPORTANT: IF THE TASK_TITLE DOESN'T MAKE SENSE AS AN APPROPRIATE ENGINEERING TASK MAKE SURE 'Poorly-scoped' IS THE SCOPE QUALITY AND 
    THE DETAILED SCOPE JUST SAYS: 'ERROR - NOT APPROPRIATE TASK'! Example of bad task titles: 'Update UI', 'Task 1234', 'Create a new feature', 
    'Hello World', 'Hi how are you?'. 'qwertyuiopasdfghjklzxcvbnm' 'blah blah blah'. Make sure to catch these bad titles and errors that get 
    passed in, don't resort to using one of th eexamples from above I want to catch the error and return the appropriate error message.

    # To Generate:
    Task Title: {task_title}
    Detailed Scope:
    <Split by each appropriate section>
    
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo", 
            response_format={ "type": "json_object" },
            messages=[
            {"role": "system", "content": f"""You are a scrum master/project manager of a software development team with many important stakeholders. 
             Your job is to help the team prioritize and plan their work. You will be given a query which represents the title of an engineering task. 
             Your task is to use this information to create a detailed task scope for each task, including a description, acceptance criteria, sub-tasks, 
             assumptions, dependencies, resources needed, estimated effort, potential risks/challenges, points for the task, and recommended number of 
             engineers. Ensure the scope is comprehensive and ready for implementation. Do not include any additional information or explanations. 
             Respond with a JSON object containing the task title and the generated task scope in the format listed in the prompt query which follows
             in the conversation."""},
            {"role": "user", "content": prompt}
  ]
        )

        return {"details": response.choices[0].message.content}

    except Exception as e:
        return {"error": f"Failed to generate task details due to: {str(e)}"}


def is_valid_task_title(task_title):
    """Checks if a task title is likely valid and relevant to engineering tasks."""
    # duct tape error handling for now
    return len(task_title) > 8

def evaluate_task_scope(client, task_title, generated_scope):
    evaluation_prompt = f"""
    Evaluate the following ticket/issue based on content quality and scope. Here are some examples of the output followed by the quality of the scope:
    # Example 1:
    Task Title: Implement OAuth2 Authentication in Service
    Detailed Scope:
    - Description: Implement OAuth2 to secure the REST API by authenticating users and services.
    - Acceptance Criteria: API must reject calls without valid authentication tokens; OAuth2 flow must be implemented according to RFC 6749.
    - Sub-Tasks: 1. Set up OAuth2 framework; 2. Integrate with user database for credentials verification; 3. Implement token generation and expiration logic; 4. Write unit and integration tests.
    - Assumptions: User database supports OAuth integrations and has necessary schema for OAuth2.
    - Dependencies: OAuth2 library (e.g., OAuthLib), User database.
    - Resources Needed: Access to development and testing environments, OAuth2 library licenses.
    - Estimated Effort: 2 weeks for a team of 2 engineers.
    - Potential Risks/Challenges: Delays in third-party library integration, potential security vulnerabilities in token handling.
    - Points for the Task: 8 points.
    - Recommended Number of Engineers: 2
    Scope Quality: Well-scoped.

    # Example 2:
    Task Title: Update UI Colors
    Detailed Scope:
    - Description: Update the user interface colors to match the new brand guidelines.
    - Acceptance Criteria: All primary and secondary colors should be updated across all pages, consistent with the new brand palette.
    - Sub-Tasks: 1. Identify all CSS files and UI components affected; 2. Replace color values; 3. Conduct cross-browser testing.
    - Assumptions: Brand guidelines are finalized and approved.
    - Dependencies: Access to UI codebase and brand guideline documents.
    - Resources Needed: UI/UX designer, front-end developer.
    - Estimated Effort: 1 week for a team of 1 designer and 1 developer.
    - Potential Risks/Challenges: Possible inconsistencies in color perception across different displays.
    - Points for the Task: 3 points.
    - Recommended Number of Engineers: 2
    Scope Quality: Well-scoped.

    # Example 3:
    Task Title: Update UI
    Detailed Scope:
    - Description: Make the UI better.
    Scope Quality: Poorly-scoped.

    THIS IS THE MOST IMPORTANT PART OF THE PROMPT: IF THE TASK TITLE DOESN'T MAKE SENSE AS AN APPROPRIATEENGINEERING TASK MAKE SURE 'Poorly-scoped' IS THE SCOPE QUALITY!
    BAD TASK EXAMPLES: 'Update UI', 'Task 1234', 'Create a new feature', 'Hello World', 'Hi how are you?'. 'qwertyuiopasdfghjklzxcvbnm'
    # Evaluating the task scope - always finish your response with:
    Task Title: {task_title}
    Detailed Scope: {generated_scope}
    Scope Quality: <this always needs to be either 'Well-scoped' or 'Poorly-scoped'>
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",  
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content": f"""You are a scrum master/project manager of a software development team with many important stakeholders. 
                Your job is to help the team prioritize and plan their work. You will be given a scoped ticket including a description, acceptance criteria, sub-tasks, 
                assumptions, dependencies, resources needed, estimated effort, potential risks/challenges, points for the task, and recommended number of 
                engineers. Ensure the scope is comprehensive and ready for implementation. Do not include any additional information or explanations. 
                Respond with a JSON object containing the task title and the generated task scope and the scope quality in the format listed in the prompt query which follows
                in the conversation."""},
                {"role": "user", "content": evaluation_prompt}
            ]
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        return {"error": f"Failed to generate task details due to: {str(e)}"}

def main():
    client = set_up_openai_client()
    response = generate_task_details(client, "Write evaluation module for MNIST classifier")
    print("Generate Task Details Response:", response)

    if "details" in response:
        quality_response = evaluate_task_scope(client, "Write evaluation module for MNIST classifier", response["details"])
        print("Raw Quality Response:", quality_response)
    else:
        print("Failed to generate task details.")

if __name__ == "__main__":
   main()

