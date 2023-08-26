import os
import requests
import base64

GITHUB_API_BASE_URL = "https://api.github.com"
REPO_OWNER = "s4masuch"
REPO_NAME = "Dashboard"
FILE_PATH = "Code/Data/ISIN-Upload/ISIN-Input.csv"  # URL-encoded path

def upload_isins_to_github(file_path, file_content):
    github_token = os.getenv("GITHUB_TOKEN")
    repo_owner = app.config["REPO_OWNER"]  # Retrieve from app.config
    repo_name = app.config["REPO_NAME"]  # Retrieve from app.config
    encoded_file_path = requests.utils.quote(file_path)  # URL-encode the file path

    if not github_token:
        return "Error: GitHub token not provided"

    url = f"{GITHUB_API_BASE_URL}/repos/{repo_owner}/{repo_name}/contents/{encoded_file_path}"

    headers = {
        "Authorization": f"Bearer {github_token}"
    }

    response = requests.put(url, json={
        "message": "Update ISIN file",
        "content": file_content
    }, headers=headers)

    if response.status_code == 200:
        return "File updated on GitHub successfully"
    else:
        return f"Error updating file on GitHub: {response.text}"
