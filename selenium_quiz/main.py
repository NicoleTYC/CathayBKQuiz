from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

import time, os, shutil, gc
import logger

screenshot_path = 'screenshoot'
log = logger.create_logger()

class test_controller:
    def __init__(self) -> None:
        self.driver = None
        
        if os.path.exists(screenshot_path):
            shutil.rmtree(screenshot_path)
        os.makedirs(screenshot_path)


    def get_chrome_driver(self):
        try:
            log.info(f'[get_chrome_driver]')
            options = Options()
            options.add_argument('--ignore-certificate-errors')
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            options.add_experimental_option('mobileEmulation', {'deviceName': 'iPhone 12 Pro'})
            return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        except Exception as ex:
            log.error(f'[get_chrome_driver] ex:{ex}')
            return None
        
    def wait_for_element(self, driver, xpath, timeout=10):
        try:
            log.info(f'[wait_for_element] wait page element exists {str(xpath)}')
            element_present = EC.presence_of_element_located((By.XPATH, xpath))
            WebDriverWait(driver, timeout).until(element_present)

        except Exception as ex:
            logger.error(f'[wait_for_element] xpath:{str(xpath)} ex: {str(ex)}')

    def check_files_count(self, path, prefix):
        cnt = 0
        try:
            files = os.listdir(path)
            cnt = len([file for file in files if file.startswith(prefix)])
        except Exception as ex:
            logger.error(f'[check_files_count] path:{str(path)} ex: {str(ex)}')
        return cnt
    
    def proess(self, url, timeout=30) :
        try:
            log.info(f'[proess] START !')

            self.driver = self.get_chrome_driver()
            if self.driver is None:
                return False
            
            self.driver.set_page_load_timeout(timeout)
            self.driver.start_client()
            log.info(f'[proess] Start {url}')
            self.driver.get(url)
            
            element_locator = '//div[contains(@class, "cubre-o-indexKv__wrap")]'            
            self.wait_for_element(driver=self.driver, xpath=element_locator)            
            self.driver.save_screenshot(f"./{screenshot_path}/launch.png")

            # ==========================================
            element_locator = '//div[contains(@class, "cubre-o-header__burger")]'
            log.info(f'[proess] Click lefe-upper menu {str(element_locator)}')
            self.driver.find_element(By.XPATH, element_locator).click()
            
            element_locator = '//div[contains(@class, "cubre-o-nav__content")]'
            self.wait_for_element(driver=self.driver, xpath=element_locator)
            self.driver.save_screenshot(f"./{screenshot_path}/menu.png")

            
            element_locator = '//div[@class="cubre-a-menuSortBtn -l1" and text()="產品介紹"]' 
            log.info(f'[proess] Click {str(element_locator)}')
            self.driver.find_element(By.XPATH, element_locator).click()

            element_locator = '//div[@class="cubre-a-menuSortBtn" and text()="信用卡"]'
            log.info(f'[proess] Click {str(element_locator)}')
            self.driver.find_element(By.XPATH, element_locator).click()

            element_locator = '//div[@class="cubre-o-menuLinkList__item is-L2open"]/div[@class="cubre-o-menuLinkList__content"]/a[@id="lnk_Link" and @class="cubre-a-menuLink"]'
            log.info(f'[proess] Check {str(element_locator)}')
            menu_cnt = len(self.driver.find_elements(By.XPATH, element_locator))
            log.info(f'[proess] menu_cnt {str(menu_cnt)}')
            self.driver.save_screenshot(f"./{screenshot_path}/menu_credit_card_items.png")

            # ==========================================

            element_locator = '//a[@class="cubre-a-menuLink" and text()="卡片介紹"]'
            log.info(f'[proess] Click {str(element_locator)}')
            self.driver.find_element(By.XPATH, element_locator).click()

            element_locator = '//a[@class="cubre-m-anchor__btn swiper-slide"]/p[text()="停發卡"]'
            log.info(f'[proess] Find {str(element_locator)}')          
            element = self.driver.find_element(By.XPATH, element_locator)
            actions = ActionChains(self.driver)
            log.info(f'[proess] Scroll to it')   
            actions.move_to_element(element).perform()
            time.sleep(3)
            self.driver.save_screenshot(f"./{screenshot_path}/stop_credit_card.png")

            element = self.driver.find_element(By.XPATH, element_locator)
            element.click()
            time.sleep(3)
            self.driver.save_screenshot(f"./{screenshot_path}/suspend_card_page.png")

            element_locator = '//section[@data-anchor-block="blockname06"]//span[@role="button"]'
            log.info(f'[proess] Find {str(element_locator)}')
            elements_list = self.driver.find_elements(By.XPATH, element_locator)
            card_cnt = len(elements_list)
            log.info(f'[proess] Get suspend credit card cnt {str(card_cnt)}')            
            for idx,ele in enumerate(elements_list):
                log.info(f'[proess] Click card {idx}')
                ele.click()
                time.sleep(1)
                self.driver.save_screenshot(f"./{screenshot_path}/suspend_credit_card{idx}.png")

            file_cnt = self.check_files_count(path=f'{screenshot_path}',prefix='suspend_credit_card')
            log.info(f'[proess] screenshot file cnt: {str(file_cnt)}')
            if file_cnt!=card_cnt:
                print('file_cnt!=card_cnt')
                log.error(f'[proess] file_cnt {file_cnt} != card_cnt {card_cnt}')
            else:
                log.info(f'[proess] file_cnt {file_cnt} is equal to card_cnt {card_cnt}')

            log.info(f'[proess] END !')

        except Exception as ex:
            log.error(f'[proess] exception:{str(ex)}')
            print(ex)
        finally:
            self.driver.quit()
            del self.driver
            gc.collect()


if __name__ == "__main__":
    c = test_controller()
    c.proess(url='https://www.cathaybk.com.tw/cathaybk/')