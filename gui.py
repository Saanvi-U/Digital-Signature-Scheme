import streamlit as st
import requests
import os

# Backend URL (change if Flask server is hosted elsewhere)
BACKEND_URL = "https://127.0.0.1:5000"

st.set_page_config(page_title="🔐 Digital Signature GUI", layout="centered")
st.title("🔐 Digital Signature Scheme")

# Turn off SSL verification warning
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

option = st.sidebar.selectbox("Choose an action:", [
    "Create Certificate",
    "Sign Certificate",
    "Verify Certificate",
    "Sign Message",
    "Verify Message"
])

if option == "Create Certificate":
    st.subheader("📄 Create Certificate")
    name = st.text_input("Enter your name:")
    user_id = st.text_input("Enter your user ID:")
    if st.button("Create"):
        data = {"name": name, "id": user_id}
        res = requests.post(f"{BACKEND_URL}/create_certificate", data=data, verify=False)
        if res.status_code == 200:
            cert_path = f"{user_id}.txt"
            with open(cert_path, "wb") as f:
                f.write(res.content)
            st.success("Certificate created!")
            st.download_button("Download Certificate", file_name=cert_path, data=res.content)
        else:
            st.error("Failed to create certificate")

elif option == "Sign Certificate":
    st.subheader("✍️ Sign Certificate")
    user_id = st.text_input("Enter certificate ID (user ID):")
    if st.button("Sign"):
        res = requests.get(f"{BACKEND_URL}/sign_certificate/{user_id}", verify=False)
        if res.status_code == 200:
            sig_path = f"{user_id}.sig"
            with open(sig_path, "wb") as f:
                f.write(res.content)
            st.success("Certificate signed!")
            st.download_button("Download Signature", file_name=sig_path, data=res.content)
        else:
            st.error("Signing failed. Make sure the certificate exists.")

elif option == "Verify Certificate":
    st.subheader("🔍 Verify Certificate")
    cert_file = st.file_uploader("Upload Certificate File", type=["txt"])
    sig_file = st.file_uploader("Upload Signature File", type=["sig"])
    if cert_file and sig_file and st.button("Verify"):
        files = {
            'certificate': cert_file,
            'signature': sig_file
        }
        res = requests.post(f"{BACKEND_URL}/verify_certificate", files=files, verify=False)
        st.write(res.json().get("status"))

elif option == "Sign Message":
    st.subheader("✉️ Sign Message")
    msg = st.text_area("Enter message to sign:")
    if st.button("Sign Message"):
        res = requests.post(f"{BACKEND_URL}/sign_message", data={"message": msg}, verify=False)
        if res.status_code == 200:
            signature = res.json().get("signature")
            st.success("Message signed!")
            st.text_area("Signature (base64):", signature)
        else:
            st.error("Failed to sign message.")

elif option == "Verify Message":
    st.subheader("📬 Verify Message")
    msg = st.text_area("Enter message:")
    signature = st.text_area("Enter base64 signature:")
    if st.button("Verify Message"):
        res = requests.post(f"{BACKEND_URL}/verify_message", data={"message": msg, "signature": signature}, verify=False)
        try:
          st.write(res.json().get("status"))
        except requests.exceptions.JSONDecodeError:
          st.error("❌ INVALID message/signature")

