import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import datetime

app = Flask(__name__)
CORS(app)

# --- AYARLAR ---
DB_NAME = "b1x_partners.db"
GMAIL_USER = "akrobathan@gmail.com" # Gönderen e-posta
GMAIL_PASS = "BURAYA_UYGULAMA_SIFRESI_GELECEK" # Gmail "Uygulama Şifresi"
RECEIVER_EMAIL = "akrobathan@gmail.com" # Bildirimin gideceği adres

def send_email(partner_data):
    """Yeni bir başvuru geldiğinde e-posta gönderir."""
    try:
        subject = f"🔥 Yeni B1x Ortağı: {partner_data['name']}"
        body = f"""
        Yeni bir katılım talebi alındı:
        
        İsim/Kurum: {partner_data['name']}
        E-posta: {partner_data['email']}
        LinkedIn: {partner_data['linkedin']}
        Rol: {partner_data['role']}
        Not: {partner_data['message']}
        
        Tarih: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        """
        
        msg = MIMEMultipart()
        msg['From'] = GMAIL_USER
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(GMAIL_USER, GMAIL_PASS)
        server.send_message(msg)
        server.quit()
        print("✅ E-posta başarıyla gönderildi!")
    except Exception as e:
        print(f"❌ E-posta gönderme hatası: {e}")

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS partners 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT, 
                  linkedin TEXT, role TEXT, message TEXT, timestamp DATETIME)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data: return jsonify({"status": "error"}), 400

    try:
        # 1. Veritabanına Kaydet
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("INSERT INTO partners (name, email, linkedin, role, message, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
                  (data['name'], data['email'], data['linkedin'], data['role'], data['message'], datetime.datetime.now()))
        conn.commit()
        conn.close()
        
        # 2. E-posta Gönder (Burada devreye giriyor)
        send_email(data)
        
        return jsonify({"status": "success"}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
