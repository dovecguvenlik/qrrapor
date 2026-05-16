from flask import Flask, request, render_template_string, send_file
from datetime import datetime
import os
import csv
import requests
import qrcode
from io import BytesIO

app = Flask(__name__)

LOG_FILE = "log.csv"

API_KEY = "re_NXXZwGLy_LYhX85m134ddVWhMbzC8gYrF"
EMAIL_TO = "1000inci@gmail.com"

# HTML Template - Ana Sayfa (Mobil Optimized)
HOME_PAGE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QR Devriye</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 20px;
            padding: 30px;
            text-align: center;
            max-width: 400px;
            width: 100%;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            animation: slideUp 0.6s ease-out;
        }
        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        h1 {
            color: #333;
            margin-bottom: 10px;
            font-size: 28px;
        }
        .subtitle {
            color: #666;
            margin-bottom: 30px;
            font-size: 14px;
        }
        .menu {
            display: grid;
            gap: 15px;
        }
        a {
            text-decoration: none;
            padding: 18px 20px;
            border-radius: 12px;
            font-weight: 600;
            font-size: 16px;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }
        a:active {
            transform: scale(0.98);
        }
        .btn-create {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .btn-report {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
        }
        .btn-scan {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            font-size: 18px;
        }
        .info {
            background: #f0f0f0;
            padding: 15px;
            border-radius: 10px;
            margin-top: 20px;
            font-size: 13px;
            color: #666;
            line-height: 1.6;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📱 QR Devriye</h1>
        <p class="subtitle">Hızlı QR kod tarama ve yönetimi</p>
        
        <div class="menu">
            <a href="/qr_generator" class="btn-create">📝 QR Kod Oluştur</a>
            <a href="/rapor" class="btn-report">📊 Raporları Görüntüle</a>
            <a href="/scan" class="btn-scan">📷 Hızlı Tara</a>
        </div>
        
        <div class="info">
            ℹ️ Devriye görevlisi olarak: "Hızlı Tara"'ya dokunun ve QR kodunuzu tarayın!
        </div>
    </div>
</body>
</html>
"""

# HTML Template - QR Üretici Arayüzü
QR_GENERATOR_HTML = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QR Kod Üretici</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            padding: 40px;
            max-width: 600px;
            width: 100%;
            animation: slideUp 0.6s ease-out;
        }
        
        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        h1 {
            color: #333;
            margin-bottom: 10px;
            font-size: 28px;
        }
        
        .subtitle {
            color: #666;
            margin-bottom: 30px;
            font-size: 14px;
        }
        
        .form-group {
            margin-bottom: 25px;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            color: #333;
            font-weight: 600;
            font-size: 14px;
        }
        
        input[type="text"],
        input[type="number"],
        select {
            width: 100%;
            padding: 12px 15px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 14px;
            transition: all 0.3s ease;
            font-family: inherit;
        }
        
        input[type="text"]:focus,
        input[type="number"]:focus,
        select:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        .form-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
        }
        
        @media (max-width: 500px) {
            .form-row {
                grid-template-columns: 1fr;
            }
        }
        
        .button-group {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-top: 30px;
        }
        
        button {
            padding: 14px;
            border: none;
            border-radius: 10px;
            font-weight: 600;
            font-size: 14px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-family: inherit;
        }
        
        .btn-generate {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            grid-column: span 2;
        }
        
        .btn-generate:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
        }
        
        .btn-generate:active {
            transform: translateY(0);
        }
        
        .btn-download {
            background: #4CAF50;
            color: white;
        }
        
        .btn-download:hover {
            background: #45a049;
            transform: translateY(-2px);
        }
        
        .btn-download:disabled {
            background: #ccc;
            cursor: not-allowed;
            transform: none;
        }
        
        .btn-print {
            background: #2196F3;
            color: white;
        }
        
        .btn-print:hover {
            background: #0b7dda;
            transform: translateY(-2px);
        }
        
        .btn-print:disabled {
            background: #ccc;
            cursor: not-allowed;
            transform: none;
        }
        
        .qr-preview {
            margin-top: 30px;
            padding: 20px;
            background: #f9f9f9;
            border-radius: 10px;
            text-align: center;
            display: none;
        }
        
        .qr-preview.show {
            display: block;
            animation: fadeIn 0.3s ease;
        }
        
        @keyframes fadeIn {
            from {
                opacity: 0;
            }
            to {
                opacity: 1;
            }
        }
        
        #qrImage {
            max-width: 300px;
            margin: 15px auto;
            display: block;
            border: 3px solid white;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        }
        
        .qr-info {
            color: #666;
            font-size: 13px;
            margin-top: 10px;
        }
        
        .success-message {
            background: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
            padding: 12px 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            display: none;
        }
        
        .success-message.show {
            display: block;
        }
        
        .tabs {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            border-bottom: 2px solid #e0e0e0;
        }
        
        .tab-btn {
            padding: 10px 20px;
            border: none;
            background: none;
            cursor: pointer;
            color: #999;
            font-weight: 600;
            font-size: 14px;
            border-bottom: 3px solid transparent;
            transition: all 0.3s ease;
            margin-bottom: -2px;
        }
        
        .tab-btn.active {
            color: #667eea;
            border-bottom-color: #667eea;
        }
        
        .tab-content {
            display: none;
        }
        
        .tab-content.active {
            display: block;
        }
        
        .btn-home {
            background: #666;
            color: white;
            grid-column: span 2;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📱 QR Kod Üretici</h1>
        <p class="subtitle">Devriye sistemi için QR kodları oluştur</p>
        
        <div class="success-message" id="successMsg">
            ✅ QR kod başarıyla oluşturuldu!
        </div>
        
        <div class="tabs">
            <button class="tab-btn active" onclick="switchTab('single')">Tek QR Kod</button>
            <button class="tab-btn" onclick="switchTab('multiple')">Toplu Oluştur</button>
        </div>
        
        <!-- TAB 1: TEK QR KOD -->
        <div class="tab-content active" id="single">
            <form id="qrForm">
                <div class="form-group">
                    <label for="qrId">QR Kodun Adı / ID</label>
                    <input 
                        type="text" 
                        id="qrId" 
                        placeholder="Örn: Depo-1, Giriş Kapısı"
                        required
                    >
                </div>
                
                <div class="form-group">
                    <label for="qrValue">QR Kod İçeriği (Opsiyonel)</label>
                    <input 
                        type="text" 
                        id="qrValue" 
                        placeholder="Boş bırakırsan QR ID kullanılır"
                    >
                </div>
                
                <button type="submit" class="btn-generate">QR Kod Oluştur</button>
            </form>
        </div>
        
        <!-- TAB 2: TOPLU OLUŞTUR -->
        <div class="tab-content" id="multiple">
            <form id="multipleForm">
                <div class="form-group">
                    <label for="baseName">Taban Adı</label>
                    <input 
                        type="text" 
                        id="baseName" 
                        placeholder="Örn: Depo"
                        required
                    >
                </div>
                
                <div class="form-row">
                    <div class="form-group">
                        <label for="startNum">Başlangıç</label>
                        <input 
                            type="number" 
                            id="startNum" 
                            value="1"
                            min="1"
                        >
                    </div>
                    <div class="form-group">
                        <label for="endNum">Bitiş</label>
                        <input 
                            type="number" 
                            id="endNum" 
                            value="10"
                            min="1"
                        >
                    </div>
                </div>
                
                <button type="submit" class="btn-generate">QR Kodları İndir (ZIP)</button>
            </form>
        </div>
        
        <!-- QR PREVIEW -->
        <div class="qr-preview" id="qrPreview">
            <h3>Ön İzleme</h3>
            <img id="qrImage" src="" alt="QR Kod">
            <div class="qr-info" id="qrInfo"></div>
            <div class="button-group">
                <button class="btn-download" id="downloadBtn" onclick="downloadQR()">⬇️ İndir (PNG)</button>
                <button class="btn-print" id="printBtn" onclick="printQR()">🖨️ Yazdır</button>
            </div>
        </div>
        
        <button class="btn-home" onclick="window.location.href='/'">← Ana Sayfa</button>
    </div>
    
    <script>
        let currentQRId = '';
        
        function switchTab(tab) {
            document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
            document.getElementById(tab).classList.add('active');
            event.target.classList.add('active');
        }
        
        document.getElementById('qrForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const qrId = document.getElementById('qrId').value;
            const qrValue = document.getElementById('qrValue').value || qrId;
            
            try {
                const response = await fetch(`/generate_qr?id=${encodeURIComponent(qrId)}&value=${encodeURIComponent(qrValue)}`);
                const blob = await response.blob();
                const url = URL.createObjectURL(blob);
                
                document.getElementById('qrImage').src = url;
                document.getElementById('qrInfo').textContent = `ID: ${qrId}`;
                document.getElementById('qrPreview').classList.add('show');
                document.getElementById('successMsg').classList.add('show');
                
                currentQRId = qrId;
                
                setTimeout(() => {
                    document.getElementById('successMsg').classList.remove('show');
                }, 3000);
            } catch (error) {
                alert('Hata: ' + error);
            }
        });
        
        document.getElementById('multipleForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const baseName = document.getElementById('baseName').value;
            const startNum = parseInt(document.getElementById('startNum').value);
            const endNum = parseInt(document.getElementById('endNum').value);
            
            const btn = e.target.querySelector('button');
            btn.disabled = true;
            btn.textContent = 'İşleniyor...';
            
            try {
                const response = await fetch(`/generate_qr_batch?base=${encodeURIComponent(baseName)}&start=${startNum}&end=${endNum}`);
                const blob = await response.blob();
                const url = URL.createObjectURL(blob);
                
                const a = document.createElement('a');
                a.href = url;
                a.download = `${baseName}_QR_Kodlari.zip`;
                a.click();
                
                document.getElementById('successMsg').classList.add('show');
                setTimeout(() => {
                    document.getElementById('successMsg').classList.remove('show');
                }, 3000);
            } catch (error) {
                alert('Hata: ' + error);
            } finally {
                btn.disabled = false;
                btn.textContent = 'QR Kodları İndir (ZIP)';
            }
        });
        
        function downloadQR() {
            const link = document.createElement('a');
            link.href = document.getElementById('qrImage').src;
            link.download = `${currentQRId}.png`;
            link.click();
        }
        
        function printQR() {
            const printWindow = window.open('', '', 'width=400,height=500');
            const img = document.getElementById('qrImage').src;
            printWindow.document.write(`
                <html>
                <head>
                    <title>QR Kod Yazdır</title>
                    <style>
                        body { margin: 20px; text-align: center; }
                        img { max-width: 400px; }
                        p { font-weight: bold; margin-top: 20px; }
                    </style>
                </head>
                <body>
                    <h2>${currentQRId}</h2>
                    <img src="${img}" alt="QR">
                    <p>Devriye Sistemi</p>
                </body>
                </html>
            `);
            printWindow.document.close();
            setTimeout(() => printWindow.print(), 500);
        }
    </script>
</body>
</html>
"""

# HTML Template - Mobil Hızlı Tara Sayfası
SCAN_PAGE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <title>QR Tara</title>
    <script src="https://cdn.jsdelivr.net/npm/jsqr@1.4.0/dist/jsQR.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #000;
            height: 100vh;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        #canvas {
            display: block;
            width: 100%;
            flex: 1;
            object-fit: cover;
        }
        .controls {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background: rgba(0, 0, 0, 0.8);
            padding: 12px;
            display: flex;
            gap: 10px;
            z-index: 100;
        }
        button {
            padding: 10px 15px;
            border: none;
            border-radius: 6px;
            font-weight: 600;
            cursor: pointer;
            flex: 1;
            font-size: 13px;
        }
        .btn-back {
            background: #f5576c;
            color: white;
        }
        .result {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: rgba(0, 0, 0, 0.95);
            color: white;
            padding: 20px;
            text-align: center;
            min-height: 90px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            gap: 8px;
            z-index: 50;
            animation: slideUp 0.3s ease;
        }
        @keyframes slideUp {
            from {
                transform: translateY(100%);
            }
            to {
                transform: translateY(0);
            }
        }
        .result.success {
            background: rgba(76, 175, 80, 0.95);
        }
        .result-text {
            font-size: 18px;
            font-weight: 700;
        }
        .countdown {
            font-size: 13px;
            color: #aaa;
        }
        .scanning-hint {
            position: fixed;
            top: 60px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(102, 126, 234, 0.9);
            color: white;
            padding: 10px 20px;
            border-radius: 20px;
            font-size: 13px;
            z-index: 10;
            animation: fadeInDown 0.4s ease;
        }
        @keyframes fadeInDown {
            from {
                opacity: 0;
                transform: translateX(-50%) translateY(-10px);
            }
            to {
                opacity: 1;
                transform: translateX(-50%) translateY(0);
            }
        }
    </style>
</head>
<body>
    <div class="controls">
        <button class="btn-back" onclick="goHome()">← Geri</button>
    </div>
    
    <div class="scanning-hint">📷 QR kodunu kameraya yaklaştırın</div>
    
    <canvas id="canvas"></canvas>
    
    <div class="result" id="result" style="display: none;">
        <div class="result-text" id="resultText"></div>
        <div class="countdown" id="countdown"></div>
    </div>
    
    <script>
        const video = document.createElement('video');
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d', { willReadFrequently: true });
        const resultDiv = document.getElementById('result');
        const resultText = document.getElementById('resultText');
        const countdown = document.getElementById('countdown');
        
        let scanned = false;
        let countdownNum = 0;
        
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        
        // Kamerayı başlat
        navigator.mediaDevices.getUserMedia({ 
            video: { facingMode: 'environment', width: { ideal: 1280 }, height: { ideal: 720 } }
        }).then(stream => {
            video.srcObject = stream;
            video.onloadedmetadata = () => {
                video.play();
                scanQR();
            };
        }).catch(err => {
            resultDiv.style.display = 'flex';
            resultDiv.classList.remove('success');
            resultText.textContent = '❌ Kamera erişimi başarısız';
            countdown.textContent = err.message;
        });
        
        function scanQR() {
            if (video.readyState === video.HAVE_ENOUGH_DATA) {
                ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
                
                try {
                    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
                    const code = jsQR(imageData.data, imageData.width, imageData.height);
                    
                    if (code && !scanned) {
                        const qrValue = code.data;
                        scanned = true;
                        
                        // QR kodunu sunucuya gönder
                        fetch(`/qr?id=${encodeURIComponent(qrValue)}`)
                            .then(res => res.text())
                            .then(data => {
                                resultDiv.classList.add('success');
                                resultDiv.style.display = 'flex';
                                resultText.textContent = '✅ ' + data;
                                
                                countdownNum = 3;
                                updateCountdown();
                            })
                            .catch(err => {
                                resultDiv.classList.remove('success');
                                resultDiv.style.display = 'flex';
                                resultText.textContent = '❌ Hata';
                                countdown.textContent = err.message;
                                countdownNum = 3;
                                updateCountdown();
                            });
                    }
                } catch (e) {
                    // QR scan hatası, devam et
                }
            }
            
            requestAnimationFrame(scanQR);
        }
        
        function updateCountdown() {
            countdown.textContent = `${countdownNum} saniye sonra yeniden taranacak...`;
            countdownNum--;
            
            if (countdownNum < 0) {
                scanned = false;
                resultDiv.style.display = 'none';
                resultDiv.classList.remove('success');
            } else {
                setTimeout(updateCountdown, 1000);
            }
        }
        
        function goHome() {
            window.location.href = '/';
        }
        
        window.addEventListener('resize', () => {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        });
    </script>
</body>
</html>
"""

# ✅ ANA SAYFA
@app.route("/")
def home():
    return render_template_string(HOME_PAGE)


# ✅ QR ÜRETICI ARAYÜZÜ
@app.route("/qr_generator")
def qr_generator():
    return render_template_string(QR_GENERATOR_HTML)


# ✅ MOBIL HIZLI TARA
@app.route("/scan")
def scan():
    return render_template_string(SCAN_PAGE)


# ✅ TEK QR KOD OLUŞTUR
@app.route("/generate_qr")
def generate_qr():
    qr_id = request.args.get("id", "bilinmiyor")
    qr_value = request.args.get("value", qr_id)
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_value)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    img_io = BytesIO()
    img.save(img_io, "PNG")
    img_io.seek(0)
    
    return send_file(img_io, mimetype="image/png")


# ✅ TOPLU QR KOD OLUŞTUR (ZIP)
@app.route("/generate_qr_batch")
def generate_qr_batch():
    import zipfile
    
    base_name = request.args.get("base", "QR")
    start = int(request.args.get("start", 1))
    end = int(request.args.get("end", 10))
    
    zip_io = BytesIO()
    
    with zipfile.ZipFile(zip_io, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for i in range(start, end + 1):
            qr_id = f"{base_name}-{i}"
            
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(qr_id)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            
            img_io = BytesIO()
            img.save(img_io, "PNG")
            img_io.seek(0)
            
            zip_file.writestr(f"{qr_id}.png", img_io.getvalue())
    
    zip_io.seek(0)
    return send_file(zip_io, mimetype="application/zip", as_attachment=True, download_name=f"{base_name}_QR_Kodlari.zip")


# ✅ QR okutma → log kaydet
@app.route("/qr")
def qr():
    qr_id = request.args.get("id", "bilinmiyor")
    ip = request.remote_addr
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([qr_id, time_now, ip])

    return f"{qr_id} okundu ✅"


# ✅ RAPOR GÖNDERME (QR ile tetiklenen)
@app.route("/rapor_mail")
def rapor_mail():
    try:
        rows = []
        with open(LOG_FILE, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                rows.append(row)

        # HTML rapor hazırla
        html = "<h3>Günlük QR Devriye Raporu</h3><table border=1>"
        html += "<tr><th>QR</th><th>Saat</th><th>IP</th></tr>"

        for row in rows:
            html += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td></tr>"

        html += "</table>"

        # RESEND API
        url = "https://api.resend.com/emails"

        data = {
            "from": "onboarding@resend.dev",
            "to": [EMAIL_TO],
            "subject": "Günlük QR Devriye Raporu",
            "html": html
        }

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=data, headers=headers)

        print("MAIL STATUS:", response.status_code)
        print("MAIL RESPONSE:", response.text)

        return "Rapor gönderildi ✅"

    except Exception as e:
        return f"Hata: {str(e)}"


# ✅ RAPORU TARAYICIYA BAS
@app.route("/rapor")
def rapor():
    html = """
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>QR Okuma Raporu</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            .container {
                background: white;
                border-radius: 15px;
                padding: 30px;
                max-width: 800px;
                margin: 0 auto;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            }
            h2 {
                color: #333;
                margin-bottom: 20px;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 20px;
            }
            th, td {
                padding: 12px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }
            th {
                background: #f5f5f5;
                font-weight: 600;
                color: #333;
            }
            tr:hover {
                background: #f9f9f9;
            }
            .button-group {
                display: flex;
                gap: 10px;
                margin-top: 20px;
            }
            button {
                padding: 10px 20px;
                border: none;
                border-radius: 8px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
            }
            .btn-home {
                background: #667eea;
                color: white;
            }
            .btn-home:hover {
                background: #764ba2;
            }
            .btn-mail {
                background: #4CAF50;
                color: white;
            }
            .btn-mail:hover {
                background: #45a049;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>📊 QR Okuma Raporu</h2>
            <table border=1>
                <tr><th>QR</th><th>Saat</th><th>IP</th></tr>
    """
    
    try:
        with open(LOG_FILE, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 3:
                    html += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td></tr>"
    except:
        html += "<tr><td colspan=3>Kayıt yok</td></tr>"

    html += """
            </table>
            <div class="button-group">
                <button class="btn-home" onclick="window.location.href='/'">← Ana Sayfa</button>
                <button class="btn-mail" onclick="window.location.href='/rapor_mail'">📧 Mail Gönder</button>
            </div>
        </div>
    </body>
    </html>
    """
    return html


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
