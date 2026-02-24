Jira Weekly Reporter 📊📧

Automated weekly Jira report generator that sends email notifications using GitHub Actions and secure repository secrets.

This project runs jira-email-notification.py on a schedule and emails a Jira report using environment variables stored securely in GitHub Secrets.

🚀 Features

Weekly scheduled execution (Every Monday)

Manual run via GitHub Actions

Secure secret management

Works with Jira Cloud

No need to run locally

📁 Project Structure
.
├── jira-email-notification.py
├── requirements.txt
└── .github/
    └── workflows/
        └── jira-weekly-reporter.yml
🔐 Required GitHub Secrets

Go to:

Repository → Settings → Secrets and variables → Actions

Add these secrets:

Secret Name	Description
JIRA_EMAIL	Your Jira account email
JIRA_TOKEN	Jira API token
JIRA_URL	Your Jira base URL (e.g. https://company.atlassian.net
)
GMAIL_PASS	Gmail App Password

⚠️ Secret names must match exactly (case-sensitive).

🔑 How to Generate Jira API Token

Log in to your Atlassian account

Go to Security → API tokens

Create a new API token

Copy it and store it in GitHub as JIRA_TOKEN

⚙️ GitHub Actions Workflow

The workflow file is located at:

.github/workflows/jira-weekly-reporter.yml

It runs:

Automatically every Monday at 09:00 UTC

Manually using the Run workflow button in the Actions tab

▶️ Run Manually

Go to your repository on GitHub

Click Actions

Select Jira Weekly Reporter

Click Run workflow

🖥 Optional: Run Locally

If you want to test locally:

export JIRA_EMAIL="your-email"
export JIRA_TOKEN="your-token"
export JIRA_URL="https://company.atlassian.net"
export GMAIL_PASS="your-app-password"

python jira-email-notification.py

Or use a .env file with python-dotenv.

📦 Install Dependencies (Local Only)
pip install -r requirements.txt
🛡 Security Notes

Secrets are not stored in code

GitHub injects them securely during workflow execution

Secret values are masked in logs

Do NOT commit .env files

⏰ Current Schedule
0 9 * * 1

Meaning: Every Monday at 09:00 UTC
