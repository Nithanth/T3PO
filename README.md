# Project Task Manager Droid

This Streamlit app takes in an engineering task title and publishes a scoped Jira ticket to match it.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/Nithanth/factory_ai_droid.git
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Configuration

1. Fetch the following credentials:
   - OpenAI API key (found on OpenAI's platform under your account)
   - Jira API key
   - Jira username
   - The base URL for your Jira server instance
   - The key of the project you want to publish a ticket for (found on your Jira account)

## Usage

1. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

2. In the UI, fill in your Jira URL, username, and project key where prompted to.

3. Input the task title where prompted to and click "Generate Ticket".

4. The generated ticket should now be displayed on the screen. Click "Generate Jira Ticket" to publish the ticket to your specified Jira project.

5. If any errors occur, follow the suggested resolution displayed.

6. To exit the program, press `Ctrl+C` or close the UI window.