"""
@author: Joseph A.
Description: Main orchestration script that runs data extraction (eda.py) and analysis (stats.py) 
while managing logging and error handling.
"""
import os
import subprocess
import sys
import logging
from datetime import datetime

def setup_logging():
    """Configure logging to output both to console and file.
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(f'logs/execution_{datetime.now().strftime("%Y%m%d")}.log')
        ]
    )

def run_script(script_name:str):
    """Execute a Python script and handle potential errors.

    Args:
        script_name (str): Name of the Python script to execute

    Returns:
        bool: True if script execution was successful, False otherwise
    """
    try:
        logging.info("Starting %s", script_name)
        subprocess.run([sys.executable, script_name], check=True, capture_output=True, text=True)
        logging.info("Execution of %s completed successfully", script_name)
        return True
    except subprocess.CalledProcessError as e:
        logging.error("Error when executing %s: %s", script_name, e)
        logging.error("Stdout %s", e.stdout)
        logging.error("Stderr %s", e.stderr)
        return False

def main():
    """Main function orchestrating the data pipeline.
    """
    # Create logs directory
    os.makedirs('logs', exist_ok=True)

    # Logging configuration
    setup_logging()
    logging.info("Start of data update and analysis process")

    # Execute data extraction
    if not run_script('eda.py'):
        logging.error("Data update failed. Process stopped.")
        sys.exit(1)

    # Execute data analysis
    if not run_script("stats.py"):
        logging.error("Failed data analysis.")
        sys.exit(1)

    logging.info("Process successfully completed")

if __name__ == "__main__":
    main()
