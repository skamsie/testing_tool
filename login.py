from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import os
import unittest
import time
import json
import sys

class UserLogin(object):
  def __init__(self, driver):
    self.driver = driver
  
  @property
  def login_button(self):
    return self.driver.find_element_by_css_selector('a.btn-login')
  
  @property
  def email_field(self):
    return self.driver.find_element_by_id('session_email')

  @property
  def password_field(self):
    return self.driver.find_element_by_id('session_password')
  
  @property
  def submit_login_button(self):
    return self.driver.find_element_by_xpath("//input[@name='commit' and @value='Log in']")
 
  @property
  def login_successful_message(self):
    return EC.text_to_be_present_in_element((By.CLASS_NAME, "flash-message-notice"), 'Login successful')

  @property
  def invalid_credentials_message(self):
    return EC.presence_of_element_located((By.ID, "session_email-error"))

  def submit_credentials(self, email, password):
    self.email_field.send_keys(email)
    self.password_field.send_keys(password)
    self.submit_login_button.click()

  def check_login_successful(self):
    return WebDriverWait(self.driver, 10).until(self.login_successful_message)

  def check_login_unsuccessful(self):
    return WebDriverWait(self.driver, 10).until(self.invalid_credentials_message)


class CookiesLogin(UserLogin):
  
  def __init__(self, driver, url, username, password):
    super(CookiesLogin, self).__init__(driver)

    self.driver = driver
    self.url = url
    self.username = username
    self.password = password
    
    for i in ['firefox', 'chrome']:
      if i in str(self.driver):
        browser = i

    self.cookies_filename = '%s**%s**%s.json' % (self.username, self.url.split('@')[-1], browser)
    self.cookies_path = os.path.join(os.path.dirname(__file__), 'cookies', self.cookies_filename)
  
  def __cookies_file_exists(self):
    if os.path.exists(self.cookies_path):
      return True
    else:
      if not os.path.exists(os.path.dirname(self.cookies_path)):
        os.makedirs(os.path.dirname(self.cookies_path))
      return False

  def __create_cookies(self):
    self.driver.get(self.url)
    self.login_button.click()
    self.submit_credentials(self.username, self.password)
    self.check_login_successful()
    cookies = self.driver.get_cookies()
    with open(self.cookies_path, "w") as outfile:
      json.dump({'cookies': cookies}, outfile, indent=4)
  
  def __load_cookies(self):
    with open(self.cookies_path, "r") as infile:
      data = json.load(infile)
    self.driver.get(URL)
    for i in data['cookies']:
      self.driver.add_cookie(i)
    self.driver.refresh()
  
  def login(self):
    if self.__cookies_file_exists():
      self.__load_cookies()
    else:
      self.__create_cookies()

