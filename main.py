import time

from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE
import openpyxl


def crawling():
    driver = webdriver.Chrome()
    driver.get("http://www.yes24.com/24/Category/Display/001001019016?PageNumber=1")

    wb = openpyxl.Workbook()
    sheet = wb.active

    time.sleep(1)

    page_count = 1

    for page in range(0, 45):
        category_layout = driver.find_element(By.ID, 'category_layout')
        book_list_ul_tag = category_layout.find_element(By.TAG_NAME, 'ul')
        book_list = book_list_ul_tag.find_elements(By.TAG_NAME, 'li')
        for i in range(0, len(book_list)):
            try:
                time.sleep(1)
                category_layout = driver.find_element(By.ID, 'category_layout')
                book_list_ul_tag = category_layout.find_element(By.TAG_NAME, 'ul')
                book = book_list_ul_tag.find_elements(By.TAG_NAME, 'li')[i]
                title_button = book.find_element(By.CLASS_NAME, 'goods_name').find_element(By.TAG_NAME, 'a')
                title_button.click()
                book_title = driver.find_element(By.CLASS_NAME, 'gd_name').text
                book_auth = driver.find_element(By.CLASS_NAME, 'gd_auth').text
                # print(book_title)
                # print(book_auth)
                row_list = [book_title, book_auth]
                try:
                    content_text = driver.find_element(By.XPATH, '//*[@id="infoset_inBook"]/div[2]/div[1]/div[1]').text
                    # print(content_text)
                    content_text_split_list = content_text.split('\n\n')
                    for text in content_text_split_list:
                        # print(text)
                        text = ILLEGAL_CHARACTERS_RE.sub(r'', text)
                        row_list.append(text)
                    # TODO 얘가 문제임; 왠지 모르겠음.
                    # https://cindycho.tistory.com/49 해결 방법
                    sheet.append(row_list)
                    wb.save("test.csv")
                    driver.back()
                except Exception:
                    sheet.append(row_list)
                    wb.save("test.csv")
                    driver.back()

            except Exception as e:
                print(e)
        time.sleep(0.5)
        try:
            page_container_xpath = driver.find_element(By.XPATH,
                                                       '//*[@id="cateSubWrap"]/div[2]/div[6]/div[2]/span[1]/div')
            page_list_a = page_container_xpath.find_elements(By.TAG_NAME, 'a')
            if page_count % 10 == 0:
                print("다음페이지 클릭")
                next_page_button = driver.find_element(By.XPATH,
                                                       '//*[@id="cateSubWrap"]/div[2]/div[6]/div[2]/span[1]/div/a[12]')
                next_page_button.click()
                page_count += 1
                continue
            page_count += 1
            for i in page_list_a:
                if i.text == str(page_count):
                    i.click()
                    break

        except Exception as e:
            print("pagenation Error : " + str(e))


if __name__ == '__main__':
    crawling()
