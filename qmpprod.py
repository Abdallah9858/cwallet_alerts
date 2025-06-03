import paramiko
import os
import requests
from twilio.rest import Client
# --- CONFIG ---
VM_IP = os.getenv("VM_IP", "192.168.5.12")
USERNAME = os.getenv("VM_USERNAME", "cwadmin")
PASSWORD = os.getenv("VM_PASSWORD", "Cwadmin@41234")

TEAMS_WEBHOOK_URL = "https://devteamcwallet.webhook.office.com/webhookb2/fe33dbc5-b5a2-485f-b1a4-39a25292367b@561f6207-9da0-40bf-8012-39dfd3ff9a8d/IncomingWebhook/5331f63defb34cf9ad57141422bc1c3d/f91d8394-4b4a-42ec-beec-fd41d90b972e/V2Mb5f8vkvkySNmC31QCqIVLlNbM6gb5UjVAzqrV-x6vo1"

TWILIO_SID = "AC98115484ee8969f05f9fce78c5e748a8"
TWILIO_AUTH_TOKEN = "d2eefee36cb69fb3da24fd2a811f3c75"
TWILIO_FROM = "+12562902716"
SMS_TO = "+97450125624"

# Only monitor these containers
GET_CONTAINERS = [
    "qmp-metric-uat",
    "qmp-heartbeat-uat",
    "qmp-reg-uat",
    "qmp-payment-uat",
    "qcb-payment-inward-uat",
    "qmp-uat-onprem-reposilite-1",
    "qmp_kibana_uat",
    "logstash",
    "postgres_uat",
    "redis_uat"
]

def send_teams_alert(message):
    try:
        payload = {"text": message}
        response = requests.post(TEAMS_WEBHOOK_URL, json=payload)
        if response.status_code != 200:
            print(f"❌ Failed to send Teams alert: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"❌ Exception during Teams alert: {e}")

def send_sms_alert(message):
    try:
        client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
        client.messages.create(body=message, from_=TWILIO_FROM, to=SMS_TO)
    except Exception as e:
        print(f"❌ Exception during SMS alert: {e}")

def run_command_on_vm():
    command = "docker ps -a --format '{{.Names}}: {{.Status}}'"
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(hostname=VM_IP, username=USERNAME, password=PASSWORD)
        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.read().decode()
        ssh.close()
    except Exception as e:
        error_msg = f"❌ SSH connection or command failed: {e}"
        print(error_msg)
        send_teams_alert(error_msg)
        send_sms_alert(error_msg)
        return

    # Parse output into a dictionary
    container_status = {}
    for line in output.splitlines():
        if ": " in line:
            name, status = line.split(": ", 1)
            container_status[name.strip()] = status.strip()

    # Print statuses of monitored containers
    print("📋 Monitored Docker Container Status:")

    # Check which are not running
    stopped = [
        name for name in GET_CONTAINERS
        if name not in container_status or not container_status[name].startswith("Up")
    ]

    if stopped:
        message = f"🚨 ALERT: qmp  container/s NOT running:\n" + "\n".join(stopped)
        send_teams_alert(message)
        send_sms_alert(message)
    else:
        print("✅ All monitored containers are running.")

if __name__ == "__main__":
    run_command_on_vm()
