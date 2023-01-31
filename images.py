import os

import selenium
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

import base64
import argparse


class IDReadException(Exception):
    pass


def _update_src(browser: webdriver.Firefox, value: str, element_id: str = 'recursivereadme'):
    script = f"document.getElementById('user-content-{element_id}').src = '{value}'"
    try:
        browser.execute_script(script)
    except selenium.common.exceptions.JavascriptException:
        raise IDReadException(f"Failed to find a tag with id '{element_id}' on {browser.current_url}. Are you sure you "
                              f"set the right one?")


def _get_recursive_image(browser: webdriver.Chrome, iterations: int = 10, element_id: str = 'recursivereadme'):
    if iterations == 0:
        return browser.get_screenshot_as_base64()

    new_img = f"data:image/png;base64,{browser.get_screenshot_as_base64()}"
    _update_src(browser, new_img, element_id)

    return _get_recursive_image(browser, iterations - 1)


def get_image(user: str, depth=10, resolution: tuple[int, int] = (1280, 800), element_id: str = 'recursivereadme'):
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

        return base64.b64decode(_get_recursive_image(browser, depth, element_id))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-u", "--user",
        help="The user for which to generate the image.",
        default='false',
    )
    parser.add_argument(
        "-o", "--output-file",
        help="The file to which the image is output.",
        default="example.png",
    )
    parser.add_argument(
        "-i", "--tag-id",
        help="The id of the img tag in your README.",
        default='recursivereadme',
    )

    args = parser.parse_args()

    if args.user == 'false':
        args.user = os.getenv('GITHUB_REPOSITORY_OWNER', 'daankoning')
        print(f"User set to: {args.user}")

    with open(args.output_file, 'wb') as file:
        file.write(get_image(args.user, element_id=args.tag_id))


if __name__ == '__main__':
    main()
