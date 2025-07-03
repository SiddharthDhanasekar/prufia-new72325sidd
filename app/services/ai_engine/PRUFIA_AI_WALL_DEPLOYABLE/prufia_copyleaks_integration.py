
import requests
import time

# Replace with your Copyleaks API credentials
COPYLEAKS_EMAIL = "your_email@example.com"
COPYLEAKS_API_KEY = "your_api_key"

def authenticate_copyleaks():
    """
    Authenticate and retrieve Copyleaks access token.
    """
    url = "https://id.copyleaks.com/v3/account/login/api"
    payload = {
        "email": COPYLEAKS_EMAIL,
        "key": COPYLEAKS_API_KEY
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()["access_token"]

def submit_plagiarism_scan(text, token, scan_id):
    """
    Submit the document for plagiarism scanning.
    """
    headers = {
        "Authorization": f"Bearer {token}"
    }
    url = f"https://api.copyleaks.com/v3/education/submit/{scan_id}"
    payload = {
        "base64": False,
        "text": text,
        "properties": {
            "webhooks": {
                "status": "https://your-callback-url.com/status",  # Optional webhook
                "completed": "https://your-callback-url.com/completed"  # Optional webhook
            }
        }
    }
    response = requests.put(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.status_code

def check_scan_completion(scan_id, token):
    """
    Poll the Copyleaks server for scan completion (manual polling method).
    """
    headers = {
        "Authorization": f"Bearer {token}"
    }
    url = f"https://api.copyleaks.com/v3/education/status/{scan_id}"
    for attempt in range(10):
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        status = response.json()
        if status.get("status") == "completed":
            return True
        time.sleep(10)  # Wait before retrying
    return False

def fetch_results(scan_id, token):
    """
    Retrieve plagiarism results.
    """
    headers = {
        "Authorization": f"Bearer {token}"
    }
    url = f"https://api.copyleaks.com/v3/education/result/{scan_id}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

# Example Usage
if __name__ == "__main__":
    document_text = "This is a test document to scan for plagiarism."
    scan_id = "your-unique-scan-id-123456789"

    try:
        token = authenticate_copyleaks()
        submit_plagiarism_scan(document_text, token, scan_id)
        if check_scan_completion(scan_id, token):
            results = fetch_results(scan_id, token)
            print("Plagiarism Scan Complete. Results:")
            print(results)
        else:
            print("Scan did not complete within expected time.")
    except Exception as e:
        print(f"Error during Copyleaks processing: {e}")
