import logging
import datetime
from dataclasses import dataclass
from aiogram.types import Message, ChatPermissions
from database.models import async_session
from database.models import KeyWords, Emodji, Time
from sqlalchemy import select
from aiogram import Bot
from config_data.config import Config, load_config

from sqlalchemy import desc

config: Config = load_config()


# Добавляем пользователя из чата в БД
async def add_key_word(data: dict) -> None:
    """
    Добавляем слова в БД
    :param word:
    :return:
    """
    logging.info(f'add_key_word')
    async with async_session() as session:
        word = await session.scalar(select(KeyWords).where(KeyWords.word == data['word']))
        if not word:
            session.add(KeyWords(**data))
            await session.commit()


async def select_key_words() -> list[KeyWords]:
    """
    Получаем список слов
    :return:
    """
    logging.info(f'select_key_words')
    async with async_session() as session:
        key_words = await session.scalars(select(KeyWords))
        list_key_words = [word for word in key_words]
        return list_key_words


async def delete_key_word(id_word: int) -> None:
    """
    Удаляем слово из БД
    :param id_word:
    :return:
    """
    logging.info(f'add_key_word')
    async with async_session() as session:
        word = await session.scalar(select(KeyWords).where(KeyWords.id_word == id_word))
        if word:
            session.delete(word)
            await session.commit()


async def add_emodji(data: dict) -> None:
    """
    Добавляем слова в БД
    :param data:
    :return:
    """
    logging.info(f'add_key_word')
    async with async_session() as session:
        emodji = await session.scalar(select(Emodji))
        if not emodji:
            session.add(Emodji(**data))
            await session.commit()
        else:
            emodji.emodji = data['emodji']
            await session.commit()


async def select_emodji() -> Emodji:
    """
    Получаем список слов
    :return:
    """
    logging.info(f'select_emodji')
    async with async_session() as session:
        return await session.scalar(select(Emodji))


async def add_time(data: dict) -> None:
    """
    Добавляем слова в БД
    :param data:
    :return:
    """
    logging.info(f'add_time')
    async with async_session() as session:
        time = await session.scalar(select(Time))
        if not time:
            session.add(Time(**data))
            await session.commit()
        else:
            time.time = data['time']
            await session.commit()


async def select_time() -> Time:
    """
    Получаем список слов
    :return:
    """
    logging.info(f'select_time')
    async with async_session() as session:
        return await session.scalar(select(Time))
