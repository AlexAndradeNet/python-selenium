"""Module for testing the Blankfactor's blog."""

import time

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

# Create Chrome options
options = Options()
options.add_argument("--headless")  # Enable headless mode
options.add_argument("--disable-gpu")  # Necessary on some systems

# Create a WebDriver instance
driver = webdriver.Chrome(options=options)


def wait_for_element(by_object, value, timeout=10):
    """Function for wait until the element is present"""
    return WebDriverWait(driver, timeout).until(
        expected_conditions.presence_of_element_located((by_object, value))
    )


def wait_for_elements(by_object, value, timeout=10):
    """Function for wait until for multi-element is present"""
    return WebDriverWait(driver, timeout).until(
        expected_conditions.presence_of_all_elements_located((by_object, value))
    )


def wait_for_page_full_loaded():
    """Function for wait until the page is loaded"""
    WebDriverWait(driver, 10).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )


def main():
    """Main function"""
    try:
        # Navigate to the specified URL and wait for it to load
        driver.get("https://blankfactor.com")
        wait_for_page_full_loaded()

        # Dismiss GDPR dialog if it appears
        gdpr_buttons = wait_for_elements(By.ID, "hs-eu-confirmation-button")
        if gdpr_buttons:
            gdpr_buttons[0].click()

        # Click on the search button
        search_toggle = wait_for_element(By.CSS_SELECTOR, ".search-toggle")
        search_toggle.click()

        # Type "blog" in the search field
        search_box = wait_for_element(By.CSS_SELECTOR, ".ais-SearchBox-input")
        search_box.send_keys("Why fintech in Latin America is booming")

        time.sleep(1)

        # Click on the blog link
        element_tag = '//li[@class="ais-Hits-item"]/a[contains(., "{}")]'
        element_tag = element_tag.format("Why fintech in Latin America is booming")
        blog_link = wait_for_element(
            By.XPATH,
            element_tag,
        )
        blog_link.click()

        # Validate that you are on the correct page
        print(f"URL: {driver.current_url}")
        assert (
            "https://blankfactor.com/insights/blog/fintech-in-latin-america/"
            in driver.current_url
        )
        assert (
            "Latin America has been a fertile ground for fintech investment"
            in driver.page_source
        )

        # Subscribe to the newsletter using the subscription form
        email_input = wait_for_element(
            By.CSS_SELECTOR, 'input[placeholder="Your email address"]'
        )
        email_input.send_keys("your_email@domain.com")
        subscribe_button = wait_for_element(
            By.CSS_SELECTOR, "#form-newsletter-blog-submit-btn"
        )
        subscribe_button.click()

        # Go back to the blog section
        driver.get("https://blankfactor.com/insights/blog/")

        # Get and print a list of all post titles with related links
        blog_posts = wait_for_elements(
            By.XPATH, '//*[@class="heading-4 post-title"]', timeout=20
        )

        for post in blog_posts:
            try:
                title = post.text
                link = post.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                print(f"Title: {title}\nLink: {link}")
            except NoSuchElementException as ex:
                print(f"Error fetching post details: {ex}")

    finally:
        # Close the browser
        driver.quit()
