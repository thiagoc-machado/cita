# Web Automation Project

This project aims to automate the process of accessing a website, filling out a form, taking a screenshot, solving a captcha, and sending an SMS notification. The primary technologies used in this project are Python, Selenium WebDriver, OpenCV, Tesseract OCR, Twilio, and PyInstaller.

## Features

- Navigates to a specific website using Selenium WebDriver
- Fills out a form with data and submits it
- Takes a screenshot of the entire webpage, including a captcha image
- Crops the captcha image from the screenshot using OpenCV
- Processes the captcha image to improve OCR recognition
- Uses Tesseract OCR to recognize characters in the captcha image
- Solves the captcha and submits the form
- Sends an SMS notification via Twilio upon successful form submission
- Loads configuration values from a `.env` file
- Can be packaged as a standalone Windows application using PyInstaller

## Requirements

- Python 3.6 or higher
- Selenium WebDriver
- Google Chrome or another supported browser
- ChromeDriver or another compatible WebDriver
- OpenCV
- Tesseract OCR
- Pytesseract
- Twilio
- python-dotenv

## Installation

Clone the repository or download the project files.
Create a virtual environment and activate it.
Install the required packages using pip install -r requirements.txt.
Install Tesseract OCR on your computer following the official documentation.
Place a valid .env file in the project directory with the necessary API keys and configuration values.
Run the script using python main.py (or your preferred method for running Python scripts).

## Usage

Follow the installation steps to set up the project. Once the script is running, it will automate the process of navigating to the website, filling out the form, solving the captcha, and sending an SMS notification. You can customize the script to suit your specific needs by modifying the form fields, captcha processing, and other parts of the code.

## Contributing

Feel free to fork the repository and submit pull requests with your improvements and bug fixes. You can also open issues to report bugs or request new features.

## License

This project is licensed under the MIT License. See the LICENSE file for more information.