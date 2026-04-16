from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import datetime

app = Flask(__name__)
# Frontend HTML'in başka bir port/domain'den buraya veri atmasına izin verir
CORS(app) 

DB_NAME = "b1x_partners.db"

def init_db():
    """İlk çalışmada veritabanını ve tabloyu oluşturur."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS partners (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            linkedin TEXT NOT NULL,
            role TEXT NOT NULL,
            message TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/api/register', methods=['POST'])
def register():
    """HTML formundan gelen JSON verisini yakalar ve DB'ye yazar."""
    data = request.get_json()
    
    if not data or not data.get('name') or not data.get('email'):
        return jsonify({"status": "error", "message": "Eksik bilgi gönderildi."}), 400

    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('''
            INSERT INTO partners (name, email, linkedin, role, message, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            data['name'], 
            data['email'], 
            data['linkedin'], 
            data['role'], 
            data['message'],
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
        conn.commit()
        conn.close()
        
        print(f"🔥 YENİ ORTAK GELDİ: {data['name']} - Rol: {data['role']}")
        return jsonify({"status": "success", "message": "Kayıt başarıyla alındı."}), 201

    except Exception as e:
        print(f"Hata oluştu: {e}")
        return jsonify({"status": "error", "message": "Veritabanı hatası."}), 500

@app.route('/api/admin/list', methods=['GET'])
def get_list():
    """(GİZLİ) Senin kaç kişinin kayıt olduğunu görmen için basit bir endpoint."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM partners ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    
    return jsonify({"total_count": len(rows), "partners": rows})

if __name__ == '__main__':
    # Veritabanını başlat ve sunucuyu çalıştır
    init_db()
    print("🚀 B1x Backend ÇırakAI sisteminde aktif! Port: 5000 dinleniyor...")
    app.run(debug=True, host='0.0.0.0', port=5000)
