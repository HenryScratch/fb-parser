import time

import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

# Bright Data proxy credentials
proxy_host = "brd.superproxy.io"
proxy_port = "22225"
proxy_username = "brd-customer-hl_6779d688-zone-gf_test0"
proxy_password = "fq3n6o413q4r"
proxy_credentials = f"{proxy_username}:{proxy_password}@{proxy_host}:{proxy_port}"

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")
chrome_options.add_argument(f"--proxy-server=http://{proxy_credentials}")

# webdriver_service = Service(
#     "/Users/aurelian/Documents/ddc-projects/fb-parser/src/chromedriver"
# )
driver = webdriver.Chrome(options=chrome_options)


driver.get("https://www.facebook.com/login")
time.sleep(5)

# Locate the username and password fields
username_field = driver.find_element(By.NAME, "email")  # Adjust if necessary
password_field = driver.find_element(By.NAME, "pass")  # Adjust if necessary

# Provide credentials (use dummy values for testing purposes)
username = "your_facebook_username"
password = "your_facebook_password"
username_field.send_keys(username)
password_field.send_keys(password)
time.sleep(5)

# Click the login button
login_button = driver.find_element(By.NAME, "login")  # Adjust if necessary
login_button.click()

# Wait for the login process
time.sleep(10)

# account bad
# div
# id = error_box

# # Parse and check for relevant requests (such as login)
# for entry in har_data["log"]["entries"]:
#     request_url = entry["request"]["url"]
#     if "login" in request_url:  # Look for requests related to the login
#         print(f"Request URL: {request_url}")
#         print(f"Request Method: {entry['request']['method']}")
#         print(f"Response Status: {entry['response']['status']}")
#         print(f"Response Content: {entry['response']['content']['text']}")

# Cleanup: Stop the proxy and close the browser
driver.quit()
