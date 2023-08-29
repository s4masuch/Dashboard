import os
import requests
import base64

GITHUB_API_BASE_URL = "https://api.github.com"

def upload_isins_to_github(file_path, file_content):   
    print(f"In upload_ISINs.py")
    print(f"Debug: file_path={file_path}")
    print(f"Debug: file_content={file_content}")
    github_token = os.getenv("GITHUB_TOKEN")
    repo_owner = os.getenv("REPO_OWNER")
    repo_name = os.getenv("REPO_NAME")
    encoded_file_path = requests.utils.quote(file_path)  # URL-encode the file path

    if not github_token:
        return "Error: GitHub token not provided"

    url = f"{GITHUB_API_BASE_URL}/repos/{repo_owner}/{repo_name}/contents/{encoded_file_path}"

    headers = {
        "Authorization": f"Bearer {github_token}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        file_sha = response.json()["sha"]
        response = requests.put(url, json={
            "message": "Update ISIN file",
            "content": base64.b64encode(file_content.encode()).decode(),  # Encode content as base64
            "sha": file_sha
        }, headers=headers)

        if response.status_code == 200:
            return "File updated on GitHub successfully"
        else:
            return f"Error updating file on GitHub: {response.status_code} - {response.text}"
    else:
        # If the file doesn't exist, create it
        response = requests.put(url, json={
            "message": "Upload ISIN file",
            "content": base64.b64encode(file_content.encode()).decode()  # Encode content as base64
        }, headers=headers)

        if response.status_code == 201:
            return "File created on GitHub successfully"
        else:
            return f"Error creating file on GitHub: {response.status_code} - {response.text}"
