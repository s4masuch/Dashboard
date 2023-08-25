import os
import requests

GITHUB_API_BASE_URL = "https://api.github.com"
REPO_OWNER = "s4masuch"
REPO_NAME = "Dashboard"
FILE_PATH = "Code/Data/ISIN-Upload/ISIN%20Input.csv"  # URL-encoded path

def upload_isins_to_github(file_path, file_content):
    github_token = os.getenv("GITHUB_TOKEN")  # Set your GitHub Personal Access Token as an environment variable
    
    if not github_token:
        return "Error: GitHub token not provided"
    
    url = f"{GITHUB_API_BASE_URL}/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}"
    
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

# Call this function with the file content to update the file on GitHub
def upload_isins_from_file(file_path):
    # Read ISINs from the provided file_path
    isin_list = []
    with open(file_path, 'r') as file:
        for line in file:
            isin_list.append(line.strip())

    processed_count = 0
    for isin in isin_list:
        if check_isin(isin):
            processed_count += 1
    
    # Read the content of the file and upload it to GitHub
    with open(file_path, 'rb') as file:
        file_content = file.read()
        upload_result = upload_isins_to_github(FILE_PATH, file_content)
        return processed_count, upload_result

# Example usage
file_path = "Code/Data/ISIN-Upload/ISIN Input.csv"
processed_count, upload_result = upload_isins_from_file(file_path)
print(f"{processed_count} ISINs processed. Upload result: {upload_result}")
