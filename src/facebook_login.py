import os
import time
import zipfile

from loguru import logger
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def create_proxy_extension(proxy_host, proxy_port, proxy_username, proxy_password):
    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version": "22.0.0"
    }
    """

    background_js = f"""
    var config = {{
        mode: "fixed_servers",
        rules: {{
            singleProxy: {{
                scheme: "http",
                host: "{proxy_host}",
                port: parseInt({proxy_port})
            }},
            bypassList: ["localhost"]
        }}
    }};

    chrome.proxy.settings.set({{value: config, scope: "regular"}}, function() {{}});

    function callbackFn(details) {{
        return {{
            authCredentials: {{
                username: "{proxy_username}",
                password: "{proxy_password}"
            }}
        }};
    }}

    chrome.webRequest.onAuthRequired.addListener(
        callbackFn,
        {{urls: ["<all_urls>"]}},
        ['blocking']
    );
    """

    extension_dir = os.path.join(os.getcwd(), "chrome_proxy_extension")
    os.makedirs(extension_dir, exist_ok=True)

    with open(os.path.join(extension_dir, "manifest.json"), "w") as manifest_file:
        manifest_file.write(manifest_json)

    with open(os.path.join(extension_dir, "background.js"), "w") as background_file:
        background_file.write(background_js)

    extension_zip = os.path.join(os.getcwd(), "chrome_proxy_auth.zip")
    with zipfile.ZipFile(extension_zip, "w") as zip_file:
        zip_file.write(os.path.join(extension_dir, "manifest.json"), "manifest.json")
        zip_file.write(os.path.join(extension_dir, "background.js"), "background.js")

    return extension_zip


def check_user(phone, email, password, proxy):
    logger.info(f"Checking user: phone: {phone} email: {email} proxy: {proxy}")
    proxy_host = proxy["host"]
    proxy_port = proxy["port"]
    proxy_username = proxy["username"]
    proxy_password = proxy["password"]
    try:
        non_empty_value = phone if phone else email

        proxy_extension = create_proxy_extension(
            proxy_host, proxy_port, proxy_username, proxy_password
        )
        chrome_options = Options()
        chrome_options.add_extension(proxy_extension)
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--headless=new")

        webdriver_service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

        driver.get("https://www.facebook.com/login")
        time.sleep(2)

        username_field = driver.find_element(By.NAME, "email")
        password_field = driver.find_element(By.NAME, "pass")

        username = non_empty_value
        password = password
        username_field.send_keys(username)
        password_field.send_keys(password)

        time.sleep(2)

        login_button = driver.find_element(By.NAME, "login")
        login_button.click()

        time.sleep(5)
        elements = driver.find_elements(By.ID, "error_box")
        if len(elements) > 0:
            logger.error("Error with account, error_box found")
            return False

        return True

    except NoSuchElementException as er:
        logger.error(f"Error with account, No such elem: {er}")
        return False
    except Exception as e:
        logger.error(f"Error with account, other error: {er}")
        return False

    finally:
        driver.quit()
