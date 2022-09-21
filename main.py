import time

from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import openpyxl


def crawling():
    driver = webdriver.Chrome()
    driver.get("http://www.yes24.com/24/Category/Display/001001025007")

    wb = openpyxl.Workbook()
    sheet = wb.active

    time.sleep(1)

    title_button = driver.find_element(By.XPATH, '//*[@id="category_layout"]/ul/li[1]/div/div[1]/div[2]/a[1]')
    title_button.click()

    book_title = driver.find_element(By.CLASS_NAME, 'gd_name').text
    book_auth = driver.find_element(By.CLASS_NAME, 'gd_auth').text
    row_list = [book_title, book_auth]
    content_text = driver.find_element(By.XPATH, '//*[@id="infoset_inBook"]/div[2]/div[1]/div[1]').text
    content_text_split_list = content_text.split('\n\n')

    for text in content_text_split_list:
        row_list.append(text)

    sheet.append(row_list)
    sheet.append(row_list)

    wb.save("test.csv")

    driver.back()


if __name__ == '__main__':
    crawling()
