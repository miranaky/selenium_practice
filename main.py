import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class GoogleKeywordScreenshoter:
    """ automaticaly screenshot keyword searching by google.com"""

    def __init__(self, keyword, screenshot_dir):
        self.browser = webdriver.Chrome(ChromeDriverManager().install())
        self.keyword = keyword
        self.screenshot_dir = screenshot_dir

    def is_dir(self, path):
        # If it doesn't exist make a directory.
        if not os.path.isdir(path):
            os.mkdir(path)

    def remove_shitty(self):
        # remove shitty_element
        try:
            shitty_element = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "liYKde"))
            )
            self.browser.execute_script(
                """
            const shitty = arguments[0]
            shitty.parentElement.removeChild(shitty)
            """,
                shitty_element,
            )
        except Exception:
            pass

    def run(self):
        dir_path = f"{self.screenshot_dir}/{self.keyword}"
        self.is_dir(dir_path)
        self.browser.get("https://www.google.com")
        search_bar = self.browser.find_element_by_class_name("gLFyf")
        search_bar.send_keys(self.keyword)
        search_bar.send_keys(Keys.ENTER)

        self.remove_shitty()

        search_results = self.browser.find_elements_by_class_name("g")
        for index, search_result in enumerate(search_results):
            search_result.screenshot(f"{dir_path}/{self.keyword}x{index}.png")

    def finish(self):
        self.browser.quit()


blackpink_scrapper = GoogleKeywordScreenshoter("blackpink", "screenshot")
blackpink_scrapper.run()
blackpink_scrapper.finish()

python_book_scrapper = GoogleKeywordScreenshoter("python book", "screenshot")
python_book_scrapper.run()
python_book_scrapper.finish()