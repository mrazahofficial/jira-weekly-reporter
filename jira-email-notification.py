import os
import requests
import base64
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
from dotenv import load_dotenv

# Load configuration
load_dotenv()

JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_TOKEN = os.getenv("JIRA_TOKEN")
JIRA_URL = os.getenv("JIRA_URL")
GMAIL_PASS = os.getenv("GMAIL_PASS")
PROJECT_KEY = "KAN"  # Example Project


def get_issues(jql):
    """Fetches issues and generates clickable links."""
    auth = base64.b64encode(f"{JIRA_EMAIL}:{JIRA_TOKEN}".encode()).decode()
    headers = {"Authorization": f"Basic {auth}", "Accept": "application/json", "Content-Type": "application/json"}
    url = f"{JIRA_URL}/rest/api/3/search/jql"
    payload = {"jql": jql, "maxResults": 50, "fields": ["summary", "key"]}

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        issues = response.json().get("issues", [])

        # Format list with links for the report
        issue_list = ""
        for issue in issues:
            link = f"{JIRA_URL}/browse/{issue['key']}"
            issue_list += f"- {issue['key']}: {issue['fields']['summary']} ({link})\n"
        return len(issues), issue_list
    except Exception as e:
        print(f"Error fetching Jira data: {e}")
        return 0, "Error retrieving list.\n"


def main():
    if not all([JIRA_EMAIL, JIRA_TOKEN, GMAIL_PASS, JIRA_URL]):
        print("Missing environment variables in .env.example file.")
        return

    # Fetch data for the report
    count_created, list_created = get_issues(f"project={PROJECT_KEY} AND created >= -7d")
    count_resolved, list_resolved = get_issues(f"project={PROJECT_KEY} AND resolved >= -7d")
    count_open, list_open = get_issues(f"project={PROJECT_KEY} AND statusCategory != Done")

    report = f"""
Jira Weekly Status Report: Project {PROJECT_KEY}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
--------------------------------------------------

SUMMARY STATS:
- Issues Created (Last 7 Days): {count_created}
- Issues Resolved (Last 7 Days): {count_resolved}
- Total Currently Open: {count_open}

DETAILED LIST (With Links):
Created This Week:
{list_created}
Currently Open:
{list_open}

--------------------------------------------------
    """

    # Send Email
    msg = MIMEText(report)
    msg["Subject"] = f"Weekly Jira Report - {PROJECT_KEY}"
    msg["From"] = JIRA_EMAIL
    msg["To"] = JIRA_EMAIL  # In real scenario, change to Project Lead Email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(JIRA_EMAIL, GMAIL_PASS)
            server.send_message(msg)
            print("Report sent to Project Lead.")
    except Exception as e:
        print(f"SMTP Error: {e}")


if __name__ == "__main__":
    main()