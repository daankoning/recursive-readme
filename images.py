import os

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

import base64
import argparse


def _update_src(browser: webdriver.Firefox, value: str):
    script = f"document.getElementById('user-content-recursivereadme').src = '{value}'"
    browser.execute_script(script)


def _get_recursive_image(browser: webdriver.Chrome, iterations: int = 10):
    if iterations == 0:
        return browser.get_screenshot_as_base64()

    new_img = f"data:image/png;base64,{browser.get_screenshot_as_base64()}"
    _update_src(browser, new_img)

    return _get_recursive_image(browser, iterations - 1)


def get_image(user: str, depth=10, resolution: tuple[int, int] = (1280, 800)):
    print("Beginning install")
    chrome_service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
    print("Succesfuly installed Chromium")

    # largely stolen from https://github.com/jsoma/selenium-github-actions
    chrome_options = Options()
    options = [
        "--headless",
        "--disable-gpu",
        f"--window-size={resolution[0]},{resolution[1]}",
        "--ignore-certificate-errors",
        "--disable-extensions",
        "--no-sandbox",
        "--disable-dev-shm-usage",
    ]
    for option in options:
        chrome_options.add_argument(option)

    with webdriver.Chrome(service=chrome_service, options=chrome_options) as browser:
        print("Succesfully instantiated browser")
        url = f"https://www.github.com/{user}"
        browser.get(url)
        browser.fullscreen_window()

        return base64.b64decode(_get_recursive_image(browser, depth))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-u", "--user",
        help="The user for which to generate the image."
    )

    args = parser.parse_args()

    if args.user == 'false':
        args.user = os.getenv('GITHUB_REPOSITORY_OWNER')
        print(f"User set to: {args.user}")

    with open("example.png", 'wb') as file:
        file.write(get_image(args.user))  # TODO: errors when no user is set


if __name__ == '__main__':
    main()
