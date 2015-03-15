from selenium import webdriver
import unittest
import login



HTTP_ACCESS = '' #username:password@ OR leave empty if no http authentication
DOMAIN = '' #domain name (not prefixed by 'http://'' or 'www')
URL = 'http://%s%s' %(HTTP_ACCESS, DOMAIN)
USERNAME = '' #username / user_email
PASSWORD = '' #password
BROWSERS = {'firefox': webdriver.Firefox, 'chrome': webdriver.Chrome}

class BlacklaneTest(unittest.TestCase):
  
  @classmethod
  def setUp(cls):
    cls.driver = BROWSERS['firefox']()
    cls.driver.maximize_window()
    cls.user_login = login.UserLogin(cls.driver)
      
  def test_login_with_correct_credentials(self):
    ul = self.user_login
    ul.driver.get(URL)
    ul.login_button.click()
    ul.submit_credentials(USERNAME, PASSWORD)
    self.assertTrue(ul.check_login_successful())

  def test_login_with_incorrect_credentials(self):
    ul = self.user_login
    ul.driver.get(URL)
    ul.login_button.click()
    ul.submit_credentials('mxmx@yaho.com', 'PASSWORD')
    self.assertTrue(ul.check_login_unsuccessful())

  @classmethod
  def tearDown(cls):
    cls.driver.close()

if __name__ == "__main__":
  unittest.main()
