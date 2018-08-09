
import os
import time

import urllib.request

from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver


class Driver:

    DATE_XPATH = '//*[@id="timemachine"]/div/div/div/div[3]/div[4]/div/span[2]'
    UL_WRAPPER_XPATH = '//*[@id="timemachine"]/div/div/div/div[5]/div[2]/ul'
    IMAGE_XPATH = '//*[@id="timemachine"]/div/div/div/div[3]/img[2]'
    DRIVER_ARGS = ["--verbose", "--log-path=./chromedriver.log"]
    IMAGE_OUTPUTS_DIR = "./results"
    IMPLICIT_WAIT = 10
    SLEEP_TIME = 2

    def __init__(self):
        opts = webdriver.ChromeOptions()
        opts.add_argument("--incognito")
        # opts.add_argument("--headless")
        self.driver = webdriver.Chrome(
            "./driver/chromedriver",
            service_args=self.DRIVER_ARGS,
            chrome_options=opts,
        )
        self.driver.implicitly_wait(self.IMPLICIT_WAIT)

    def clean_path(self):
        p = self.IMAGE_OUTPUTS_DIR
        if os.path.exists(p):
            os.system("rm -rf {}".format(p))
        if not os.path.exists(p):
            os.makedirs(p)

    def open_url(self, url, tag):
        self.driver.get(url)
        self.tag = tag

    def download_historical_images(self):
        ul = self.driver.find_element_by_xpath(self.UL_WRAPPER_XPATH)
        for i, li in enumerate(ul.find_elements_by_tag_name("li")):
            print("-" * 100)
            print("{}: {}".format(i, li))
            b = li.find_element_by_tag_name("button")
            ActionChains(self.driver).move_to_element(b).click().perform()
            time.sleep(self.SLEEP_TIME)
            self._download_current_image()

    def _download_current_image(self):
        date = self.driver.find_element_by_xpath(self.DATE_XPATH)
        date = self._fix_date(date.text)
        image = self.driver.find_element_by_xpath(self.IMAGE_XPATH)
        img_src = image.get_attribute("src")
        print("- Date: {}".format(date))
        print("- Image: {}".format(img_src))
        print("- Downloading and saving image... ", end="")
        self._ensure_image_tag_directory_exists()
        save_to = "{}/{}/{}.jpeg".format(self.IMAGE_OUTPUTS_DIR, self.tag, date)
        urllib.request.urlretrieve(image.get_attribute("src"), save_to)
        print("DONE")

    def close(self):
        self.driver.close()

    def _ensure_image_tag_directory_exists(self):
        path = "{}/{}".format(self.IMAGE_OUTPUTS_DIR, self.tag)
        if not os.path.exists(path):
            os.makedirs(path)

    def _fix_date(self, date):
        try:
            parts = date.split(". ")
            return parts[1] + "_" + parts[0]
        except IndexError as e:
            return date + "_fix_date_error"
