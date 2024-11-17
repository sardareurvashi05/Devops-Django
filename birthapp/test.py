from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

class LoginFormTest(LiveServerTestCase):
    def testform(self):
        driver = webdriver.Chrome()
        driver.get('http://127.0.0.1:8000/accounts/login/')
        
        time.sleep(3)
        
        user_name = driver.find_element(By.NAME, 'username')
        user_password = driver.find_element(By.NAME, 'password')

        time.sleep(3)

        user_name.send_keys('urvashisardare05')
        user_password.send_keys('national12345')
        user_password.submit()

        assert 'Welcome urvashisardare05' in driver.page_source