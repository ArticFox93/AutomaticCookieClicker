from selenium import webdriver
from selenium.webdriver.common.by import By
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)

driver.get("https://orteil.dashnet.org/experiments/cookie/")

# get cookies
cookie = driver.find_element(By.ID, value="cookie")

# get upgrade items
items = driver.find_elements(By.CSS_SELECTOR, value="#store div")
items_ids = [item.get_attribute("id") for item in items]

timeout = time.time() + 5
five_min = time.time() + 5*60 # 5 minutes

while True:
    cookie.click()

    if time.time() > timeout:
        all_prices = driver.find_elements(By.CSS_SELECTOR, value="#store b")
        item_prices = []

        # convert <b> into integer
        for price in all_prices:
            element_text = price.text
            if element_text != "":
                cost = int(element_text.split("-")[1].strip().replace(",", ""))
                item_prices.append(cost)

        # create a dictionary of store items and prices
        cookie_upgrader = {}
        for n in range(len(item_prices)):
            cookie_upgrader[item_prices[n]] = items_ids[n]

        # get current cookie amount
        money = driver.find_element(By.ID, value="money").text
        if "," in money:
            money = money.replace(",", "")
        cookie_count = int(money)

        # find upgrades that we can afford
        affordable_upgrades = {}
        for cost, id in cookie_upgrader.items():
            if cookie_count > cost:
                affordable_upgrades[cost] = id

        # purchase the most expensive upgrade
        highest_price_affordable_upgrade = max(affordable_upgrades)
        to_purchase_id = affordable_upgrades[highest_price_affordable_upgrade]

        driver.find_element(By.ID, value=to_purchase_id).click()

        timeout = time.time() + 5

    if time.time() > five_min:
        cookie_per_s = driver.find_element(By.ID, value="cps").text
        print(cookie_per_s)
        break