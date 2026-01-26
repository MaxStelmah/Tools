# Automated Test Client Registration Tool

> **Stop wasting time on manual test account creation.** Automate the entire workflow from API registration to browser login in seconds.

## 🎯 The Problem

If you're a QA engineer, product manager, or support team member, you know this pain:

**The Old Way:**
1. Open Postman/cURL to call registration API
2. Manually copy credentials to a text file
3. Open browser and navigate to login page
4. Type email and password manually
5. Search through terminal logs or multiple tools for session info
6. Repeat this 10-50 times per day...

**Result:** 5-10 minutes wasted per test account. Multiply that by your daily testing needs.

## ✨ The Solution

One command. One configuration file. Instant test accounts with browser sessions ready to go.

```bash
python main.py
```

**What happens:**
- Generates unique test email automatically
- Registers client via your API
- Launches browser and logs in
- Displays credentials in console
- Saves complete session log to file
- Keeps browser open for testing

**✅ Time saved:** 90% reduction in setup time. Focus on actual testing, not repetitive setup.

---

## 🚀 Quick Start

### Installation


1. Install python

2. Install dependencies
```bash
pip install requests selenium pycryptodome
```
3. Download config.py and main.py and place it in the same folder

### Configuration

1. Open `config.py`
2. Update your API endpoint and authentication:

```python
API_URL = "https://your-api.com/register"
API_AUTH = "Bearer your_api_token"
WEB_APP_URL = "https://your-app.com"
```

3. Customize email generation for your team:

```python
EMAIL_CONFIG = {
    "prefix": "qa_john_",
    "domain": "test.company.com"
}
# Generates: qa_john_2501231530@test.company.com
```

### Add Custom API Fields

Need to send additional fields? Edit `prepare_registration_data()`:

```python
def prepare_registration_data(email, encrypted_password):
    return {
        "email": email,
        "password": encrypted_password,
        "customField": "your_value",  # Add here
        "anotherField": "another_value"
    }
```

### Add encription parameters

Specify your encription key and style in `encrypt_password()`

### Run

```bash
python main.py
```

Thats it! Your browser opens with a logged-in test account, and all details are saved to a log file.

---

## 💡 Who Is This For?

### QA Engineers
**Problem:** Need 20+ test accounts daily with different configurations  
**Solution:** Configure once, generate instantly. No more API tool switching.

### Product Managers
**Problem:** Need demo accounts for stakeholder presentations  
**Solution:** Generate professional demo accounts in seconds, no technical knowledge required.

### Customer Support
**Problem:** Need to recreate customer scenarios for debugging  
**Solution:** Quickly create accounts matching specific customer configurations.

### Development Teams
**Problem:** Manual testing workflows slow down sprint velocity  
**Solution:** Automate the boring stuff, focus on building features.

---

## ⚙️ Configuration Options

All configuration is done in `config.py` - **no code changes needed**.

### Email Generation

Control how test emails are generated:

```python
EMAIL_CONFIG = {
    "prefix": "your_name_",
    "domain": "test.yourcompany.com"
}
```

**Examples:**
- QA Team: `qa_team_2501231530@test.company.com`
- Mobile Testing: `mobile_2501231530@qa.mobile.com`
- PO Demos: `demo_2501231530@demo.company.com`

### Client Configuration

Set default parameters for all test clients:

```python
CLIENT_CONFIG = {
    "password": "Test123!",
    "firstName": "Test",
    "lastName": "User",
    "country": "USA",
    "language": "en"
    # Add any fields your API requires
}
```

### Browser Settings

```python
CHROME_CONFIG = {
    "auto_open_devtools": True,      # Open DevTools automatically
    "keep_browser_open": True,       # Don't close when script ends
    "maximize_window": True,         # Start maximized
    # "mobile_device": "iPhone 14"   # Uncomment for mobile testing
}
```

### Login Methods

Two approaches supported:

```python
LOGIN_METHOD = "auto_login_url"  # If your registration API returns an autostart link
# or
LOGIN_METHOD = "manual_login"    # Traditional email/password input via the script
```

---

## 📊 Features

### Fast Auto-Login
Uses API-provided login URLs for instant authentication (when available).

### Automatic Logging
Every session is logged with timestamps. Perfect for:
- Debugging test failures
- Audit trails
- Sharing credentials with team members
- Tracking which accounts were used when

### Multi-Environment Support
Easily switch between dev, staging, and production environments by changing config values.

### Mobile Testing
Built-in mobile device emulation for responsive testing:

```python
CHROME_CONFIG = {
    "mobile_device": "iPhone 14 Pro Max"
}
```

### Flexible API Integration
Adapts to your API structure. Simple hooks to customize request/response handling.

---

## 📁 Project Structure

```
automated-test-client-registration/
├── config.py              # All configuration here
├── main.py                # Main execution script
├── README.md
└── Logs/                  # Auto-generated
    ├── qa_team_250123_test.company.com.log
    └── ...
```

---

## 📋 Sample Log Output

```
[2025-01-23 15:30:45] ============================================================
[2025-01-23 15:30:45] Starting client registration process
[2025-01-23 15:30:45] Generated email: qa_test_250123@test.company.com
[2025-01-23 15:30:46] Registration status: 200 ✓
[2025-01-23 15:30:47] Auto-login completed!
[2025-01-23 15:30:47] ============================================================
[2025-01-23 15:30:47] 🎉 Test client ready!
[2025-01-23 15:30:47] Email: qa_test_250123@test.company.com
[2025-01-23 15:30:47] Password: Test123!
[2025-01-23 15:30:47] ============================================================
```

---

## 🎯 Common Use Cases

### Scenario 1: Daily QA Workflow
```python
# Morning setup for regression testing
EMAIL_CONFIG = {"prefix": "regression_", "domain": "qa.company.com"}
# Run 5 times for different test scenarios
```

### Scenario 2: Client Demo Preparation
```python
# Create professional demo account
EMAIL_CONFIG = {"prefix": "demo_", "domain": "demo.company.com"}
CLIENT_CONFIG = {"firstName": "Demo", "lastName": "Account"}
```

### Scenario 3: Bug Reproduction
```python
# Match customer's exact configuration
CLIENT_CONFIG = {
    "country": "FRA",
    "language": "fr",
    "birthDay": "1985-06-15"
}
```

### Scenario 4: Mobile Testing Sprint
```python
# Test on multiple devices
CHROME_CONFIG = {"mobile_device": "iPhone 14 Pro Max"}
# Change device, run again
CHROME_CONFIG = {"mobile_device": "Samsung Galaxy S21"}
```

---



## 📝 Requirements

- Python 3.7+
- Chrome browser
- ChromeDriver (auto-managed by Selenium 4.6+)

---

## ⚠️ Troubleshooting

### "Auto-login URL not found"
**Cause:** API response structure doesn't match expected format  
**Fix:** Check logs for available response keys and update extraction logic

### "ChromeDriver not found"
**Cause:** Outdated Selenium version  
**Fix:** `pip install --upgrade selenium`

### "Registration fails with 401"
**Cause:** Invalid API authentication  
**Fix:** Verify your `API_AUTH` token in config.py

### Browser closes immediately
**Cause:** Script configuration  
**Fix:** Set `"keep_browser_open": True` in `CHROME_CONFIG`

---

## 🙏 Acknowledgments

Built by IT engineers, for IT engineers. **If this tool saves you time, give it a ⭐ on GitHub!**

---

## 💬 Support

- 🐛 **Found a bug?** Open an issue
- 💡 **Have an idea?** Start a discussion
- 📧 **Need help?** Check existing issues or create a new one

---

**Thank you!** 