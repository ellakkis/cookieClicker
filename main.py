import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get('http://orteil.dashnet.org/experiments/cookie/')
cookie = driver.find_element(By.ID, 'cookie')


def buy_item(upgrade):
    driver.find_element(By.ID, 'buy'+upgrade[0]).click()


def check_money():
    my_money = driver.find_element(By.ID, 'money')
    current_money = int(my_money.text.replace(',', ''))
    return current_money


def check_store():
    store_items = driver.find_elements(By.CSS_SELECTOR, "#store div b")
    store_items.pop()
    store = [item.text for item in store_items]
    upgrades = []
    for item in store_items:
        upgrades.append([
            item.text.split('-')[0].strip(),
            int((item.text.split('-')[1]).replace(',', ''))
        ])
    money = check_money()
    for n in reversed(range(len(upgrades))):
        if upgrades[n][1] < money:
            buy_item(upgrades[n])
            break


timeout = time.time() + 5
five_min = time.time() + 60*5  # 5minutes

while True:
    cookie.click()
    if time.time() > timeout:
        check_store()
        timeout += 10