import sys

from dotenv import dotenv_values
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


CONFIG = dotenv_values(".env")


chrome_options = webdriver.ChromeOptions()
if "headless" in sys.argv:
    chrome_options.add_argument("--headless")

DRIVER = webdriver.Chrome(options=chrome_options)

DAY = sys.argv[1]

WAIT = WebDriverWait(DRIVER, 30)


def is_logged_in():
    DRIVER.get(
        "https://sso.university.innopolis.ru/adfs/oauth2/authorize/?response_type=code&client_id=7d0eb0b9-ad73-4942-be55-284facc99a95&resource=7d0eb0b9-ad73-4942-be55-284facc99a95&redirect_uri=https%3A%2F%2Fsport.innopolis.university%2Foauth2%2Fcallback&state=cHJvZmlsZQ%3D%3D&scope=openid"
    )
    return DRIVER.title == "Profile"


def log_in():
    user_name = DRIVER.find_element(By.ID, "userNameInput")
    password = DRIVER.find_element(By.ID, "passwordInput")
    check_in = DRIVER.find_element(By.ID, "kmsiInput")
    user_name.send_keys(CONFIG["email"])
    password.send_keys(CONFIG["password"])

    sign_in_button = DRIVER.find_element(by=By.ID, value="submitButton")
    check_in.click()
    sign_in_button.click()


def load_spot():
    spot = None
    match DAY:
        case "tue":
            spot = WAIT.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "/html/body/div[1]/div/div[2]/div/div[2]/div/div[2]/div[2]/div/div/table/tbody/tr[20]/td[3]/a",
                    )
                )
            )

        case "thu":
            spot = WAIT.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "/html/body/div[1]/div/div[2]/div/div[2]/div/div[2]/div[2]/div/div/table/tbody/tr[61]/td[3]/a",
                    )
                )
            )
        case "sat":
            spot = WAIT.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "/html/body/div[1]/div/div[2]/div/div[2]/div/div[2]/div[2]/div/div/table/tbody/tr[91]/td[3]/a",
                    )
                )
            )
        case _:
            print("Day entered wrong")
            exit(1)

    return spot


def reserve_spot():
    DRIVER.get("https://sport.innopolis.university/profile/")
    move_right = WAIT.until(
        EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="calendar"]/div[1]/div[2]/div/button[2]/span')
        )
    )
    move_right.click()

    spot = load_spot()
    spot.click()

    click_button = WAIT.until(
        EC.presence_of_element_located(
            (By.XPATH, "/html/body/div[4]/div/div/div[3]/div/div/div[2]/button")
        )
    )

    if click_button.is_enabled():
        click_button.click()
        DRIVER.refresh()
    print(spot)


if __name__ == "__main__":
    if not is_logged_in():
        log_in()
    reserve_spot()
    DRIVER.quit()
    print("SUCCESS")
