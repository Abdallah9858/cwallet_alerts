import requests
import xml.etree.ElementTree as ET

# API request to get interface statuses
url = "https://192.168.20.1:4444/webconsole/APIController"
data = {
    "reqxml": """
    <Request>
        <Login>
            <Username>admin</Username>
            <Password>Pass@41234</Password>
        </Login>
        <Get>
            <Interface></Interface>
        </Get>
    </Request>
    """
}

# Disable SSL verification if using a self-signed certificate
response = requests.post(url, data=data, verify=False)

# Parse XML response
root = ET.fromstring(response.text)

# Initialize message to collect all interface statuses
message = "Interface Status Report (Not Connected):\n\n"

# List of interfaces to exclude from the search
excluded_interfaces = ["Port1", "PortF1", "PortF2", "PortMGMT"]

# Microsoft Teams Webhook URL
TEAMS_WEBHOOK_URL = "https://devteamcwallet.webhook.office.com/webhookb2/6c62caa4-6967-45fd-992d-bc1d596143e6@561f6207-9da0-40bf-8012-39dfd3ff9a8d/IncomingWebhook/f39f143adea14a43b76b6291a782f2b3/f91d8394-4b4a-42ec-beec-fd41d90b972e/V2Xcq91ZxTuJYEc6PtkZlKqbieBEIRT0jWpufyo1G1bhA1"

# Loop through all interfaces and check the status
for interface in root.findall("Interface"):
    # Get the interface name (e.g., Port2, Port3)
    port_name = interface.find("Name").text if interface.find("Name") is not None else "Unknown"
    
    # Check if the current interface should be excluded
    if port_name in excluded_interfaces:
        continue  # Skip this interface if it is in the exclusion list
    
    # Get the status of the interface (e.g., Connected, Disabled)
    status = interface.find("Status").text if interface.find("Status") is not None else "Unknown"
    
    # Check if the status is not "Connected"
    if "Connected" not in status:
        # Append the interface information to the message if not connected
        message += f"Interface: {port_name}\nStatus: {status}\n\n"

# If there are interfaces with a non-connected status, send the notification
if len(message) > len("Interface Status Report (Not Connected):\n\n"):  # If message contains any non-connected status
    teams_payload = {
        "text": message
    }
    response = requests.post(TEAMS_WEBHOOK_URL, json=teams_payload)

    # Check for successful response
    if response.status_code == 200:
        print("Notification sent to Microsoft Teams.")
    else:
        print(f"Failed to send notification. Status code: {response.status_code}")
else:
    print("No interfaces with a non-connected status.")
