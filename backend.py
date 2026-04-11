from flask import Flask, request, jsonify, render_template_string
import requests
import os

app = Flask(__name__)

API_KEY = "BURAYA_API_KEY"

# ================= HTML =================
html = """ 
<!DOCTYPE html>
<html>
<head>
<title>CIRAKAI ENGINE</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
body{background:#0f172a;color:white;font-family:Arial;text-align:center;margin-top:80px;}
.box{background:#1e293b;padding:30px;border-radius:20px;display:inline-block;width:90%;max-width:500px;}
textarea{width:100%;padding:10px;border-radius:10px;border:none;margin-top:10px;}
button{margin-top:10px;padding:12px;border:none;border-radius:10px;background:#22c55e;color:white;}
#sonuc{margin-top:20px;color:#38bdf8;}
</style>
</head>

<body>
<div class="box">
<h1>🚀 CIRAKAI ENGINE</h1>

<textarea id="input" placeholder="Sorunu yaz..."></textarea>
<button onclick="gonder()">GÖNDER</button>

<div id="sonuc"></div>
</div>

<script>
function gonder(){
    let text = document.getElementById("input").value;

    document.getElementById("sonuc").innerText = "Yükleniyor...";

    fetch("/chat",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({message:text})
    })
    .then(res=>res.json())
    .then(data=>{
        document.getElementById("sonuc").innerText = data.reply;
    })
    .catch(()=>{
        document.getElementById("sonuc").innerText = "Hata oluştu";
    });
}
</script>

</body>
</html>
"""

# ================= ROUTES =================

@app.route("/")
def home():
    return render_template_string(html)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_msg = data.get("message", "")

    headers = {
        "x-api-key": API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }

    body = {
        "model": "claude-3-sonnet-20240229",
        "max_tokens": 500,
        "messages": [
            {"role": "user", "content": user_msg}
        ]
    }

    try:
        res = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers=headers,
            json=body
        )

        data = res.json()
        reply = data["content"][0]["text"]

    except:
        reply = "AI bağlantı hatası"

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run()
