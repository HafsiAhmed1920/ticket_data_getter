from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.edge import service
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from retry import retry  # Install this library using: pip install retry


@retry(ConnectionRefusedError, tries=3, delay=2)
def connect():
    edgeOption = webdriver.EdgeOptions()
    edgeOption.use_chromium = True
    edgeOption.add_argument("start-maximized")
    edgeOption.add_argument("--disable-gpu")
    edgeOption.add_argument("--headless")  # Added headless argument
    edgeOption.add_argument("--no-sandbox")
    edgeOption.add_argument("--disable-dev-shm-usage")
    # to be changed with your locale directory's msdge path check the same path  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #if your path contains spaces put % instead of spaces !!!!!!!!!!!!!!!!!!!!!!!!!!
    edgeOption.binary_location = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    s = service.Service(r'C:\edgedriver_win64\msedgedriver.exe')
    driver = webdriver.Edge(service=s, options=edgeOption)
    return driver



def Inject_login_cookies(driver):
    cookies_dict = {}
    cookies_dict["ARRAffinitySameSite"] = "402fc1fc19f8bb6f08337cb84108f0843dd4e5826f326686893b4dda90f82731"
    cookies_dict["Bearer"] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9uYW1laWRlbnRpZmllciI6IjEwMzczIiwiQ29ubmVjdGl2aXR5IjoiMSIsIlVzZXJOYW1lIjoiay56b2dobGFtaUBhcmlvbi10ZWNoLmNvbSIsIkRpc3BsYXlOYW1lIjoiay56b2dobGFtaTEiLCJFbWFpbCI6Imsuem9naGxhbWlAYXJpb24tdGVjaC5jb20iLCJJc19BZ2VudCI6IkZhbHNlIiwiSXNfQ2xpZW50IjoiRmFsc2UiLCJhY2Nlc3NfdG9rZW5fY29udHJhY3RzIjoiIiwiZXhwIjoxNzMyNDQzNjQ1LCJpc3MiOiJUaW1zb2Z0LmNvbSIsImF1ZCI6IlRpbXNvZnQuY29tIn0.bDtuYrbPuxYR_ZIOT2Uw2LYrJCwNy55TCUAdJPt3otc"
    for cookie_name, cookie_value in cookies_dict.items():
        driver.add_cookie({'name': cookie_name, 'value': cookie_value})


def get_current_page(driver):
    pagination = driver.find_element(By.CLASS_NAME, "pagination")
    current_page = pagination.find_element(By.XPATH, '//li[contains(@class, "active")]/a').text
    return int(current_page)


def click_next_button(driver):
    non_active_pages_xpath = '//li[not(contains(@class, "active"))]/a[@class="page-link"]'
    non_active_pages = driver.find_elements(By.XPATH, non_active_pages_xpath)
    for page in non_active_pages:
        if page.text == str(get_current_page(driver) + 1):
            page.click()
            return True
    return False

