import subprocess

# Path to your OpenVPN configuration file
config_file = "/home/abdallah/Downloads/sslvpn-abdallahdou-client-config.ovpn"
# Path to your credentials file (with username and password)
vpn_username = "abdallahdou"
vpn_password = "Mynewaccount0123456*"
# OpenVPN command with the config file and credentials file
vpn_command = [
    'sudo', 'openvpn',
    '--config', config_file,
 '--auth-user-pass', '/dev/stdin'  # Pass credentials via stdin
]

# Run the command to start the VPN connection
try:
    subprocess.run(vpn_command, check=True)
    print("VPN connected successfully")
except subprocess.CalledProcessError as e:
    print(f"Error connecting to VPN: {e}")
