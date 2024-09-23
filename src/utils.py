import os
import time
import zipfile

from selenium import webdriver
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

    # Create the extension directory
    extension_dir = os.path.join(os.getcwd(), "chrome_proxy_extension")
    os.makedirs(extension_dir, exist_ok=True)

    # Write manifest.json and background.js
    with open(os.path.join(extension_dir, "manifest.json"), "w") as manifest_file:
        manifest_file.write(manifest_json)

    with open(os.path.join(extension_dir, "background.js"), "w") as background_file:
        background_file.write(background_js)

    # Zip the extension for Chrome
    extension_zip = os.path.join(os.getcwd(), "chrome_proxy_auth.zip")
    with zipfile.ZipFile(extension_zip, "w") as zip_file:
        zip_file.write(os.path.join(extension_dir, "manifest.json"), "manifest.json")
        zip_file.write(os.path.join(extension_dir, "background.js"), "background.js")

    return extension_zip
