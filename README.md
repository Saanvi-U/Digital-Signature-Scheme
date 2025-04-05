# 🔐 Digital Signature Scheme

## 📖 Overview
This project implements a Digital Signature Scheme using Flask for backend and Streamlit for GUI. It allows users to:

- Create and sign digital certificates.
- Verify digital certificates.
- Sign and verify messages using digital signatures.
- Detect tampering of certificates or messages.


## 🎥 Demo Video

👉 [Watch the demo video on Google Drive](https://drive.google.com/file/d/1XXW6NdYmnp2Mo2LFQOne0o-YWQpMF3kN/view?usp=sharing)
## 🚀 Features
- 📝 Create Certificate
- ✍️ Sign Certificate
- 🔍 Verify Certificate
- ✉️ Sign Message
- 📬 Verify Message
- 🌐 Flask API endpoints
- 🧪 Postman support
- 🎛️ Streamlit GUI for user interaction

# 💻 Run via GitHub Codespaces

You can run this project directly in your browser using GitHub Codespaces.

🔗 **Start Here**: [Open in Codespaces](https://github.com/codespaces/new?hide_repo_select=true&repo=961040898)

---

## ▶️ Running in GitHub Codespaces

Once inside the Codespace:

1. Open a terminal (`Ctrl + `` or View → Terminal`).
2. Run the Flask server: (Before that make sure to run generate_cert.py )
   ```bash
   python app.py
   ```
3. In a new terminal tab, run the Streamlit GUI:
   ```bash
   streamlit run gui.py --server.port 8501 --server.address 0.0.0.0
   ```
4. Streamlit will provide a public URL in the terminal once it’s running. Click that to open the app.

---

## 📦 Dependencies

Make sure to install the following Python packages:

```bash
pip install flask streamlit pycryptodome requests
```

If you are using Codespaces, these are already installed.

---

## 🧯 Troubleshooting & Common Issues

### 🔐 SSL Certificate Issues
If you're running the app locally with `https://127.0.0.1:5000`, you may see SSL warnings. You can:
- Use `verify=False` in your `requests` (already handled in the code), or
- Generate your own `cert.pem` and `key.pem` using:

```bash
openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365 -nodes
```

### 🌐 Streamlit 502 Gateway Error in Codespaces
If you encounter a `502` error:
- Ensure you used `--server.address 0.0.0.0` when starting Streamlit.
- Use port `8501` (GitHub automatically exposes this).
- Wait a few seconds for the public link to be generated in the terminal.

### 📂 File Access Issues
Make sure files like `key.pem`, `cert.pem`, `.txt`, and `.sig` are uploaded or generated inside the project folder.

---

## 📁 Folder Structure
```
Digital-Signature-Scheme/
├── app.py                  # Flask backend
├── gui.py                  # Streamlit frontend
├── certs/                  # SSL certificates (cert.pem, key.pem)
├── certificates/           # Generated certificates (.txt)
├── signatures/             # Generated signatures (.sig)
├── .gitignore              # Git ignore rules
└── README.md               # Project documentation
```

## ⚙️ Prerequisites
- Python 3.8+

## 🛠️ Installation
### 1. Clone the Repository
```bash
git clone https://github.com/Saanvi-U/Digital-Signature-Scheme.git
cd Digital-Signature-Scheme
```

### 2. Create and Activate Virtual Environment
#### For Windows:
```bash
python -m venv venv
venv\Scripts\activate
```
#### For macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install flask streamlit pycryptodome requests
```

## 🔐 SSL Setup (For HTTPS)
If you don’t have certificates, generate them:
```bash
mkdir certs
openssl req -x509 -newkey rsa:2048 -keyout certs/key.pem -out certs/cert.pem -days 365 -nodes
```

## 🚦 Running the App
### 1. Run Flask Backend
```bash
python app.py
```

### 2. Run Streamlit GUI (port 8501)
```bash
streamlit run gui.py --server.port 8501 --server.address 0.0.0.0
```

## ✅ Output Files
- 📄 Certificates saved in `/certificates`
- ✍️ Signatures saved in `/signatures`

## 📦 Dependencies
- Flask
- Streamlit
- PyCryptodome
- Requests

---

Enjoy securing your data! 🔐✨

