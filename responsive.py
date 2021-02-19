import time
import os
from urllib.parse import urlparse
from math import ceil
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


class ResponsiveTester:
    def __init__(self, urls, path):
        self.browser = webdriver.Chrome(ChromeDriverManager().install())
        self.browser.maximize_window()
        self.urls = urls
        self.sizes = [480, 960, 1366, 1920]
        self.browser_height = self.browser.get_window_size()["height"]
        self.path = path

    def screenshot(self, url):
        self.browser.get(url)
        for size in self.sizes:
            self.browser.set_window_size(size, self.browser_height)
            self.browser.execute_script("window.scrollTo(0,0)")
            time.sleep(1)
            scroll_size = self.browser.execute_script("return document.body.scrollHeight")
            total_sections = ceil(scroll_size / self.browser_height)
            for section in range(total_sections + 1):
                self.browser.execute_script(f"window.scrollTo(0, {section * self.browser_height})")
                self.browser.save_screenshot(f"{self.save_path}/{size}x{section}.png")

    def get_path(self, url):
        dir_name = urlparse(url).netloc
        self.save_path = os.path.join(self.path, dir_name)
        print(self.save_path)

    def is_dir(self):
        # If it doesn't exist make a directory.
        if not os.path.isdir(self.save_path):
            os.mkdir(self.save_path)

    def start(self):
        for url in self.urls:
            self.get_path(url)
            self.is_dir()
            self.screenshot(url)

    def finish(self):
        self.browser.quit()


test_responsive = ResponsiveTester(
    [
        "https://nomadcoders.co/",
        "https://www.google.com/",
        "https://www.naver.com/",
    ],
    "screenshot/responsive",
)
test_responsive.start()
test_responsive.finish()