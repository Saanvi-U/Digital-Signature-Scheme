import requests
import time

# Suppress SSL warnings for self-signed HTTPS cert
requests.packages.urllib3.disable_warnings()

BASE_URL = "https://127.0.0.1:5000"
USER_ID = "user123"
NAME = "Alice"

def print_step(title):
    print(f"\n[•] {title}")

def save_file_from_response(response, filename):
    with open(filename, "wb") as f:
        f.write(response.content)

print_step("Creating certificate...")
data = {"name": NAME, "id": USER_ID}
res = requests.post(f"{BASE_URL}/create_certificate", data=data, verify=False)
if res.status_code == 200:
    save_file_from_response(res, f"{USER_ID}.txt")
    print("✅ Certificate created.")
else:
    print("❌ Failed to create certificate:", res.status_code, res.text)
    exit()

time.sleep(1)

print_step("Signing certificate...")
res = requests.get(f"{BASE_URL}/sign_certificate/{USER_ID}", verify=False)
if res.status_code == 200:
    save_file_from_response(res, f"{USER_ID}.sig")
    print("✅ Certificate signed.")
else:
    print("❌ Failed to sign certificate:", res.status_code, res.text)
    exit()

time.sleep(1)

print_step("Verifying original certificate...")
with open(f"{USER_ID}.txt", "rb") as cert_file, open(f"{USER_ID}.sig", "rb") as sig_file:
    files = {
        'certificate_file': cert_file,
        'signature_file': sig_file
    }
    res = requests.post(f"{BASE_URL}/verify_certificate", files=files, verify=False)
    print("✅ Verification result (original):", res.json()["status"])

print_step("Tampering certificate for test...")
# Modify the certificate
with open(f"{USER_ID}.txt", "a") as f:
    f.write("\n[TAMPERED LINE]")

with open(f"{USER_ID}.txt", "rb") as cert_file, open(f"{USER_ID}.sig", "rb") as sig_file:
    files = {
        'certificate_file': cert_file,
        'signature_file': sig_file
    }
    res = requests.post(f"{BASE_URL}/verify_certificate", files=files, verify=False)
    print("✅ Tampered certificate verification result:", res.json().get("status", "No status key returned"))

print_step("Signing a message...")
message = "This is a secure message."
res = requests.post(f"{BASE_URL}/sign_message", data={"message": message}, verify=False)
if res.status_code == 200:
    data = res.json()
    signature = data["signature"]
    print("✅ Message signed.")

    print_step("Verifying signed message...")
    res = requests.post(f"{BASE_URL}/verify_message", data={
        "message": message,
        "signature": signature
    }, verify=False)
    print("✅ Message verification result:", res.json()["status"])

    print_step("Tampering message for test...")
    tampered_message = message + " Extra text!"
    res = requests.post(f"{BASE_URL}/verify_message", data={
        "message": tampered_message,
        "signature": signature
    }, verify=False)
    print("✅ Tampered message verification result:", res.json()["status"])
else:
    print("❌ Failed to sign message:", res.status_code, res.text)
