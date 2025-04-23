import requests
import datetime

API_KEY = 'BM5LO4IN65RBIRG3G2ADROXVMRUA6UFSKDDAFPRWUWQVWZHFIRYGZ7DGF3QJSJHKWU4OEQGXM6KDXRNIO'
EXPIRY_THRESHOLD_DAYS = 30  # Days before expiry to notify

headers = {
    'X-DC-DEVKEY': API_KEY,
    'Content-Type': 'application/json'
}

def get_certificates():
    url = "https://certcentral.digicert.com/services/v2/certificate"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json().get('certificates', [])

def check_expiry(certs):
    today = datetime.datetime.utcnow()
    for cert in certs:
        expiry_date_str = cert.get('valid_till')
        if expiry_date_str:
            expiry_date = datetime.datetime.strptime(expiry_date_str, "%Y-%m-%d")
            days_remaining = (expiry_date - today).days
            if days_remaining <= EXPIRY_THRESHOLD_DAYS:
                print(f"⚠️ Certificate '{cert['common_name']}' expires in {days_remaining} days!")
                # trigger your notification function here (email/SMS/etc.)

certs = get_certificates()
check_expiry(certs)
