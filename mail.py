import os
import time
import random
from faker import Faker
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import argparse

# Initialize Faker for random data generation
fake = Faker()

# Generate a requirements.txt file function
def generate_requirements_file():
    requirements = [
        "selenium",
        "faker"
    ]
    with open("requirements.txt", "w") as f:
        f.write("\n".join(requirements))
    print("Generated requirements.txt with the necessary dependencies.")

# Function to save generated credentials before account creation
def save_pre_generated_credentials(credentials):
    with open("pre_credentials.txt", "a") as f:
        f.write(f"Email: {credentials['email']}, Password: {credentials['password']}, "
                f"First Name: {credentials['first_name']}, Last Name: {credentials['last_name']}\n")
    print(f"Pre-generated credentials saved for {credentials['email']}")

# Function to save verified credentials after successful account creation
def save_verified_credentials(credentials):
    with open("verified_accounts.txt", "a") as f:
        f.write(f"Email: {credentials['email']}, Password: {credentials['password']}\n")
    print(f"Verified account saved for {credentials['email']}")

# Function to generate random credentials
def generate_random_credentials():
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = fake.user_name() + random.choice(["@mail.com", "@email.com", "@randommail.com"])
    password = fake.password()
    
    credentials = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": password
    }
    return credentials

# Function to fill out and submit the mail.com sign-up form
def fill_and_submit_form(driver, credentials):
    try:
        # Locate form fields and fill them with credentials
        driver.find_element(By.NAME, "first_name").send_keys(credentials["first_name"])
        driver.find_element(By.NAME, "last_name").send_keys(credentials["last_name"])
        driver.find_element(By.NAME, "email").send_keys(credentials["email"])
        driver.find_element(By.NAME, "password").send_keys(credentials["password"])
        
        # Simulate the form submission (adjust according to actual HTML)
        driver.find_element(By.ID, "submit_button_id").click()
        print(f"Form submitted for {credentials['email']}")
        
        time.sleep(5)  # Wait for account creation process

        # Confirm that the account was created successfully (adjust for actual success criteria)
        if "confirmation" in driver.page_source:
            print(f"Account creation successful for {credentials['email']}")
            return True
        else:
            print(f"Account creation failed for {credentials['email']}")
            return False
    except Exception as e:
        print(f"Error during account creation: {e}")
        return False

# Function to automate the account creation process
def create_email_account(num_accounts):
    # Set up Chrome in headless mode for Google Codespaces
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Path to ChromeDriver in Codespaces
    chrome_service = Service('/usr/bin/chromedriver')

    # Create WebDriver instance with the headless Chrome browser
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    
    # Open the mail.com sign-up page
    driver.get("https://signup.mail.com/#.7518-header-signup1-1")
    
    # Create the specified number of accounts
    for i in range(num_accounts):
        print(f"Creating account {i+1}/{num_accounts}...")

        # Generate random credentials
        credentials = generate_random_credentials()

        # Save pre-generated credentials before account creation
        save_pre_generated_credentials(credentials)

        # Fill out the form and submit it
        success = fill_and_submit_form(driver, credentials)

        # If account creation was successful, save verified credentials
        if success:
            save_verified_credentials(credentials)

        # Add a small delay between account creations
        time.sleep(2)
    
    driver.quit()

# Set up CLI interface
def main():
    parser = argparse.ArgumentParser(description="Automate mail.com account creation.")
    parser.add_argument(
        "--accounts",
        type=int,
        help="Number of accounts to create",
        required=True
    )
    
    args = parser.parse_args()
    
    # Generate requirements.txt file
    generate_requirements_file()
    
    # Start the account creation process
    create_email_account(args.accounts)

# Run the script from the command line
if __name__ == "__main__":
    main()
