import requests

# Your actual API key here
API_KEY = "BM5LO4IN65RBIRG3G2ADROXVMRUA6UFSKDDAFPRWUWQVWZHFIRYGZ7DGF3QJSJHKWU4OEQGXM6KDXRNIO"

url = "https://www.digicert.com/services/v2/certificate/intermediates"
headers = {
    'X-DC-DEVKEY': API_KEY,
    'Content-Type': "application/json"
}

# Making a GET request
response = requests.get(url, headers=headers)

# Checking the status and saving to a file
if response.status_code == 200:
    with open("digicert_intermediates_output.txt", "w") as file:
        file.write(response.text)  # Save raw JSON response as text
    print("✅ Success! Output saved to digicert_intermediates_output.txt")
else:
    print(f"❌ Error: {response.status_code}")
    print(f"Error details: {response.text}")