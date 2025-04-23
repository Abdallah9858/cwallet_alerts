import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import requests
import time

JENKINS_URL = "https://dev-jenkins-onprem.cwallet.qa/job/"
JOB_NAME = "DR/job/DR-DATABASE-SYNC"


USERNAME = "abdallahdou"
PASSWORD = "Abdallah77@cwallet*"
TEAMS_WEBHOOK_URL = "https://devteamcwallet.webhook.office.com/webhookb2/fe33dbc5-b5a2-485f-b1a4-39a25292367b@561f6207-9da0-40bf-8012-39dfd3ff9a8d/IncomingWebhook/5331f63defb34cf9ad57141422bc1c3d/f91d8394-4b4a-42ec-beec-fd41d90b972e/V2Mb5f8vkvkySNmC31QCqIVLlNbM6gb5UjVAzqrV-x6vo1"

def get_latest_build_status():
    url = f"{JENKINS_URL}/job/{JOB_NAME}/lastBuild/api/json"
    try:
        response = requests.get(url, auth=(USERNAME, PASSWORD), verify=False)
        if response.status_code == 200:
            data = response.json()
            return data.get('result'), data.get('number')
        else:
            print(f"Failed to fetch build status: {response.status_code}")
            return None, None
    except Exception as e:
        print(f"Error fetching build status: {e}")
        return None, None

def send_teams_notification(build_number, status):
    message = {
        "text": f"🚨 Jenkins Deployment Failed: Build #{build_number}\nStatus: **{status}**"
    }
    response = requests.post(TEAMS_WEBHOOK_URL, json=message)
    if response.status_code != 200:
        print("❌ Failed to send Teams message")

def monitor():
    last_checked_build = None
    while True:
        status, build_number = get_latest_build_status()
        if build_number and build_number != last_checked_build:
            print(f"🔍 Build #{build_number} status: {status}")
            if status == "FAILURE":
                send_teams_notification(build_number, status)
            last_checked_build = build_number
        time.sleep(60)  # Check every 60 seconds

if __name__ == "__main__":
    monitor()
