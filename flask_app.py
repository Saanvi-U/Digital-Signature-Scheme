from flask import Flask, request, send_file, jsonify
import os
from datetime import datetime, timezone
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
import base64

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = "uploads"
app.config['CERTIFICATE_FOLDER'] = "certificates"
app.config['SIGNATURE_FOLDER'] = "signatures"
app.config['SECRET_KEY'] = 'supersecretkey'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['CERTIFICATE_FOLDER'], exist_ok=True)
os.makedirs(app.config['SIGNATURE_FOLDER'], exist_ok=True)

PRIVATE_KEY_PATH = "private_key.pem"
PUBLIC_KEY_PATH = "public_key.pem"

# Generate ECDSA Keys
def generate_keys():
    if not (os.path.exists(PRIVATE_KEY_PATH) and os.path.exists(PUBLIC_KEY_PATH)):
        private_key = ec.generate_private_key(ec.SECP256R1())
        public_key = private_key.public_key()
        with open(PRIVATE_KEY_PATH, "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))
        with open(PUBLIC_KEY_PATH, "wb") as f:
            f.write(public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))

generate_keys()

@app.route('/')
def home():
    return '''
    <h1>🔐 Digital Signature Scheme Server</h1>
    <p>API Endpoints:</p>
    <ul>
        <li>POST /create_certificate</li>
        <li>GET /sign_certificate/&lt;user_id&gt;</li>
        <li>POST /verify_certificate</li>
        <li>POST /sign_message</li>
        <li>POST /verify_message</li>
    </ul>
    '''

@app.route('/create_certificate', methods=['POST'])
def create_certificate():
    name = request.form.get("name")
    user_id = request.form.get("id")
    if not name or not user_id:
        return jsonify({"error": "Missing name or ID"}), 400
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    content = f"Certificate of Identity\nName: {name}\nID: {user_id}\nIssued At: {date_str}\n"
    cert_path = os.path.join(app.config['CERTIFICATE_FOLDER'], f"{user_id}.txt")
    with open(cert_path, "w") as f:
        f.write(content)
    return send_file(cert_path, as_attachment=True)

@app.route('/sign_certificate/<cert_id>', methods=['GET'])
def sign_certificate(cert_id):
    cert_path = os.path.join("certificates", f"{cert_id}.txt")
    sig_path = os.path.join("signatures", f"{cert_id}.sig")

    if not os.path.exists(cert_path):
        return jsonify({"error": "Certificate not found"}), 404

    try:
        with open(cert_path, "rb") as f:
            cert_data = f.read()

        with open("private_key.pem", "rb") as f:
            private_key = serialization.load_pem_private_key(f.read(), password=None)

        signature = private_key.sign(cert_data, ec.ECDSA(hashes.SHA256()))

        with open(sig_path, "wb") as f:
            f.write(signature)

        return send_file(sig_path, as_attachment=True)
    except Exception as e:
        return jsonify({"error": f"Signing failed: {str(e)}"}), 500

@app.route('/verify_certificate', methods=['POST'])
def verify_certificate():
    cert_file = request.files.get("certificate")
    sig_file = request.files.get("signature")

    if not cert_file or not sig_file:
        return jsonify({
            "status": "Missing certificate or signature file",
            "error": True
        }), 400

    cert_data = cert_file.read()
    sig_data = sig_file.read()

    try:
        with open(PUBLIC_KEY_PATH, "rb") as f:
            public_key = serialization.load_pem_public_key(f.read())

        public_key.verify(sig_data, cert_data, ec.ECDSA(hashes.SHA256()))

        return jsonify({
            "status": "Certificate is valid ✅",
            "error": False
        }), 200

    except Exception as e:
        return jsonify({
            "status": "Invalid certificate. Tampering detected!",
            "error": True,
            "detail": str(e)
        }), 200

@app.route('/sign_message', methods=['POST'])
def sign_message():
    message = request.form.get("message")
    if not message:
        return jsonify({"error": "No message provided"}), 400
    with open(PRIVATE_KEY_PATH, "rb") as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None)
    signature = private_key.sign(message.encode(), ec.ECDSA(hashes.SHA256()))
    return jsonify({
        "message": message,
        "signature": base64.b64encode(signature).decode()
    })

@app.route('/verify_message', methods=['POST'])
def verify_message():
    message = request.form.get("message")
    signature_b64 = request.form.get("signature")
    if not message or not signature_b64:
        return jsonify({"error": "Missing message or signature"}), 400
    signature = base64.b64decode(signature_b64)
    with open(PUBLIC_KEY_PATH, "rb") as f:
        public_key = serialization.load_pem_public_key(f.read())
    try:
        public_key.verify(signature, message.encode(), ec.ECDSA(hashes.SHA256()))
        return jsonify({"status": "Valid message. No tampering detected."})
    except Exception as e:
        return jsonify({"status": "Invalid message. Tampering detected!", "error": str(e)})

@app.route('/public_key', methods=['GET'])
def download_public_key():
    return send_file(PUBLIC_KEY_PATH, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, ssl_context=('cert.pem', 'key.pem'))
