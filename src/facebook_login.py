import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service

# Bright Data proxy credentials
proxy_host = "brd.superproxy.io"
proxy_port = 22225
proxy_username = "brd-customer-hl_6779d688-zone-gf_test0"
proxy_password = "fq3n6o413q4r"

# Set up Selenium to use the proxy with Firefox
firefox_options = webdriver.FirefoxOptions()

# Set proxy settings for Firefox
proxy_credentials = f"{proxy_username}:{proxy_password}@{proxy_host}:{proxy_port}"
firefox_options.set_preference("network.proxy.type", 1)
firefox_options.set_preference("network.proxy.http", proxy_host)
firefox_options.set_preference("network.proxy.http_port", proxy_port)
firefox_options.set_preference("network.proxy.ssl", proxy_host)
firefox_options.set_preference("network.proxy.ssl_port", proxy_port)
firefox_options.set_preference("network.proxy.socks_remote_dns", True)

# Disable proxy authentication prompt
firefox_options.set_preference("network.proxy.http", proxy_host)
firefox_options.set_preference("network.proxy.http_port", proxy_port)
firefox_options.set_preference("signon.autologin.proxy", True)

# Setup for the Firefox WebDriver
webdriver_service = Service(
    "/Users/aurelian/Documents/ddc-projects/fb-parser/src/geckodriver"
)  # Adjust path to your geckodriver

# Initialize WebDriver with options
driver = webdriver.Firefox(service=webdriver_service, options=firefox_options)


# Go to the Facebook login page
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
