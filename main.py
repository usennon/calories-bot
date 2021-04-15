from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import csv

CHROME_DRIVER_PATH = r'C:\Users\Hooin Kema\Development\chromedriver.exe'


class CaloriesParser:
    def __init__(self, path=CHROME_DRIVER_PATH):
        self.driver = webdriver.Chrome(executable_path=path)
        self.driver.get('https://www.nutritionvalue.org/Pasta%2C_enriched%2C_dry_nutritional_value.html')

    def get_table_items(self):
        button = self.driver.find_element_by_xpath(xpath='//*[@id="main"]/tbody/tr[2]/td/form/input')
        search = self.driver.find_element_by_id('food_query')
        user_input = input('Enter product name: ')
        search.send_keys(user_input)
        button.click()
        sleep(6)
        table_list = self.driver.find_elements_by_class_name('table_item_name')[:5]
        return table_list


parser = CaloriesParser()

while True:
    sleep(5)
    table_items = parser.get_table_items()
    if not table_items:
        print('Seems such product does not exist. Try again!')
        parser.driver.back()
        continue
    else:

        for item in table_items:
            print(str(int(table_items.index(item)) + 1) + item.text)

        choice = input('Choose your item: from 1 to 5.')
        if int(choice) in range(1, 6):

            break
print(table_items)
item_name = table_items[int(choice) - 1].text
table_items[int(choice) - 1].click()
sleep(5)

webdriver.ActionChains(parser.driver).send_keys(Keys.ESCAPE).perform()

sleep(2)
calories = parser.driver.find_element_by_xpath(xpath='//*[@id="main"]/tbody/tr[4]/td/table/tbody/tr[3]/td['
                                                     '1]/table/tbody/tr/td/table/tbody/tr[5]/td[2]')


with open('food-calories.csv', mode='a+') as csv_file:
    fieldnames = ['Product_name', 'Calories']

    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writerow({'Product_name': f'{item_name}',
                     'Calories': f'{calories.text}'})