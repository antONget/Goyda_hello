from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str
    support_id: int
    group_id: int
    admin_ids: str


@dataclass
class Config:
    tg_bot: TgBot


def load_config(path: str = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(token=env('BOT_TOKEN'),
                               support_id=env('SUPPORT_ID'),
                               group_id=env('GROUP_ID'),
                               admin_ids=env('ADMIN_IDS')))
