# 📝 FastAPI Todo App

Kimlik doğrulama, rol tabanlı yetkilendirme ve sunucu taraflı (Jinja2) arayüzü olan tam kapsamlı bir **Todo** uygulaması. Backend, FastAPI + SQLAlchemy + PostgreSQL üzerine kurulu; kimlik doğrulama JWT ile sağlanıyor, şema değişiklikleri Alembic ile yönetiliyor ve endpoint'ler pytest ile test ediliyor.

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.139-009688?logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-CC2927)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-supported-336791?logo=postgresql&logoColor=white)
![JWT](https://img.shields.io/badge/Auth-JWT-000000?logo=jsonwebtokens&logoColor=white)
![Pytest](https://img.shields.io/badge/tests-pytest-0A9EDC?logo=pytest&logoColor=white)

---

## İçindekiler

- [Özellikler](#-özellikler)
- [Mimari](#-mimari)
- [Teknoloji Yığını](#-teknoloji-yığını)
- [Proje Yapısı](#-proje-yapısı)
- [Kurulum](#-kurulum)
- [Ortam Değişkenleri](#-ortam-değişkenleri)
- [Veritabanı Migrasyonları](#-veritabanı-migrasyonları-alembic)
- [API Uç Noktaları](#-api-uç-noktaları)
- [Kimlik Doğrulama Akışı](#-kimlik-doğrulama-akışı)
- [Testler](#-testler)
- [Geliştirilebilecek Noktalar](#-geliştirilebilecek-noktalar)
- [Lisans](#-lisans)

---

## ✨ Özellikler

- **Kullanıcı kaydı & girişi** — bcrypt ile şifre hash'leme, JWT (`python-jose`) ile oturum yönetimi.
- **Rol tabanlı yetkilendirme** — `user` ve `admin` rolleri; admin'e özel uç noktalar korunuyor.
- **Todo CRUD** — her kullanıcı sadece kendi todo'larını görür/düzenler/siler; admin tüm todo'ları yönetebilir.
- **Sunucu taraflı arayüz** — Jinja2 + Bootstrap ile render edilen login/register/todo sayfaları, aynı router'lar üzerinden hem HTML hem JSON döndürülüyor.
- **Cookie tabanlı sayfa oturumu, Bearer token tabanlı API** — tarayıcı sayfaları `access_token` cookie'sini, `fetch` çağrıları `Authorization: Bearer` header'ını kullanıyor.
- **Şema versiyonlama** — Alembic ile veritabanı migrasyonları (örn. `users` tablosuna `phone_number` eklenmesi).
- **Otomatik test paketi** — pytest + bağımsız SQLite test veritabanı + dependency override'ları ile auth/todos/admin/users uç noktaları test ediliyor.

## 🏗 Mimari

Proje, sorumlulukların router bazında ayrıldığı katmanlı bir yapı izliyor:

```mermaid
flowchart LR
    subgraph Client["İstemci"]
        Browser["Tarayıcı (Jinja2 sayfaları)"]
        API["API İstemcisi (fetch / JS)"]
    end

    subgraph App["FastAPI Uygulaması (main.py)"]
        Auth["routers/auth.py<br/>kayıt · login · JWT üretimi"]
        Todos["routers/todos.py<br/>todo CRUD · sayfa render"]
        Admin["routers/admin.py<br/>admin CRUD (role check)"]
        Users["routers/users.py<br/>profil · şifre/telefon"]
    end

    ORM["models.py + database.py<br/>SQLAlchemy Session"]
    DB[("PostgreSQL")]
    Alembic["Alembic<br/>şema migrasyonları"]

    Browser -- "cookie: access_token" --> Todos
    API -- "Authorization: Bearer <jwt>" --> Todos
    API --> Auth
    API --> Admin
    API --> Users

    Auth -- "JWT doğrula (get_current_user)" --> Todos
    Auth -- "JWT doğrula" --> Admin
    Auth -- "JWT doğrula" --> Users

    Auth --> ORM
    Todos --> ORM
    Admin --> ORM
    Users --> ORM
    ORM --> DB
    Alembic -.-> DB
```

**Temel prensipler:**

- **Router bazlı ayrım** — `auth`, `todos`, `admin`, `users` router'ları kendi `prefix` ve `tags` değerleriyle `main.py` içinde birleştiriliyor; her biri kendi Pydantic şemalarını ve DB bağımlılığını taşıyor.
- **Tek noktadan kimlik doğrulama** — `auth.py` içindeki `get_current_user` bağımlılığı JWT'yi çözüp `{username, id, user_role}` döndürüyor; diğer router'lar bunu `Depends()` ile tekrar kullanıyor (DRY).
- **Hibrit uç noktalar** — `todos.py` içindeki `*-page` uç noktaları (`/todo-page`, `/add-todo-page`, `/edit-todo-page/{id}`) HTML sayfası render ederken, aynı router'daki `/`, `/todo`, `/todo/{id}` uç noktaları saf JSON REST API olarak çalışıyor; sayfa tarafı `base.js` üzerinden bu API'lere `fetch` ile istek atıyor.
- **Rol tabanlı erişim kontrolü** — `admin.py` içindeki her uç nokta `user.get('user_role') != 'admin'` kontrolüyle korunuyor.
- **Bağımlılık enjeksiyonu ile DB oturumu** — her router kendi `get_db()` generator'ını tanımlayıp `Annotated[Session, Depends(get_db)]` ile istek başına kısa ömürlü bir SQLAlchemy oturumu sağlıyor.
- **Şema evrimi Alembic ile** — model değişiklikleri (`models.py`) migration dosyaları (`alembic/versions/`) üzerinden veritabanına uygulanıyor.

## 🧰 Teknoloji Yığını

| Katman | Teknoloji |
|---|---|
| Web çatısı | [FastAPI](https://fastapi.tiangolo.com/) 0.139, [Starlette](https://www.starlette.io/), [Uvicorn](https://www.uvicorn.org/) |
| ORM / Veritabanı | [SQLAlchemy](https://www.sqlalchemy.org/) 2.0, PostgreSQL (`psycopg2-binary`), test ortamında SQLite |
| Şema migrasyonu | [Alembic](https://alembic.sqlalchemy.org/) |
| Kimlik doğrulama | JWT (`python-jose`), `passlib` + `bcrypt`, `OAuth2PasswordBearer` |
| Doğrulama / Şema | [Pydantic](https://docs.pydantic.dev/) v2, `email-validator` |
| Arayüz (SSR) | [Jinja2](https://jinja.palletsprojects.com/) şablonları, Bootstrap, jQuery |
| Test | `pytest`, `pytest-asyncio`, `httpx` (FastAPI `TestClient`) |
| Yapılandırma | `python-dotenv` (`.env` → `SECRET_KEY`) |

## 📁 Proje Yapısı

```
FastAPI-TodoApp/
├── TodoApp/
│   ├── alembic/                # Veritabanı migrasyon ortamı
│   │   ├── versions/           # Migration script'leri
│   │   └── env.py
│   ├── routers/
│   │   ├── auth.py             # Kayıt, login, JWT üretimi, login/register sayfaları
│   │   ├── todos.py            # Todo CRUD (API) + todo sayfaları (SSR)
│   │   ├── admin.py            # Admin'e özel todo yönetimi
│   │   └── users.py            # Profil görüntüleme, şifre/telefon güncelleme
│   ├── static/
│   │   ├── css/                # base.css, bootstrap.css
│   │   └── js/                 # base.js (fetch çağrıları, cookie yönetimi)
│   ├── templates/               # login, register, todo, add/edit-todo, layout, navbar
│   ├── test/                    # pytest test paketi + ortak fixture'lar (utils.py)
│   ├── database.py              # Engine, SessionLocal, declarative Base
│   ├── models.py                # Users, Todos SQLAlchemy modelleri
│   ├── main.py                  # Uygulama girişi, router'ların bağlanması
│   ├── alembic.ini
│   └── requirements.txt
├── .env                          # SECRET_KEY (repo'ya dahil değil)
└── README.md
```

## 🚀 Kurulum

### Gereksinimler

- Python 3.11+
- PostgreSQL (yerelde çalışan bir sunucu) **veya** hızlı başlangıç için SQLite

### Adımlar

```bash
# 1. Depoyu klonla
git clone https://github.com/gokdeniztural/FastAPI-TodoApp.git
cd FastAPI-TodoApp

# 2. Sanal ortam oluştur ve aktive et
python -m venv fastapienv
# Windows
fastapienv\Scripts\activate
# macOS / Linux
source fastapienv/bin/activate

# 3. Bağımlılıkları kur
pip install -r TodoApp/requirements.txt

# 4. .env dosyasını oluştur (bkz. Ortam Değişkenleri) ve kendi değerlerinizi girin
cp .env.example .env

# 5. Migrasyonları uygula
cd TodoApp
alembic upgrade head

# 6. Uygulamayı başlat
cd ..
uvicorn TodoApp.main:app --reload
```

Uygulama ayağa kalktıktan sonra:

- Arayüz: <http://127.0.0.1:8000/> (otomatik olarak todo sayfasına yönlenir)
- Swagger/OpenAPI dokümantasyonu: <http://127.0.0.1:8000/docs>
- Health check: <http://127.0.0.1:8000/healthy>

> **Veritabanı notu:** Bağlantı bilgisi artık kodda değil, `.env` dosyasındaki `DATABASE_URL` değişkeninde tutuluyor. `DATABASE_URL` tanımlanmazsa uygulama otomatik olarak yerel bir SQLite dosyasına (`./todos.db`) düşer — hızlıca denemek için Postgres kurmanıza gerek yok. Kendi PostgreSQL'inizi kullanmak isterseniz `.env` içine `DATABASE_URL=postgresql://<kullanici>:<sifre>@localhost:5432/TodoApplicationDatabase` satırını ekleyin; hem uygulama (`database.py`) hem de Alembic (`alembic/env.py`) bu değeri otomatik okur.

## 🔑 Ortam Değişkenleri

| Değişken | Açıklama | Nerede kullanılıyor |
|---|---|---|
| `SECRET_KEY` | JWT imzalama anahtarı | `routers/auth.py` → `create_access_token` / `get_current_user` |
| `DATABASE_URL` | Veritabanı bağlantı dizesi (örn. `postgresql://user:pass@localhost:5432/TodoApplicationDatabase`). Tanımlanmazsa yerel bir SQLite dosyasına (`./todos.db`) düşülür. | `database.py`, `alembic/env.py` |

`.env` dosyası `.gitignore` içinde olduğu için repoya dahil edilmez; her geliştirici kendi değerlerini `.env.example` dosyasını kopyalayarak oluşturmalıdır:

```bash
cp .env.example .env
```

`SECRET_KEY` üretmek için: `python -c "import secrets; print(secrets.token_hex(32))"`

## 🗃 Veritabanı Migrasyonları (Alembic)

```bash
cd TodoApp

# Mevcut migrasyonları uygula
alembic upgrade head

# models.py'de yapılan değişiklikten yeni migration üret
alembic revision --autogenerate -m "açıklama"

# Bir önceki migrasyona geri dön
alembic downgrade -1
```

## 📡 API Uç Noktaları

### `auth` — `/auth`

| Metot | Yol | Açıklama | Yetki |
|---|---|---|---|
| GET | `/auth/login-page` | Login sayfasını render eder | — |
| GET | `/auth/register-page` | Register sayfasını render eder | — |
| POST | `/auth/` | Yeni kullanıcı oluşturur | — |
| POST | `/auth/token` | Kullanıcı adı/şifre ile JWT (`access_token`) üretir | — |

### `todos` — `/todos`

| Metot | Yol | Açıklama | Yetki |
|---|---|---|---|
| GET | `/todos/todo-page` | Giriş yapan kullanıcının todo listesini render eder | JWT (cookie) |
| GET | `/todos/add-todo-page` | Yeni todo ekleme sayfası | JWT (cookie) |
| GET | `/todos/edit-todo-page/{todo_id}` | Todo düzenleme sayfası | JWT (cookie) |
| GET | `/todos/` | Kullanıcının tüm todo'larını JSON olarak döndürür | JWT (Bearer) |
| GET | `/todos/todo/{todo_id}` | Tek bir todo döndürür | JWT (Bearer) |
| POST | `/todos/todo` | Yeni todo oluşturur | JWT (Bearer) |
| PUT | `/todos/todo/{todo_id}` | Todo günceller | JWT (Bearer) |
| DELETE | `/todos/todo/{todo_id}` | Todo siler | JWT (Bearer) |

### `admin` — `/admin`

| Metot | Yol | Açıklama | Yetki |
|---|---|---|---|
| GET | `/admin/todo` | Sistemdeki tüm kullanıcılara ait todo'ları listeler | JWT + rol: `admin` |
| DELETE | `/admin/todo/{todo_id}` | Herhangi bir kullanıcının todo'sunu siler | JWT + rol: `admin` |

### `user` — `/user`

| Metot | Yol | Açıklama | Yetki |
|---|---|---|---|
| GET | `/user/` | Giriş yapan kullanıcının profil bilgisini döndürür | JWT (Bearer) |
| PUT | `/user/password` | Mevcut şifreyi doğrulayıp yeni şifre atar | JWT (Bearer) |
| PUT | `/user/phone_number/{phone_number}` | Telefon numarasını günceller | JWT (Bearer) |

### Genel

| Metot | Yol | Açıklama |
|---|---|---|
| GET | `/` | `/todos/todo-page` adresine yönlendirir |
| GET | `/healthy` | Basit health-check (`{"status": "healthy"}`) |

## 🔐 Kimlik Doğrulama Akışı

1. Kullanıcı `/auth/` uç noktasına kayıt olur → şifre `bcrypt` ile hash'lenip `users` tablosuna yazılır.
2. `/auth/token` uç noktasına `username`/`password` gönderilir (OAuth2 password flow) → doğrulama başarılıysa `sub`, `id`, `role` ve `exp` (20 dakika) alanlarını içeren bir JWT üretilip döndürülür.
3. **Sayfa (SSR) tarafı:** `base.js`, dönen token'ı `access_token` cookie'sine yazar; sonraki sayfa isteklerinde (`/todos/todo-page` vb.) token cookie'den okunup `get_current_user()` ile manuel doğrulanır. Token geçersizse kullanıcı `/auth/login-page`'e yönlendirilir ve cookie silinir.
4. **API tarafı:** `fetch` istekleri token'ı `Authorization: Bearer <token>` header'ında gönderir; FastAPI tarafında `OAuth2PasswordBearer` + `Depends(get_current_user)` ile doğrulanır.
5. **Yetkilendirme:** Kullanıcının `role` alanı JWT payload'ına gömülüdür; `admin` router'ındaki her uç nokta bu alanı kontrol ederek erişimi sınırlar.

## 🧪 Testler

```bash
# Proje kök dizininden çalıştırılmalı (main.py, "TodoApp/static" yolunu kök dizine göre çözer)
pytest TodoApp/test -v
```

- Testler production veritabanından tamamen izole, ayrı bir **SQLite** dosyası (`testdb.db`) üzerinde çalışır.
- `get_db` ve `get_current_user` bağımlılıkları `test/utils.py` içinde `app.dependency_overrides` ile sahte (test) sürümleriyle değiştirilir — gerçek JWT/DB olmadan uç noktalar izole test edilir.
- `test_user` ve `test_todo` pytest fixture'ları her testten sonra ilgili tabloları temizler.
- Kapsam: kayıt/login (`test_auth.py`), todo CRUD (`test_todos.py`), admin uç noktaları (`test_admin.py`), kullanıcı profili (`test_users.py`).

---

**Geliştirici:** [Gökdeniz Tural](https://github.com/gokdeniztural)
