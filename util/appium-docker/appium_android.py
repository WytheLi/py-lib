from appium import webdriver

desired_caps = {}
desired_caps["platformName"] = "Android"
desired_caps["platformVersion"] = "8.0.0"
desired_caps["deviceName"] = "Nokia 6"

desired_caps["appPackage"] = "com.ted.android"
desired_caps["appActivity"] = ".view.splash.SplashActivity"

import requests
def test_chrome_server():
    while True:
        i = 0
        try:
            resp = requests.get("http://appium:4723/wd/hub/status", timeout=0.5)
        except:
            i += 1
            if i>10:
                raise
        else:
            print(resp.content)
            break

test_chrome_server()


print("尝试连接")
driver = webdriver.Remote(
    command_executor="http://appium:4723/wd/hub",
    desired_capabilities=desired_caps
)

print("连接成功")
import time
time.sleep(2)
driver.find_element_by_android_uiautomator("text(\"热门\")").click()
import time
time.sleep(5)
driver.quit()


