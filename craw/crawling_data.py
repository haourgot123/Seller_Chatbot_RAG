import argparse
import logging
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from time import sleep


logging.basicConfig(
    filename='logs/app.log', 
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logging.info("------Log từ file crawling_data.py. --------")


def chrome_webdriver():
    chromedriver_path = '/usr/local/bin/chromedriver'
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                'Chrome/123.0.0.0 Safari/537.36'
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    #  options.add_argument('--headless')
    options.add_argument(f'user-agent={user_agent}')
    service = Service(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def show_more(browser, class_name):
    '''
        Click tự động vào nút hiện thị thêm
    '''
    try:
        while 1:
            show_more = browser.find_element(By.CLASS_NAME, class_name)
            show_more.find_element(By.TAG_NAME, 'a').click()
            sleep(5)
    except Exception as e:
        logging.warning(f'Can not find HTML element {e}')


def craw_product_link(browser, class_name, output_filename):
    '''
        Craw dữ liệu về tên sản phầm và đường link sản phẩm
    '''
    try:
        productions_link =  []
        products = browser.find_elements(By.CLASS_NAME, class_name)
        for product in products:
            product_link = product.find_element(By.TAG_NAME, 'a').get_attribute('href')
            product_name = product.find_element(By.TAG_NAME, 'h3').text
            productions_link.append(
                {
                    'product_name': product_name,
                    'product_link': product_link
                }
            )
        productions_link = pd.DataFrame(productions_link)
        productions_link.to_csv(f'{output_filename}', index = False)
        return productions_link
    except Exception as e:
        logging.error(f'Error when run craw_product_link function {e}')



def craw_product_info(browser, url):
    '''
        Truy cập vào link sản phẩm và craw dữ liệu chi tiết về sản phẩm.
    '''
    try:
        browser.get(url)
        sleep(5)
        # Craw item name
        item_name = browser.find_element(By.CLASS_NAME, 'header-name')
        item_name = item_name.find_element(By.TAG_NAME, 'h1').text
        # Craw color price
        origin_price = browser.find_elements(By.CLASS_NAME, 'LastPrice')
        if not origin_price:
            origin_price = ''
        else:
            origin_price = origin_price[0].text
        color_price_items = browser.find_elements(By.CLASS_NAME, 'color-price')
        color_prices = []
        for color_price in color_price_items:
            color = color_price.find_element(By.TAG_NAME, 'span').text
            price = color_price.find_elements(By.TAG_NAME, 'p')
            if not price:
                price = browser.find_element(By.CLASS_NAME, 'box-price').find_element(By.TAG_NAME, 'strong').text
            else:
                price = price[0].text
            color_prices.append(
                f'Màu: {color} - Giá: {price}'
            )
        # Craw technical info
        technical_infomation = []
        browser.find_element(By.CLASS_NAME, 'ajax-modal-show').click()
        sleep(2)
        technicals_info = browser.find_element(By.CLASS_NAME, 'text-align-start')
        technicals_info = technicals_info.find_elements(By.CLASS_NAME, 'specs-item')
        for technical_info in technicals_info:
            technical_title = technical_info.find_element(By.CLASS_NAME, 'title').text
            technicals_content = technical_info.find_elements(By.TAG_NAME, 'li')
            technicals_data = ''
            for technical_content in technicals_content:
                technical_content_title = technical_content.find_element(By.TAG_NAME, 'strong').text
                technical_content_data = technical_content.find_element(By.TAG_NAME, 'span').text
                technicals_data += f'{technical_content_title}: {technical_content_data}\n'
            technical_infomation.append(
                f'{technical_title}: [{technicals_data}]'
            )
        
        product_info = {
            'url': url,
            'item_name': item_name,
            'origin_price': origin_price,
            'color_price': color_prices,
            'technical_infomation': technical_infomation
        }
        return product_info

    except Exception as e:
        logging.warning(f'Warning using craw_product_info function {e}') 


class WebCrawler:
    def __init__(self, url):
        self.url = url
        self.browser = chrome_webdriver()
    def crawling(self, product_link_filename, product_info_filename):
        # Truy cập vào url
        self.browser.get(self.url)
        sleep(5)
        # Click hiện thị thêm
        show_more(self.browser, 'v5-more-product')
        # Craw dữ liệu tên sản phẩm và link sản phẩm
        products_link = craw_product_link(self.browser, 'v5-item', output_filename = product_link_filename)
        # Truy cập vào link sản phầm và craw thông tin chi tiết về sản phầm
        products_info = []
        for _, row in products_link.iterrows():
            product_info  = craw_product_info(self.browser, row['product_link'])
            products_info.append(
                product_info
            )
        # Xử lí các thông tiin lỗi và lưu thành file csv
        products_info = [item for item in products_info if item is not None]
        products_info = pd.DataFrame(products_info)
        products_info.to_csv(f'{product_info_filename}', index = False)

        sleep(5)

        #Close Website
        self.browser.close()
        

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="WebCrawling program")
    # Add argument
    parser.add_argument('--pl', type = str, default='product_brand.csv', help = 'File name of phone brand')
    parser.add_argument('--pi', type = str, default = 'item.csv', help  = 'File name of item infomation')
    parser.add_argument('--url', type = str, required = True, help = 'Url of Website you need craw')

    args = parser.parse_args()

    crawler = WebCrawler(args.url)
    crawler.crawling(product_link_filename = args.pl, product_info_filename = args.pi)
