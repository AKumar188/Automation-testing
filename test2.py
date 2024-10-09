import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from tabulate import tabulate

edge_driver_path = os.path.join(current_dir, 'drivers', 'msedgedriver.exe')
edge_service = Service(executable_path=edge_driver_path)
# Define the test cases (caseid, URL, username, password)
test_cases = [
    (1, "https://www.saucedemo.com/", "standard_user", "secret_sauce"),
    (2, "https://www.saucedemo.com/", "locked_out_user", "secret_sauce"),
    (3, "https://www.saucedemo.com/", "problem_user", "secret_sauce"),
    (4, "https://www.saucedemo.com/", "performance_glitch_user", "secret_sauce"),
    (5, "https://www.saucedemo.com/", "invalid_user", "invalid_password")
]

# Results list to store the outcomes
results = []

# Initialize the EdgeDriver with the Service object
driver = webdriver.Edge(service=edge_service)
driver.maximize_window()

# Run each test case
for caseid, url, username, password in test_cases:
    try:
        # Open the website
        driver.get(url)
        time.sleep(2)


        # Locate the username field and enter the username
        username_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "user-name")))
        username_field.send_keys(username)

        # Locate the password field and enter the password
        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys(password)

        # Locate the login button and click it
        login_button = driver.find_element(By.ID, "login-button")
        time.sleep(2)
        login_button.click()
        time.sleep(2)

        # Wait for the login to complete
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_list")))

        # If successful, the inventory list should be visible
        success_indicator = driver.find_element(By.CLASS_NAME, "inventory_list")
        if success_indicator.is_displayed():
            results.append((caseid, username, password, "Pass"))
        else:
            results.append((caseid, username, password, "Fail"))
    except Exception as e:
        results.append((caseid, username, password, "Fail"))
        print(f"Test case {caseid} failed: {e}")

# Additional test case for adding items to the cart, proceeding to checkout, and completing the purchase
try:
    driver.get("https://www.saucedemo.com/")

    # Login with standard_user
    username_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "user-name")))
    username_field.send_keys("standard_user")
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys("secret_sauce")
    login_button = driver.find_element(By.ID, "login-button")
    time.sleep(2)
    login_button.click()

    # Wait for the login to complete
    time.sleep(5)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_list")))

    # Add the first two items to the cart
    add_to_cart_buttons = driver.find_elements(By.CLASS_NAME, "btn_inventory")
    for i in range(4):
        add_to_cart_buttons[i].click()
    
    time.sleep(2)

    # Go to the cart
    cart_button = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
    cart_button.click()
    time.sleep(2)


    # Proceed to checkout
    checkout_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "checkout")))
    checkout_button.click()
    time.sleep(2)


    # Enter the first name, last name, and postal code
    first_name_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "first-name")))
    first_name_field.send_keys("Alok")
    last_name_field = driver.find_element(By.ID, "last-name")
    last_name_field.send_keys("Anand")
    postal_code_field = driver.find_element(By.ID, "postal-code")
    postal_code_field.send_keys("560098")
    time.sleep(2)


    # Continue to the next step
    continue_button = driver.find_element(By.ID, "continue")
    continue_button.click()


    # Wait for 5 seconds and then click on finish
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "finish")))
    time.sleep(2)
    # Scroll down by 1000 pixels
    driver.execute_script("window.scrollBy(0, 1000);")
    time.sleep(2)

    finish_button = driver.find_element(By.ID, "finish")
    finish_button.click()

    # Wait for 5 seconds
    time.sleep(5)
except Exception as e:
    print(f"Additional test case failed: {e}")

# Close the browser
driver.quit()

# Create a DataFrame to hold the results
df = pd.DataFrame(results, columns=["Case ID", "Username", "Password", "Login Result"])

# Print the results using tabulate for a nicely formatted table
print(tabulate(df, headers='keys', tablefmt='grid'))
