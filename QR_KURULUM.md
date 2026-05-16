# QR Kod Devriye Sistemi - Kurulum Kılavuzu

## 📋 Gereksinimler

```bash
pip install flask qrcode[pil] requests
```

## 🚀 Kullanım

### Seçenek 1: Yeni Dosya Kullanma (Önerilen)
```bash
python qr_app.py
```

Tarayıcıda açın: `http://localhost:5000`

### Seçenek 2: Mevcut app.py'yi Güncelleme
Orijinal `app.py` dosyasını yedekleyin, ardından `qr_app.py` içeriğini `app.py` üzerine kopyalayın.

## 📱 Özellikler

### 1. **QR Kod Üretici Arayüzü** (`/qr_generator`)
- ✅ Güzel ve responsive tasarım
- ✅ Tek QR kod oluştur ve indir
- ✅ Toplu QR kodlar oluştur (ZIP olarak)
- ✅ Yazdırma desteği
- ✅ PNG indirme

### 2. **Tek QR Kod Oluştur**
- QR ID/Adını gir (Örn: Depo-1, Giriş)
- İçerik belirle (opsiyonel)
- "QR Kod Oluştur" butonu
- İndir veya Yazdır

### 3. **Toplu QR Kod Oluştur**
- Taban adı gir (Örn: Depo)
- Başlangıç ve bitiş numarası belirle
- Tek tıkla tüm QR kodları ZIP olarak indir
- Örn: Depo-1.png, Depo-2.png ... Depo-10.png

### 4. **API Endpoints**

#### QR Kod Oluştur
```
GET /generate_qr?id=Depo-1&value=https://sistem.local/qr?id=Depo-1
```
PNG görseli döner

#### Toplu Oluştur
```
GET /generate_qr_batch?base=Depo&start=1&end=10
```
ZIP dosyası döner

#### Okuma Raporu
```
GET /rapor
```
Tarayıcıda HTML tablosu gösterir

#### Mail Gönder
```
GET /rapor_mail
```
E-mail ile rapor gönderir

## 🎯 Kullanım Senaryoları

### Senaryo 1: Tek Nokta için QR Kod
1. `/qr_generator` sayfasına git
2. "Depo-1" yazarak QR kod oluştur
3. Yazdır, kemerle yapıştır

### Senaryo 2: Bütün Binaya 20 Nokta
1. "Toplu Oluştur" sekmesine tıkla
2. "Bina" yazarak, 1-20 gir
3. ZIP indir
4. 20 QR kodunu başarıyla yazdır

### Senaryo 3: Web'den Okuma
1. QR kod tarama cihazında şu URL kullan: `http://localhost:5000/qr?id=Depo-1`
2. Her tarama otomatik log.csv'ye kaydedilir
3. `/rapor` ile görüntüle

### Senaryo 4: Mail Rapor
1. Devriye tamamlandıktan sonra `/rapor_mail` ziyaret et
2. Raporla mail otomatik gönderilir

## 🔧 Ayarlamalar

### API Key Değiştir
Dosyada şu satırı düzenle:
```python
API_KEY = "sizin_resend_api_key"
EMAIL_TO = "alici@email.com"
```

### QR Kod Boyutu
```python
qr = qrcode.QRCode(
    version=1,              # Boyut (1-40, daha büyük = daha kapasiteli)
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,            # Pixel boyutu
    border=4,               # Beyaz çerçeve
)
```

## 📊 Log Dosyası Yapısı

`log.csv`:
```
QR_ID,Saat,IP
Depo-1,2024-01-15 09:30:45,192.168.1.100
Depo-2,2024-01-15 09:35:12,192.168.1.101
```

## 🎨 İstediğin Şekilde Özelleştir

- **Renk değiştir**: CSS'teki `#667eea` ve `#764ba2` değerlerini kendi renklerinle değiştir
- **Logo ekle**: HTML'e şu satırı ekle:
  ```html
  <img src="logo.png" style="max-width: 200px; margin-bottom: 20px;">
  ```
- **Kısayol**: `Depo-1` yazarken otomatik QR URL'si: `/qr?id=Depo-1`

## 🚨 Sorun Giderme

**ModuleNotFoundError: No module named 'qrcode'**
```bash
pip install qrcode[pil]
```

**Port 5000 zaten kullanımda**
```bash
python qr_app.py
# Veya farklı port:
PORT=8000 python qr_app.py
```

**ZIP dosyası açılmıyor**
- İşletim sisteminizin ZIP desteğini kontrol et
- Python 3.7+ kullandığından emin ol

---

**Sorularınız mı var?** Dosya içindeki kodları istediğin gibi düzenleyebilirsin! 🚀
