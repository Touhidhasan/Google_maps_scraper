from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
import time
import csv
import undetected_chromedriver as uc


class GoogleMapsScraper:
    def __init__(self):
        # Initialize the Chrome driver with options to disable images
        chrome_options = webdriver.ChromeOptions()
        self.driver = uc.Chrome(use_subprocess=True)

    def open_google_maps(self):
        # Navigate to Google Maps with specific coordinates
        self.driver.get("https://www.google.com/maps/@50.8248567,4.7978348,8z?hl=en&entry=ttu")
        time.sleep(5)

    def search_places(self, query):
        # Search for places in Google Maps
        search = self.driver.find_element(By.ID, "searchboxinput")
        search.send_keys(query)
        time.sleep(8)

        search_btn = self.driver.find_element(By.ID, "searchbox-searchbutton")
        search_btn.click()
        time.sleep(5)

    def scroll(self):
        # Scroll the results to load more places
        div_item = self.driver.find_element(By.XPATH,
                                            '/html/body/div[1]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]')
        div_item.send_keys(Keys.PAGE_UP)
        time.sleep(2)
        div_item.send_keys(Keys.PAGE_DOWN)
        time.sleep(2)
        print("Scrolling...")

    def extract_data(self, index):
        # Extract data for a specific place from Google Maps
        try:
            item = self.driver.find_element(By.XPATH,
                                            f'/html/body/div[1]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]/div[{index}]/div/a')
            item.click()
            time.sleep(7)

            # Extract the name, address, website, and phone number
            name = self.get_element_text(By.XPATH,
                                         '/html/body/div[1]/div[3]/div[8]/div[9]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[2]/div/div[1]/div[1]/h1')
            address = self.get_element_text(By.XPATH, '//*[@data-item-id="address"]/div/div[2]/div[1]')
            website = self.get_element_text(By.XPATH, '//*[@data-item-id="authority"]/div/div[2]/div[1]')
            phone = self.get_element_text(By.XPATH, '//*[@data-tooltip="Copy phone number"]/div/div[2]/div[1]')

            # Log the extracted information
            print(f"Name: {name}, Address: {address}, Website: {website}, Phone: {phone}")

            # Save data to CSV
            self.save_to_csv(name, website, address, phone)

            return True  # Successful extraction
        except Exception as e:
            print(f"Error extracting data at index {index}: {e}")
            return False

    def get_element_text(self, by, value):
        # Helper function to safely get the text of an element
        try:
            element = self.driver.find_element(by, value)
            return element.text
        except:
            return ""

    def save_to_csv(self, name, website, address, phone):
        # Save the extracted data to a CSV file
        with open('output.csv', 'a', newline='', encoding="utf-8-sig") as file:
            writer = csv.writer(file)
            writer.writerow([name, website, address, phone])

    def run(self):
        # Main method to run the scraper
        self.open_google_maps()
        #Enter any keyword for search, Ex: lounges in Miami, FL
        self.search_places("lounges in Miami, FL")

        index = 3
        while index < 10000:
            print(f"Processing index: {index}")
            if not self.extract_data(index):
                self.scroll()  # Scroll if extraction failed
            index += 2
            time.sleep(1)

    def close(self):
        # Close the Chrome driver
        self.driver.quit()


if __name__ == "__main__":
    scraper = GoogleMapsScraper()
    try:
        scraper.run()
    finally:
        scraper.close()  # Ensure the driver is closed when done
