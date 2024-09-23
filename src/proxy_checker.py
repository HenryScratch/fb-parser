import json
import os

from loguru import logger

from src.database import init_db, save_working_pair
from src.facebook_login import check_user

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
            if check_user(
                email=account["email"],
                phone=account["phone"],
                password=account["password"],
                proxy=proxy,
            ):
                save_working_pair(
                    proxy_host=proxy["host"],
                    account_email=account["email"],
                    account_phone=account["phone"],
                )
                logger.info(
                    f"Успешная связка: {account['email']} {account['phone']} через прокси {proxy['host']}"
                )
            else:
                logger.info(
                    f"Неудачная проверка: {account['email']} {account['phone']} -> {proxy['host']}"
                )
