# Mock function to simulate generate_task_details response
def generate_mock_task_details(task_title):
    # Simulate an error if the task title is "error"
    if task_title.lower() == "error":
        return {"error": "Mocked error: Task title cannot be 'error'."}
    # Otherwise, return a mocked detailed task scope
    else:
        return {"details": f"Mocked details for task '{task_title}'. This includes descriptions, acceptance criteria, etc."}

# Mock function to simulate create_jira_issue response
def create_mock_jira_issue(task_details):
    # Simply return a success message with mocked issue key
    return "Mocked success: Jira issue created successfully! Issue key: MOCK-123"