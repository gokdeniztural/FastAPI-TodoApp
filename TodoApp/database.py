from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
import os
from dotenv import load_dotenv

load_dotenv()  # .env dosyasındaki DATABASE_URL gibi değişkenleri sisteme yükler

# Bağlantı dizesi artık kodda değil, .env dosyasındaki DATABASE_URL değişkeninde tutuluyor.
# .env içinde DATABASE_URL tanımlı değilse (örn. hızlı deneme için) yerel bir SQLite dosyasına düşülür.
SQLALCHEMY_DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./todos.db')

connect_args = {'check_same_thread': False} if SQLALCHEMY_DATABASE_URL.startswith('sqlite') else {}
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args)
# Uygulamanın veritabanıyla etkileşimini sağlayan motor.

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # Her bir istek için geçici
# bir oturum oluşturuyoruz
# İşlemleri hemen veritabanına kaydetme, ben kodun içinde açıkça onay verene kadar (session.commit()) bekle

Base = declarative_base() # test_todos.py dosyasında da kullanmak için Base'i burada tanımlıyoruz.