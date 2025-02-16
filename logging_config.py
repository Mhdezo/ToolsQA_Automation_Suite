import logging
import os

# Get the absolute path of the project root dynamically
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))  # Path to logging_config.py

# Ensure we are setting the correct root (move up directories if inside tests/)
while not os.path.exists(os.path.join(PROJECT_ROOT, "logs")):
    PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)

# Define log directory inside the project root
LOG_DIR = os.path.join(PROJECT_ROOT, "logs")

# Ensure the logs directory exists
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Log file path
LOG_FILE_PATH = os.path.join(LOG_DIR, "logfile.log")

# Configure logging
logging.basicConfig(
    filename=LOG_FILE_PATH,  # Always save logs in ToolsQA_Automation_Suite/logs/
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Add a console handler to print logs to the console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logging.getLogger().addHandler(console_handler)

# Debugging: Print the resolved log path
logging.info(f"Logging initialized. Log file: {LOG_FILE_PATH}")
print(f"Log file created at: {LOG_FILE_PATH}")
