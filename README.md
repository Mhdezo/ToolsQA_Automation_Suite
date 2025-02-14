# ToolsQA Automation Suite

This project automates tests for [ToolsQA Practice Form](https://demoqa.com/automation-practice-form) using Selenium WebDriver and Python.

## 📂 Project Structure
```
ToolsQA_Automation_Suite/
├── data/ # Test data (Excel, images)
├── pages/ # Page Object Model (POM) classes
├── tests/ # Test scripts
├── utils/ # Utility functions
├── logs/ # Log files
├── reports/ # HTML test reports
├── Drivers/ # Browser drivers (e.g., ChromeDriver, GeckoDriver)
├── conftest.py # pytest fixtures
├── logging_config.py # Centralized logging configuration
├── config.ini # Configuration file for paths and settings
├── requirements.txt # Dependencies
└── README.md # Project documentation
```

##   Setup & Installation

1. Clone the Repository:
   ```sh
   git clone https://github.com/your-username/ToolsQA_Automation_Suite.git
   cd ToolsQA_Automation_Suite
   ```
## Install Dependencies:
```sh
pip install -r requirements.txt
```
## Download Browser Drivers:

- Download the required browser drivers (e.g., ChromeDriver, GeckoDriver) and place them in the Drivers directory.
- Update the paths in config.ini if necessary.

## ▶️ Running Tests
```sh
python -m pytest -v --html=reports/report.html
```

## 📜 Logging
Logs are stored in `logs/logfile.log`.
Ensure the logs directory exists and is writable.

## 🛠 Configuration
- config.ini: Contains paths to browser drivers, test data, and other configurations.
- logging_config.py: Centralized logging configuration.

## 🤝 Contributions
Feel free to fork and contribute! Pull requests are welcome.
