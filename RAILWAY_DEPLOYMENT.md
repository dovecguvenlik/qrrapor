# 🚀 RAILWAY.APP DEPLOYMENT - FIREWALL SORUNU ÇÖZÜMÜ

Railway.app kullanarak firewall'dan kurtulacağız! ☁️

---

## ✅ ADIM 1: RAILWAY HESABI OLUŞTUR (2 dakika)

### Seçenek A: GitHub ile Giriş (Önerilen)
1. https://railway.app açıp **Sign in** tıkla
2. **Continue with GitHub** seç
3. GitHub hesabını bağla (hiç yoksa https://github.com/signup)

### Seçenek B: Google ile Giriş
1. https://railway.app açıp **Sign in** tıkla
2. **Continue with Google** seç
3. Google hesabını seç

---

## ✅ ADIM 2: PROJE OLUŞTUR (1 dakika)

1. Railway.app ana sayfada **Create New Project** tıkla
2. **Deploy from GitHub repo** seç
3. Repo seçme (ilk başta yoksa skip et)
4. Manual deployment yapacağız

---

## ✅ ADIM 3: DOSYALARI HAZIRLA

3 dosya gerekli:

### 1️⃣ **app.py** (Ana uygulama)
```python
# Zaten hazırladığım dosya
# PORT = os.environ.get("PORT", 5000) kullanıyor (Railway'in port'u alıyor)
```

### 2️⃣ **requirements.txt** (Paketler)
```
Flask==2.3.2
qrcode[pil]==7.4.2
requests==2.31.0
Pillow==10.0.0
```

### 3️⃣ **Procfile** (Railway'e nasıl başlatacağını söyle)
Yeni dosya oluştur:
```
web: python app.py
```

---

## ✅ ADIM 4: RAILWAY DEPLOY ETME (5 dakika)

### A. Git Repository Oluştur

**Windows/Mac/Linux:**
```bash
# Proje klasöründe:
git init
git add .
git commit -m "Initial commit"
```

### B. Railway CLI İndir
https://docs.railway.app/cli/install

**Windows (PowerShell):**
```bash
iwr https://railway.app/install.ps1 -useb | iex
```

**Mac/Linux:**
```bash
curl -fsSL https://railway.app/install.sh | sh
```

### C. Railway'e Giriş
```bash
railway login
```
Tarayıcı açılacak, GitHub seç ve authorize et.

### D. Proje Başlat
```bash
railway init
```
- Proje adı sor: **qr-devriye** yaz
- **Empty Project** seç

### E. Deploy Et
```bash
railway up
```

**Bitti!** 🎉

---

## 🌐 SONUÇ: AÇIK URL

Deploy başarılı olunca şöyle bir bağlantı alacaksın:

```
https://qr-devriye-production.up.railway.app
```

Telefondan URL:
```
https://qr-devriye-production.up.railway.app/
```

**Başka ne yapmana gerek yok! Firewall sorguda yok!** ☁️

---

## 📱 TELEFONDAN KULLANMA

### 1. Bilgisayardan hiçbir şey çalıştırmaya gerek YOK!

### 2. Telefonda tarayıcı açıp yazıp ENTER:
```
https://qr-devriye-production.up.railway.app
```

### 3. Ana sayfa açılacak:
```
📱 QR Devriye
├─ 📝 QR Kod Oluştur
├─ 📊 Raporları Görüntüle
└─ 📷 Hızlı Tara
```

### 4. Kalan tüm işlemler aynı! ✅
- QR oluştur
- Tara
- Rapor gör

---

## 💾 LOG DOSYASI SORUNU

⚠️ **Önemli:** Railway free tier'inda log.csv kalıcı değil (her restart'ta silinir)

### Çözüm 1: PostgreSQL Veritabanı Ekle (Önerilen)
```bash
railway add
# Postgre SQL seç
```

Daha sonra app.py'yi düzenleyip PostgreSQL kullan.

### Çözüm 2: Şimdilik Yeterli
- İşletme süresi boyunca log tutulur
- Restart'ta yeni log başlanır
- Yeterli ise bu şekilde devam et

### Çözüm 3: S3 ya da Firebase
Bulut depolama ekle (ücretli olabilir)

---

## 🔧 SORUN GIDERME

### "railway command not found"
```bash
# PATH'i güncelle veya direkt çalıştır:
./node_modules/.bin/railway login
```

### "Deployment başarısız oldu"
```bash
# Log'ları kontrol et:
railway logs
```

### "500 error alıyorum"
```bash
railway logs
# Hata mesajını kopyala ve bak
```

### "Email göndermede hata"
```python
# API_KEY kontrol et: qr_app_mobile.py
API_KEY = "re_..."  # Doğru mu?
EMAIL_TO = "..."    # Doğru mail mi?
```

---

## 📊 ÜCRETLENDİRME

Railway **free tier:**
- ✅ 5$ aylık kredi (ilk ay bedava)
- ✅ Sınırsız sayıda proje
- ✅ 100GB bandwidth
- ✅ PostgreSQL veritabanı
- ✅ Redis cache

Çoğu devriye sistemi bu kredi içinde çalışır!

---

## 🌍 KENDİ DOMAIN BAĞLAMA (İsteğe Bağlı)

Railway URL'si yerine kendi domain'ini kullanmak istiyorsan:

1. Railway > Settings > Domain
2. **Add Domain** tıkla
3. **devriye.yoursite.com** yaz
4. CNAME records'u güncelle (Domain provider'dan)

---

## 📈 İLERİ: GEREKTİĞİNDE VERİTABANI EKLE

```bash
railway add
```
- PostgreSQL seç
- App.py'yi güncelleyelim

```python
import psycopg2
from psycopg2 import sql

# Veritabanı bağlantısı
DATABASE_URL = os.environ.get("DATABASE_URL")
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

# Tablo oluştur (ilk çalıştırmada)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS qr_logs (
        id SERIAL PRIMARY KEY,
        qr_id VARCHAR(255),
        scanned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        ip_address VARCHAR(50)
    )
""")
conn.commit()

# Tarama kaydet
@app.route("/qr")
def qr():
    qr_id = request.args.get("id", "bilinmiyor")
    ip = request.remote_addr
    cursor.execute(
        "INSERT INTO qr_logs (qr_id, ip_address) VALUES (%s, %s)",
        (qr_id, ip)
    )
    conn.commit()
    return f"{qr_id} okundu ✅"
```

Ama şimdilik **CSV yeterli!** 📝

---

## ✅ KONTROL LİSTESİ

- [ ] Railway hesabı oluşturuldu
- [ ] app.py dosyası hazır
- [ ] requirements.txt hazır
- [ ] Procfile oluşturuldu
- [ ] Git repo başlatıldı (`git init`)
- [ ] Railway CLI kuruldu
- [ ] `railway login` çalıştırıldı
- [ ] `railway init` çalıştırıldı
- [ ] `railway up` başarılı oldu
- [ ] URL alındı
- [ ] Telefondan URL'ye erişim başarılı
- [ ] QR tarama çalışıyor ✅

---

## 🎯 SONUÇ

```
❌ ESKI: python qr_app_mobile.py + localhost + Firewall sorunu
✅ YENİ: https://qr-devriye-production.up.railway.app + Herkes erişebilir
```

**Hepsi bitti! Firewall artık sorun değil!** 🚀

---

## 📞 RAILWAY DESTEK

- https://docs.railway.app
- https://railway.app/docs
- Discord: https://discord.gg/railway

İhtiyaçlarına göre [railway-deployment.md](railway-deployment.md) yazabilirim! 📖
