import json
import os

from loguru import logger

from src.database import init_db, save_working_pair
from src.facebook_login import facebook_login

# Инициализируем базу данных при старте скрипта
init_db()


def check_proxy_account_pairs(accounts_file, proxies_file):
    # Загрузка данных
    with open(accounts_file, "r") as f:
        accounts = json.load(f)["accounts"]
    with open(proxies_file, "r") as f:
        proxies = json.load(f)["proxies"]

    for account in accounts:
        for proxy in proxies:
            if facebook_login(account["email"], account["password"], proxy):
                save_working_pair(account["email"], proxy["ip"])
                logger.info(
                    f"Успешная связка: {account['email']} через прокси {proxy['ip']}"
                )
            else:
                logger.info(f"Неудачная проверка: {account['email']} -> {proxy['ip']}")
