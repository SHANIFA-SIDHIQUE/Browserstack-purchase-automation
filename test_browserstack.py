import pytest
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging


class TestBrowserstack():
    @pytest.fixture
    def setup(self):
       self.driver = webdriver.Chrome()
       self.driver.maximize_window()
       self.driver.get("https://bstackdemo.com/")
       yield self.driver
       self.driver.quit()

    def login(self, driver):
        sign_in = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "signin")))
        sign_in.click()

        user_name = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.ID, "username")))
        user_name.click()
        time.sleep(5)

        user_list = WebDriverWait(driver, 10).until(
            EC.visibility_of_all_elements_located((By.CLASS_NAME, "css-yt9ioa-option"))
        )

        for user in user_list:
            # print(user.text)
            if user.text == "fav_user":
                user.click()
                break

        password = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.ID, "password")))
        password.click()

        password_li = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "react-select-3-option-0-0"))
        )
        password_li.click()

        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='login-btn']"))
        )
        button.click()

        time.sleep(10)

        WebDriverWait(driver, 35).until(
            EC.url_contains("https://bstackdemo.com/?signin=true")
        )
        assert driver.current_url == "https://bstackdemo.com/?signin=true"
        logging.info("[INFO]successfully logged in as expected..")


    def test_login(self,setup):
        driver = setup
        self.login(driver)

    def test_purchase_product(self,setup):
        driver = setup
        self.login(driver)

        search_field = WebDriverWait(self.driver,20).until(
            EC.visibility_of_element_located((By.XPATH,"//*[@id='__next']/div/div/div[1]/div/div/div[2]/div/input"))
        )
        search_field.send_keys("iphone 12")
        search_button = WebDriverWait(self.driver,10).until(
            EC.element_to_be_clickable((By.XPATH,"//*[@id='__next']/div/div/div[1]/div/div/div[2]/div/button"))
        )
        search_button.click()
        time.sleep(3)

        add_to_cart_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH,"//*[@id='1']/div[4]"))
        )
        add_to_cart_button.click()


        checkout_btn = WebDriverWait(driver,20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,".buy-btn"))
        )
        checkout_btn.click()

        Firstname = WebDriverWait(driver,20).until(
            EC.visibility_of_element_located((By.ID,"firstNameInput"))
        )
        Firstname.send_keys("Rahul")
        Lastname = WebDriverWait(driver,20).until(
            EC.visibility_of_element_located((By.ID,"lastNameInput"))
        )
        Lastname.send_keys("Manoj")
        address = WebDriverWait(driver,20).until(
            EC.visibility_of_element_located((By.ID,"addressLine1Input"))
        )
        address.send_keys("Nest")
        state = WebDriverWait(driver,20).until(
            EC.visibility_of_element_located((By.ID,"provinceInput"))
        )
        state.send_keys("Kerala")
        postal = WebDriverWait(driver,20).until(
            EC.visibility_of_element_located((By.ID,"postCodeInput"))
        )
        postal.send_keys("670593")
        submit_btn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='checkout-shipping-continue']"))
        )
        submit_btn.click()
        time.sleep(5)

        confirmation_message = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//*[@id='confirmation-message']"))
        )
        assert "Your Order has been successfully placed!." in confirmation_message.text

