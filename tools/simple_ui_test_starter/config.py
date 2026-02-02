# ============================================================================
# CONFIGURATION - Change these values as needed
# ============================================================================

# Web Application URL
WEB_APP_URL = "https://your-app.com"

# Client Parameters
CLIENT_CONFIG = {
    "password": "qwerty",
    "firstName": "John",
    "lastName": "Doe",
    "birthDay": "1900-01-01",
    "country": "USA",
    "language": "en"
}

# Email Generation Configuration
EMAIL_CONFIG = {
    "prefix": "my_name_",  # Your unique name/prefix before timestamp
    "domain": "somemail.com"  # Domain after '@'
    # Result: {prefix}{timestamp}@{domain}
    # Example: my_name_2501141530@somemail.com
}

# Logging Configuration
LOGGING_CONFIG = {
    "logs_folder": "",  # Leave empty to use script directory, or specify path like "C:/QA/Logs"
    "enabled": True
}

# Login Method Configuration
LOGIN_METHOD = "auto_login_url"  # Options: "auto_login_url" or "manual_login"

# API Configuration
API_URL = "https://your-api.com/register"
API_AUTH = "Bearer your_api_token"

# Chrome Browser Configuration
CHROME_CONFIG = {
    "auto_open_devtools": True,
    "keep_browser_open": True,
    "browser_language": "en",
    "maximize_window": True,
    # Uncomment to use mobile emulation:
    # "mobile_device": "iPhone 14 Pro Max"
}