# 🔐 2 GITHUB HESABI İLE RAILWAY - SEÇIM REHBERİ

2 GitHub hesabın varsa, hangisini kullanacağını seçebilirsin! Detaylı açıklama:

---

## 📋 SENARYO

```
GitHub Hesap 1: cmaks (Kişisel)
GitHub Hesap 2: cmaks-work (İş)

Railway: Hangisine bağlanacak?
```

**Cevap: Sende karar! İstediğin hesabı seç!**

---

## 🎯 SEÇIM REHBERI

### Seçenek 1: Kişisel GitHub (cmaks)
```bash
railway login
# Tarayıcı açılır → GitHub Sign in
# cmaks (Kişisel) ile giriş yap
# Authorize Railway ✅

# Artık Railway cmaks hesabına bağlı
# - Repository cmaks altında oluşturulur
# - Deployments cmaks'ın profili altında
```

### Seçenek 2: İş GitHub (cmaks-work)
```bash
railway login
# Tarayıcı açılır → GitHub Sign in
# cmaks-work (İş) ile giriş yap
# Authorize Railway ✅

# Artık Railway cmaks-work'e bağlı
# - Repository cmaks-work altında oluşturulur
# - Deployments cmaks-work'ün profili altında
```

---

## 🔄 SONRA DEĞİŞTİREBİLİR MİSİN?

### EVET! İstediğin zaman değiştirebilirsin:

```bash
# 1. Logout yap
railway logout

# 2. Diğer hesapla login yap
railway login

# 3. Yeni hesapla authorize et
# İşte! Artık diğer hesaba bağlı
```

---

## ✅ KARŞILAŞTIRMA TABLOSU

| Kriter | GitHub 1 (cmaks) | GitHub 2 (cmaks-work) |
|--------|------------------|----------------------|
| **Bağlı Olacak** | Railway → cmaks | Railway → cmaks-work |
| **Repo Yeri** | github.com/cmaks/qr-devriye | github.com/cmaks-work/qr-devriye |
| **Kimin İçinde** | Kişisel profilde | İş profilde |
| **Log-in şekli** | `railway login` → cmaks seç | `railway login` → cmaks-work seç |

---

## 🚀 BAĞLAMA ADIMLARI (Seçimli)

### ADIM 1: Hangisini kullanacağını belirle
```
İşletme ile ilişkili = cmaks-work (İş)
Kişisel proje = cmaks (Kişisel)
```

### ADIM 2: Railway'e giriş
```bash
railway login
```

### ADIM 3: Tarayıcıda GitHub seç
```
Tarayıcı açılır
↓
"Sign in with GitHub" tıkla
↓
GitHub Sign in sayfası
↓
İLK AYARLADIĞIN HESAPLA GIRIŞ YAP!
(Önemli: Eğer başka hesapla değilse çık, diğer hesapla gir)
```

### ADIM 4: Authorize Railway
```
Railway'e bu hesabı kullanmayı onaylayan mesaj gelir
"Authorize railway-app" tıkla
↓
✅ Bağlı!
```

### ADIM 5: Railway config kontrol et
```bash
railway whoami
# Çıktı: 
# Email: cmaks@example.com (Hangisi olmuş, görürsün)
```

---

## 💡 ÖNERİ

### Eğer İşletme Projesi İse:
```
GitHub Hesap: cmaks-work (İş)
Railway: cmaks-work'e bağla

Avantaj:
- İş hesabında organize olur
- İş proje dosyaları iş hesabında
- Kişisel ve iş ayrı kalır
```

### Eğer Kişisel Proje İse:
```
GitHub Hesap: cmaks (Kişisel)
Railway: cmaks'a bağla

Avantaj:
- Kişisel projelerin aynı yerde
- Yönetmesi daha kolay
```

---

## 🔄 MİD-DEPLOYMENT DEĞİŞTİRİRSEM NE OLUR?

### Değiştirme (Logout → Yeni hesap):
```bash
railway logout
railway login  # Diğer hesapla
```

**Sonuç:**
- ❌ Eski deployment silinmez
- ✅ Yeni projeler yeni hesapla oluşturulur
- ℹ️ Eski proje eski hesapta kalır

---

## ⚠️ ÖNEMLI NOTLAR

### 1. GitHub'da Aynı Anda 2 Hesap Açamazsın
```
Tarayıcıda 1 GitHub hesabı açıksa, 2. ile login yapmak için:
- ÇIKIŞ YAP (sign out) ilkinden
- SONRA 2. ile gir

VEYA

- Gizli pencere aç (Incognito)
- 2. hesapla gir
```

### 2. Railway Bir Hesaba Bir Defada Bağlanır
```
Email: cmaks@example.com → GitHub: cmaks
Email: cmaks-work@example.com → GitHub: cmaks-work
```

### 3. 2 Ayrı Bilgisayarda Farklı Hesap Kullanabilir
```
Bilgisayar 1: cmaks ile gir
Bilgisayar 2: cmaks-work ile gir
İkisi birbirini etkilemez
```

---

## 🎯 ADIM ADIM ÖRNEK (cmaks-work SEÇTIM)

```bash
# 1. Railway login
railway login

# 2. Tarayıcı açılır → GitHub yönlendir
# Tarayıcı: https://github.com/login
#   → Username: cmaks-work
#   → Password: ****
#   → Sign in

# 3. Railway authorize istiyor
# "Authorize railway-app" → Confirm password

# 4. ✅ Bağlı!
railway whoami
# Email: cmaks-work@example.com
# GitHub: cmaks-work

# 5. Deploy et
railway init
# Proje adı: qr-devriye
# 📝 Repository: github.com/cmaks-work/qr-devriye

railway up
# Deploy başlı!
```

---

## 🔍 KONTROL ET

Deploy sonrası hangi hesaba bağlı olduğunu kontrol et:

```bash
# Terminal'de
railway whoami

# Çıktı (Örnek):
# Email: cmaks-work@example.com
# GitHub Org: cmaks-work
```

Eğer yanlışsa:
```bash
railway logout
railway login  # Diğer hesapla gir
```

---

## 📱 TELEFONDAN BAKABILIR MİSİN?

```
Railway.app → Dashboard
↓
Hangi hesapla login ettiysen, o görünür
↓
cmaks-work hesabı giriş yapmışsan:
   ↓
   github.com/cmaks-work altında proje
   ↓
   cmaks-work'ün deployments, logs, settings

cmaks hesabı giriş yapmışsan:
   ↓
   github.com/cmaks altında proje
   ↓
   cmaks'ın deployments, logs, settings
```

---

## ✅ KONTROL LİSTESİ

- [ ] Hangi GitHub hesabını kullanacağına karar verdin
- [ ] `railway login` çalıştırılır
- [ ] Tarayıcıda **o hesapla** GitHub'a giriş yap
- [ ] Railway authorize et
- [ ] `railway whoami` ile kontrol et (doğru hesap mı?)
- [ ] `railway init` çalıştır
- [ ] Proje adını gir
- [ ] `railway up` başlat
- [ ] Deploy başarılı ✅

---

## 🎯 ÖZETİ

```
railway login
    ↓
Tarayıcı aç → GitHub
    ↓
1. HESAP SEÇ (cmaks veya cmaks-work)
    ↓
Authorize Railway
    ↓
✅ O HESABA BAĞLANDI!
    ↓
railway init → railway up
    ↓
✅ Deploy o hesaptan!
```

---

## 💬 SORU: İkisini Aynı Anda Kullana Bilir Miyim?

**EVET!** 2 Farklı yoldan:

### Yol 1: 2 Bilgisayar Kullan
```
Bilgisayar 1: railway login (cmaks)
Bilgisayar 2: railway login (cmaks-work)
```

### Yol 2: Docker Container'lar
```
Container 1: cmaks project
Container 2: cmaks-work project
```

### Yol 3: Workspace (İleri)
```
Railway orgs kullan
```

Ama **şimdilik biri yeterli!** 🚀

---

## 🚀 ŞİMDİ BAŞLAMAYA HAZIR!

Hangisini seçtin?
- **cmaks (Kişisel)** ← Seçim 1
- **cmaks-work (İş)** ← Seçim 2

Sonra `railway login` yap ve **o hesapla** gir!

**Kolay gelsin!** 🎉

Soru olursa yaz! 💬
