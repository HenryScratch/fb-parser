import os

from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Определение базы данных и пути для SQLite
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "proxy_account_pairs.db")

# Создаем движок для SQLite
engine = create_engine(
    f"sqlite:///{DATABASE_PATH}", connect_args={"check_same_thread": False}
)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class ProxyAccountPair(Base):
    __tablename__ = "proxy_account_pairs"
    id = Column(String, primary_key=True)
    account_email = Column(String, unique=True, nullable=False)
    account_phone = Column(String, unique=True, nullable=False)
    proxy_host = Column(String, nullable=False)


# Инициализация базы данных
def init_db():
    Base.metadata.create_all(bind=engine)


def save_working_pair(account_email, account_phone, proxy_host):
    session = SessionLocal()
    if not account_email:
        account_email = "phone"
    if not account_phone:
        account_phone = "email"

    pair = ProxyAccountPair(
        account_email=account_email, account_phone=account_phone, proxy_host=proxy_host
    )
    try:
        session.add(pair)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Ошибка при сохранении: {e}")
    finally:
        session.close()
