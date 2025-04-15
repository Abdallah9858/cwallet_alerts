# Pending VPN:QCB_02,HQ_AZ_IPSEC,HQ_GulfExchange
# gateway status still have issue 
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
            <VPNIPSecConnection></VPNIPSecConnection>
            <GatewayConfiguration></GatewayConfiguration>          
            </Get>
    </Request>
    """
}
# Disable SSL verification if using a self-signed certificate
response = requests.post(url, data=data, verify=False)
# Parse XML response
root = ET.fromstring(response.text)
# Microsoft Teams Webhook URL
TEAMS_WEBHOOK_URL = "https://devteamcwallet.webhook.office.com/webhookb2/fe33dbc5-b5a2-485f-b1a4-39a25292367b@561f6207-9da0-40bf-8012-39dfd3ff9a8d/IncomingWebhook/5331f63defb34cf9ad57141422bc1c3d/f91d8394-4b4a-42ec-beec-fd41d90b972e/V2Mb5f8vkvkySNmC31QCqIVLlNbM6gb5UjVAzqrV-x6vo1"
# SMS Configuration (Twilio example)

TWILIO_SID = "AC98115484ee8969f05f9fce78c5e748a8"
TWILIO_AUTH_TOKEN = "d2eefee36cb69fb3da24fd2a811f3c75"
TWILIO_FROM = "+12562902716"  # Twilio phone number
SMS_TO = "+97450125624"  # Your phone number
TWILIO_URL = f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_SID}/Messages.json"

# Check all interfaces
# List of ports to exclude
excluded_ports = ["Port1","PortF1", "PortF2", "PortMGMT"]
for interface in root.findall("Interface"):
    port_name = interface.find("Name").text
    # Skip excluded ports
    if port_name in excluded_ports:
        continue
    status = interface.find("Status").text
    if status != "Connected, 1000 Mbps - Full Duplex, FEC off":
        message = f"Alert: {port_name} is NOT connected! Current status: {status}"
        # Send SMS via Twilio
        sms_data = {
            "From": TWILIO_FROM,
            "To": SMS_TO,
            "Body": message,
        }
        requests.post(TWILIO_URL, data=sms_data, auth=(TWILIO_SID, TWILIO_AUTH_TOKEN))
        # Send notification to Microsoft Teams
        teams_payload = {
            "text": message
        }
        requests.post(TEAMS_WEBHOOK_URL, json=teams_payload)
        print(f"Disconnection alert sent for {port_name}")
    
  ########################################################################### 
        
  ##################        Check   VPN connections   #######################
  
  ########################################################################### 
  
  
for vpn_config in root.findall(".//VPNIPSecConnection/Configuration"):
    vpn_name = vpn_config.findtext("Name", default="Unknown VPN")
    
    # Skip VPNs that aren't QCB related
    if not vpn_name ==("QCB"):
        continue

    vpn_status = vpn_config.findtext("Status", default="Unknown")

    # Alert only if status is not "Active"
    if vpn_status != "2":
        message = f"🚨 VPN Alert: {vpn_name} is NOT active! Current status: {vpn_status}"
        
        sms_data = {
            "From": TWILIO_FROM,
            "To": SMS_TO,
            "Body": message,
        }
        try:
            requests.post(TWILIO_URL, data=sms_data, auth=(TWILIO_SID, TWILIO_AUTH_TOKEN))
            requests.post(TEAMS_WEBHOOK_URL, json={"text": message})
            print(f"VPN for {vpn_name} is Down ")
        except requests.exceptions.RequestException as e:
            print(f"Failed to send alert for VPN {vpn_name}: {e}")

 #######################################################################
 
  ##############    Gateway status    ##########################
  #######################################################################

gateway_status = "UNKNOWN"
for gateway in root.findall(".//GatewayConfiguration/Gateway"):
    name = gateway.findtext("Name")
    if name == "ADSL":
        gateway_status = gateway.findtext("Type")  # ← Now correctly checks ADSL
        break

if gateway_status != "Active":
    alert_msg = f"⚠️ ADSL Gateway is NOT active! Current status: {gateway_status}"
    try:
        requests.post(TWILIO_URL, data={"From": TWILIO_FROM, "To": SMS_TO, "Body": alert_msg}, auth=(TWILIO_SID, TWILIO_AUTH_TOKEN))
        requests.post(TEAMS_WEBHOOK_URL, json={"text": alert_msg})
        print("ADSL gateway alert sent.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send ADSL alert: {e}")
else:
    print("✅ ADSL gateway is active.")
