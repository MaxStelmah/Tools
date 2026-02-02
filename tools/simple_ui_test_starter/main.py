import requests
import json
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os
import sys
from config import *

class Logger:
    """Simple logger that writes to both console and file"""
    
    def __init__(self, log_file_path=None):
        self.log_file_path = log_file_path
        self.enabled = LOGGING_CONFIG["enabled"] and log_file_path is not None
    
    def log(self, message):
        """Print message and write to log file"""
        print(message)
        
        if self.enabled and self.log_file_path:
            try:
                with open(self.log_file_path, 'a', encoding='utf-8') as f:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    f.write(f"[{timestamp}] {message}\n")
            except Exception as e:
                print(f"Warning: Could not write to log file: {e}")

    def mark_as_failed(self):
        """Mark the test run as failed and rename log file with failed prefix"""
        if not self.enabled or not self.log_file_path:
            return
        
        self.failed = True
        
        try:
            # Get directory and filename
            directory = os.path.dirname(self.log_file_path)
            filename = os.path.basename(self.log_file_path)
            
            # Create new filename with failed prefix
            new_filename = f"failed_{filename}"
            new_log_path = os.path.join(directory, new_filename)
            
            # Close any open file handles and rename
            if os.path.exists(self.log_file_path):
                os.rename(self.log_file_path, new_log_path)
                self.log_file_path = new_log_path
                print(f"Log file marked as failed: {new_filename}")
        except Exception as e:
            print(f"Warning: Could not rename log file: {e}")
            
def setup_logging(email):
    """Create logs folder and prepare log file"""
    if not LOGGING_CONFIG["enabled"]:
        return Logger()
    
    # Determine logs folder path
    if LOGGING_CONFIG["logs_folder"]:
        logs_folder = LOGGING_CONFIG["logs_folder"]
    else:
        # Use script directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        logs_folder = os.path.join(script_dir, "Logs")
    
    # Create Logs folder if it doesn't exist
    try:
        os.makedirs(logs_folder, exist_ok=True)
    except Exception as e:
        print(f"Warning: Could not create logs folder: {e}")
        return Logger()
    
    # Create log file path (sanitize email for filename)
    safe_email = email.replace('@', '_').replace(':', '_')
    log_file = os.path.join(logs_folder, f"{safe_email}.log")
    
    logger = Logger(log_file)
    logger.log(f"Log file created: {log_file}")
    logger.log("="*60)
    
    return logger


def encrypt_password(password):
    """Encrypt password for API request"""
    cipher = AES.new(
        "key".encode(),
        AES.MODE_ECB
    )
    result = cipher.encrypt(pad(
        (password).encode(),
        AES.block_size,
        style='style'
    ))
    return base64.b64encode(result).decode("ascii")

def generate_email():
    """Generate unique email with timestamp"""
    timestamp = datetime.now().strftime("%y%m%d%H%M")
    prefix = EMAIL_CONFIG.get("prefix", "test_")
    domain = EMAIL_CONFIG.get("domain", "example.com")
    email = f"{prefix}{timestamp}@{domain}"
    return email


def prepare_registration_data(email, encrypted_password):
    """Prepare registration payload for API"""
    return {
        ...
        "client": {
            "email": email,
            "password": encrypted_password,
            "firstName": CLIENT_CONFIG["firstName"],
            "lastName": CLIENT_CONFIG["lastName"],
            "birthDay": CLIENT_CONFIG["birthDay"],
            "country": CLIENT_CONFIG["country"],
            "language": CLIENT_CONFIG["language"]
        },
        ...
    }


def register_client(email, password, logger):
    """Register new client via API"""
    logger.log(f"Registering client with email: {email}")
    
    encrypted_password = encrypt_password(email, password)
    data = prepare_registration_data(email, encrypted_password)
    
    headers = {
        "Authorization": API_AUTH,
        "content-type": "application/json"
    }
    
    response = requests.post(API_URL, headers=headers, data=json.dumps(data))
    
    logger.log(f"Registration status: {response.status_code}")
    
    # Beautify JSON response
    try:
        response_json = response.json()
        beautified_response = json.dumps(response_json, indent=2, ensure_ascii=False)
        logger.log("Response:")
        logger.log(beautified_response)
    except json.JSONDecodeError:
        logger.log(f"Response (not JSON): {response.text}")
    
    if response.status_code == 200:
        return True, response_json
    else:
        return False, None


def setup_chrome_driver():
    """Configure and create Chrome WebDriver"""
    chrome_options = webdriver.ChromeOptions()
    
    if CHROME_CONFIG.get("auto_open_devtools"):
        chrome_options.add_argument("--auto-open-devtools-for-tabs")
    
    if CHROME_CONFIG.get("mobile_device"):
        mobile_emulation = {"deviceName": CHROME_CONFIG["mobile_device"]}
        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)   
    
    if CHROME_CONFIG.get("keep_browser_open"):
        chrome_options.add_experimental_option("detach", True)
    
    if CHROME_CONFIG.get("browser_language"):
        chrome_options.add_argument(f"--lang={CHROME_CONFIG['browser_language']}")
    
    driver = webdriver.Chrome(options=chrome_options)
    
    # Only maximize if not using mobile emulation (mobile needs specific viewport size)
    if CHROME_CONFIG.get("maximize_window") and not CHROME_CONFIG.get("mobile_device"):
        driver.maximize_window()
    
    return driver


def login_to_web_app(driver, email, password, logger):
    """Open web app and login with credentials (manual login method)"""
    logger.log(f"Opening web application: {WEB_APP_URL}")
    logger.log("Using manual login method (email + password)")
    
    driver.get(WEB_APP_URL)
    driver.implicitly_wait(2)
    
    # Click login button
    btn_enter = driver.find_element("xpath", "//*[text()='Log in']")
    btn_enter.click()
    
    # Enter email
    email_input = driver.find_element(By.ID, "login-field")
    email_input.clear()
    email_input.send_keys(email)
    
    # Enter password
    pass_input = driver.find_element(By.ID, "password-field")
    pass_input.clear()
    pass_input.send_keys(password)
    
    # Submit login
    btn_login = driver.find_element("xpath", "//input[@value='Log in']")
    btn_login.click()
    
    logger.log("Login completed!")


def extract_auto_login_url(response_data, logger):
    """Extract auto-login URL from API response"""
    try:
        # Adjust this path based on your actual API response structure
        # Common patterns: response_data['autoLoginUrl'] or response_data['data']['loginUrl']
        auto_login_url = response_data.get('startUrl')
        
        if auto_login_url:
            logger.log(f"Auto-login URL extracted: {auto_login_url}")
            return auto_login_url
        else:
            logger.log("Warning: Auto-login URL not found in response")
            logger.log("Available keys in response: " + str(list(response_data.keys())))
            return None
    except Exception as e:
        logger.log(f"Error extracting auto-login URL: {e}")
        logger.mark_as_failed()
        return None


def login_with_auto_url(driver, auto_login_url, logger):
    """Open web app using auto-login URL (no credentials needed)"""
    logger.log("Using auto-login URL method")
    logger.log(f"Opening URL: {auto_login_url}")
    
    driver.get(auto_login_url)
    driver.implicitly_wait(2)
    
    logger.log("Auto-login completed!")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main execution flow"""
    logger = None
    
    try:
        # Generate credentials
        email = generate_email()
        password = CLIENT_CONFIG["password"]
        
        # Setup logging
        logger = setup_logging(email)
        logger.log("Starting client registration process")
        logger.log(f"Generated email: {email}")
        logger.log(f"Login method: {LOGIN_METHOD}")
        
        # Register client via API
        registration_successful, response_data = register_client(email, password, logger)
        
        if not registration_successful:
            logger.log("Registration failed! Check the error above.")
            logger.mark_as_failed()
            return
        
        # Setup browser
        driver = setup_chrome_driver()
        
        # Choose login method
        if LOGIN_METHOD == "auto_login_url" and response_data:
            auto_login_url = extract_auto_login_url(response_data, logger)
            if auto_login_url:
                login_with_auto_url(driver, auto_login_url, logger)
            else:
                logger.log("Falling back to manual login method")
                login_to_web_app(driver, email, password, logger)
        else:
            login_to_web_app(driver, email, password, logger)
        
        logger.log("\n" + "="*60)
        logger.log("Test client ready!")
        logger.log(f"Email: {email}")
        logger.log(f"Password: {password}")
        logger.log("="*60)
        
    except Exception as e:
        error_msg = f"Script failed with error: {str(e)}"
        if logger:
            logger.log(error_msg)
            logger.mark_as_failed()
        else:
            print(error_msg)
        raise


if __name__ == "__main__":
    main()
