import os
import requests

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


# Call this function with the file content to update the file on GitHub
def upload_isins_from_file(file_path, content_string):
    # Save the uploaded content as a file in the ISIN upload directory
    with open(file_path, 'wb') as f:
        f.write(base64.b64decode(content_string))

    # Read ISINs from the provided file_path
    isin_list = []
    with open(file_path, 'r') as file:
        for line in file:
            isin_list.append(line.strip())

    processed_count = 0
    for isin in isin_list:
        if check_isin(isin):
            processed_count += 1

    return processed_count

# Example usage
file_path = "Code/Data/ISIN-Upload/ISIN-Input.csv"
with open(file_path, 'r') as file:
    content_string = file.read()

processed_count = upload_isins_from_file(file_path, content_string)
print(f"{processed_count} ISINs processed. Upload result: {upload_result}")
