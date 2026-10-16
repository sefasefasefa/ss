# iPhone (iOS) Projesi

Bu proje **iPhone (iOS)** için otomatik olarak oluşturulmuştur.

## 🎯 Özellikler
- ✅ Arayüz: Logo
- ✅ Arayüz: Ana sayfa
- ✅ Arayüz: Menü
- ✅ API
- ✅ Veritabanı

## 📦 Kurulum

```bash
pip install -r requirements.txt
```

## iPhone'a derleme ve yükleme (Windows'tan)

Bu proje Kivy kullanır. iOS uygulamasını Windows üzerinde doğrudan derlemek mümkün değildir; derleme GitHub Actions'ın macOS makinesinde yapılır. Bu depo için `.github/workflows/ios-build.yml` iş akışı, imzasız bir IPA oluşturur. Apple Developer Program hesabı gerektirmez; ancak IPA'yı iPhone'a yüklemek için Windows'ta Sideloadly gibi bir yan yükleme aracıyla Apple hesabınız kullanılarak imzalanması gerekir. Ücretsiz Apple hesabıyla yüklenen uygulamaların imzası genellikle 7 gün sonra yenilenmelidir.

1. Bu klasörün içeriğini **özel (private) bir GitHub deposuna** yükleyin. Apple hesabı parolası veya sertifika dosyası depoya eklemeyin.
2. GitHub deposunda **Actions** sekmesini açın. İlk kez sorulursa GitHub Actions iş akışlarını etkinleştirin.
3. `Build unsigned iOS IPA` iş akışını seçip **Run workflow** ile çalıştırın. Ana dala gönderim de derlemeyi otomatik başlatır.
4. Başarılı çalışmanın **Artifacts** bölümünden `ZONE-unsigned-ipa` dosyasını indirin ve ZIP dosyasını çıkartın.
5. Windows'ta Sideloadly'yi açın, iPhone'u USB ile bağlayın, IPA dosyasını seçin ve kendi Apple hesabınızla cihaza yükleyin. Apple hesabı bilgilerinizi yalnızca kullandığınız imzalama aracına girin; GitHub deposuna veya iş akışına eklemeyin.

Bu iş akışı derleme/paketleme yapar; Apple tarafından imzalanmış dağıtım paketi veya App Store/TestFlight yüklemesi üretmez. Üretilen IPA'nın ilk gerçek cihaz testi başarılı olduktan sonra arayüz, dokunmatik davranış ve ağ bağlantısını iPhone'da ayrıca kontrol edin.

## 🚀 Çalıştırma

### Yöntem 1: start.bat ile
1. **start.bat** dosyasını çift tıklayarak projeyi başlatabilirsiniz.

### Yöntem 2: Komut satırından
```bash
python main.py
```

## 🌐 API Kullanımı

Projede ortak API yapısı bulunmaktadır. Tüm platformlarda aynı API istemcisini kullanabilirsiniz.

### API İstemcisi

```python
from api.api_client import APIClient
from api.api_config import APIConfig

# API istemcisi oluştur
client = APIClient()
config = APIConfig()

# GET isteği
users = client.get(config.get_endpoint('users'))

# Login işlemi
login_response = client.post(config.get_endpoint('login'), {
    'username': 'admin',
    'password': 'admin'
})
```

### 📡 API Endpoint'leri

| Endpoint | Açıklama | Method |
|----------|----------|--------|
| `/api/auth/login` | Kullanıcı giriş | POST |
| `/api/auth/register` | Kullanıcı kayıt | POST |
| `/api/users` | Kullanıcı listele | GET |

Proje içinde `api/server.py` dosyasıyla seçilen giriş yöntemlerine göre SQLite kullanan bir doğrulama API'si oluşturulur. `start.bat` API'yi uygulamayla birlikte başlatır; `api/start_server.bat` sunucuyu ayrı başlatır. İlk çalıştırmadan önce `py -3 -m pip install -r api/server_requirements.txt` komutunu çalıştırın. API adresi `auth_settings.py` içindeki `API_BASE_URL` veya `API_BASE_URL` ortam değişkeniyle değiştirilebilir. Mobil cihazda `127.0.0.1` cihazın kendisi olduğundan, API'yi erişilebilir bir HTTPS sunucusunda yayınlayıp bu adresi güncelleyin.

## 🗃️ Veritabanı

Her projeye SQLite veritabanı otomatik eklenir ve uygulama başlarken başlatılır. Şema seçilen özelliklere göre oluşturulur; Login Sistemi kullanıcı tablolarını, e-posta girişi doğrulama kodlarını, ana sayfa kartları ise içerik tablosunu ekler. Veritabanı varsayılan olarak kullanıcı dizininde uygulama adına özel tutulur; `APP_DATABASE_PATH` ile değiştirilebilir.

### Kullanım

```python
from database.db_helper import DatabaseHelper

db = DatabaseHelper()
record_id = db.add_record('note', '{"text": "Merhaba"}')
records = db.get_records('note')
```

---

📝 **Not:** Bu proje otomatik olarak oluşturulmuştur.
Gerekli kütüphaneler `requirements.txt` dosyasında belirtilmiştir.

## Ana Sayfa Arayüzü

Uygulama adı ve üst çubuk logosu düzenleyiciden değiştirilebilir; logo metin/emoji veya PNG/JPG/GIF/BMP görseli olabilir. Ana sayfa başlığı, açıklaması ve içerik kartları; logo, footer ve soldan açılan hamburger menüsü oluşturucu ekranından seçilip düzenlenebilir. Menü öğelerinin adı, işlemi, mesajı, 1 tabanlı satır/sütun konumu ve dp cinsinden genişlik/yüksekliği düzenlenebilir. Menü içeriği `auth_settings.py` içindeki `MENU_ITEMS` ayarında tutulur; ana sayfa içeriği `auth_settings.py` içindeki `HOME_CONFIG` ayarında tutulur. Arayüz, yoğunluktan bağımsız dp/sp ölçüleri, ekran genişliğine göre değişen kart düzeni ve küçük ekranlarda kaydırılabilen içerik kullanır.

## Düğme Stili

Oluşturucu üzerinden ayarlanan arka plan/yazı renkleri ve temel px boyutları `auth_settings.py` içindeki `BUTTON_STYLE` değerinde saklanır ve uygulamadaki düğmelere uygulanır.
# ss
