import requests
from loguru import logger


def facebook_login(email, password, proxy):
    proxy_dict = {
        "http": f"http://{proxy['username']}:{proxy['password']}@{proxy['ip']}:{proxy['port']}",
        "https": f"http://{proxy['username']}:{proxy['password']}@{proxy['ip']}:{proxy['port']}",
    }

    try:
        # Попытка логина на Facebook через прокси
        login_url = "https://www.facebook.com/login"
        data = {"email": email, "pass": password}
        response = requests.post(login_url, data=data, proxies=proxy_dict, timeout=10)

        if response.status_code == 200:
            logger.info(
                f"Успешный логин: {email} через прокси {proxy['ip']}:{proxy['port']}"
            )
            return True
        else:
            logger.error(
                f"Ошибка логина: {email} через прокси {proxy['ip']}:{proxy['port']} - Статус: {response.status_code}"
            )
            return False
    except requests.RequestException as e:
        logger.error(f"Ошибка при логине {email} через прокси {proxy['ip']}: {e}")
        return False
