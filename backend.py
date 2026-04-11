from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

html = """
<!DOCTYPE html>
<html>
<head>
    <title>CIRAKAI ENGINE</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: Arial;
            background: #0f172a;
            color: white;
            text-align: center;
            margin-top: 80px;
        }
        .box {
            background: #1e293b;
            padding: 30px;
            border-radius: 20px;
            display: inline-block;
            width: 90%;
            max-width: 400px;
        }
        input {
            padding: 12px;
            width: 100%;
            border-radius: 10px;
            border: none;
            margin-top: 20px;
        }
        button {
            padding: 12px;
            margin-top: 20px;
            border-radius: 10px;
            border: none;
            background: #22c55e;
            color: white;
            font-weight: bold;
            width: 100%;
        }
        #sonuc {
            margin-top: 25px;
            font-size: 18px;
            color: #38bdf8;
        }
    </style>
</head>

<body>
<div class="box">
    <h1>🚀 CIRAKAI ENGINE</h1>
    <p>Mühendislik hesaplama asistanı</p>

    <input id="input" placeholder="Örn: 10 5 2">
    <button onclick="hesapla()">HESAPLA</button>

    <div id="sonuc"></div>
</div>

<script>
function hesapla() {
    let text = document.getElementById("input").value;

    fetch("/analyze", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ text: text })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("sonuc").innerHTML =
            "İvme: " + data.ivme + "<br>" +
            "Kuvvet: " + data.kuvvet + "<br>" +
            "Enerji: " + data.enerji;
    })
}
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(html)

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    text = data.get("text", "")

    try:
        numbers = [float(x) for x in text.split()]

        if len(numbers) >= 3:
            m, v, t = numbers[0], numbers[1], numbers[2]

            a = v / t
            F = m * a
            E = 0.5 * m * v**2

            return jsonify({
                "ivme": round(a, 2),
                "kuvvet": round(F, 2),
                "enerji": round(E, 2)
            })

    except:
        pass

    return jsonify({"ivme": 0, "kuvvet": 0, "enerji": 0})


if __name__ == "__main__":
    app.run()
