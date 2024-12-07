from sqlalchemy import String, Integer, BigInteger, DateTime
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine


# Создаем асинхронный движок
engine = create_async_engine("sqlite+aiosqlite:///database/db.sqlite3", echo=False)
# Настраиваем фабрику сессий
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class ChatAction(Base):
    __tablename__ = 'chat_actions'
    tg_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger)
    type: Mapped[str] = mapped_column(String(50))
    added = mapped_column(DateTime)


class ChatUser(Base):
    __tablename__ = 'chat_users'
    tg_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(200))
    last_name: Mapped[str] = mapped_column(String(200))
    user_name: Mapped[str] = mapped_column(String(100))
    reputation: Mapped[int] = mapped_column(BigInteger)
    total_help: Mapped[int] = mapped_column(BigInteger)
    mutes: Mapped[int] = mapped_column(BigInteger)
    last_rep_boost = mapped_column(DateTime)
    last_help_boost = mapped_column(DateTime)
    status: Mapped[str] = mapped_column(String(30))


class User(Base):
    __tablename__ = 'users'
    tg_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(String(100))


class KeyWords(Base):
    __tablename__ = 'keywords'
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    word: Mapped[str] = mapped_column(String(100))


class Emodji(Base):
    __tablename__ = 'emodji'
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    emodji: Mapped[str] = mapped_column(String(100))


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
