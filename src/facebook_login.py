import os
import time
import zipfile

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Bright Data proxy credentials
proxy_host = "brd.superproxy.io"
proxy_port = 22225
proxy_username = "brd-customer-hl_6779d688-zone-gf_test0"
proxy_password = "fq3n6o413q4r"


# Create a custom Chrome extension to handle proxy authentication
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


# Create the proxy extension
proxy_extension = create_proxy_extension(
    proxy_host, proxy_port, proxy_username, proxy_password
)

# Set up Chrome options
chrome_options = Options()
# Add proxy extension to Chrome
chrome_options.add_extension(proxy_extension)
chrome_options.add_argument("--start-maximized")

# Start the Chrome driver with the proxy
webdriver_service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

# Test the IP via the proxy
driver.get("https://whatismyipaddress.com/")
time.sleep(5)

# You can now interact with the page as needed
# Here’s an example for Facebook login:
driver.get("https://www.facebook.com/login")
time.sleep(5)

# Locate the username and password fields
username_field = driver.find_element(By.NAME, "email")  # Adjust if necessary
password_field = driver.find_element(By.NAME, "pass")  # Adjust if necessary

# Provide credentials (use real Facebook credentials for testing purposes)
username = "your_facebook_username"
password = "your_facebook_password"
username_field.send_keys(username)
password_field.send_keys(password)

# Wait for inputs to be registered
time.sleep(2)

# Click the login button
login_button = driver.find_element(By.NAME, "login")  # Adjust if necessary
login_button.click()

# Wait for the login process
time.sleep(10)

# After login, check the page for success or errors

# Cleanup: Close the browser
driver.quit()
