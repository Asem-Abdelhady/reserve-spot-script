from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from dotenv import dotenv_values
from time import sleep


CONFIG = dotenv_values(".env")

DRIVER = webdriver.Chrome()

WAIT = WebDriverWait(DRIVER, 30)
def is_logged_in():
    DRIVER.get('https://sso.university.innopolis.ru/adfs/oauth2/authorize/?response_type=code&client_id=7d0eb0b9-ad73-4942-be55-284facc99a95&resource=7d0eb0b9-ad73-4942-be55-284facc99a95&redirect_uri=https%3A%2F%2Fsport.innopolis.university%2Foauth2%2Fcallback&state=cHJvZmlsZQ%3D%3D&scope=openid')
    return DRIVER.title != 'Profile'

def log_in():
    user_name = DRIVER.find_element(By.ID, 'userNameInput')
    password =  DRIVER.find_element(By.ID, 'passwordInput')
    check_in = DRIVER.find_element(By.ID, 'kmsiInput')
    user_name.send_keys(CONFIG['email'])
    password.send_keys(CONFIG['password'])

    sign_in_button = DRIVER.find_element(by=By.ID, value='submitButton')
    check_in.click()
    sign_in_button.click()

def load_spots():
    tue = WAIT.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div/div[2]/div/div[2]/div[2]/div/div/table/tbody/tr[11]/td[3]/a')))
    wed = WAIT.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div/div[2]/div/div[2]/div[2]/div/div/table/tbody/tr[29]/td[3]/a')))
    return [tue, wed]

def reserve_spot():
    DRIVER.get('https://sport.innopolis.university/profile/')
    move_right = WAIT.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="calendar"]/div[1]/div[2]/div/button[2]/span')))
    move_right.click()

    
    spots = load_spots()
    counter = 0
    for spot in spots:
        print(counter)
        spot.click()
        click_button = WAIT.until(EC.presence_of_element_located((By.XPATH,'//*[@id="group-info-modal"]/div/div/div[3]/div/div/div[2]/button')))
        if click_button.is_enabled() and click_button.text == 'Check in':
             print('inside if')
             click_button.click()
             spots=load_spots()
             counter+=1
             continue
        print('outside if ')
        close_botton = click_button = WAIT.until(EC.presence_of_element_located((By.XPATH,'//*[@id="group-info-modal"]/div/div/div[3]/div/div/div[1]/button')))
        close_botton.click()
        sleep(0.5)
        counter+=1
    # counter = 5
    # while counter:
    #     elements = WAIT.until(EC.presence_of_all_elements_located((By.PARTIAL_LINK_TEXT, 'Swimming - Advanced')))
    #     print("inside while")
    #     for element in elements:
    #         print (f"Counter is {counter}")
    #         element.click()
    #         click_button = WAIT.until(EC.presence_of_element_located((By.XPATH,'//*[@id="group-info-modal"]/div/div/div[3]/div/div/div[2]/button')))
    #         print(click_button.text)
    #         if click_button.is_enabled() and click_button.text == 'Check in':
    #             click_button.click()
    #             break
    #         close_botton = click_button = WAIT.until(EC.presence_of_element_located((By.XPATH,'//*[@id="group-info-modal"]/div/div/div[3]/div/div/div[1]/button')))
    #         close_botton.click()
    #         counter-=1
            

        

    # for element in elements:
    #     print(element)
    # print(elements)
    # element = WAIT.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Football')))
    # element.click()

    # enroll = WAIT.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="group-info-modal"]/div/div/div[3]/div/div/div[2]/button')))
    # enroll.click()
    # elements = WAIT.until(EC.presence_of_all_elements_located((By.PARTIAL_LINK_TEXT, 'Football')))
    
    # for element in elements:
    #     try:
    #         if not element.is_enabled():
    #             continue
    #         element.click()
    #         enrolls = WAIT.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="group-info-modal"]/div/div/div[3]/div/div/div[2]/button')))
            
    #         for enroll in enrolls:
    #             try:
    #                 #print(f"Text : {enroll.text}")
    #                 enroll.click()
    #                 DRIVER.navigate().refresh()
    #             except:
    #                 print("inside the enroll exception")
    #                 pass
    #     except:
    #         print("inside the element exception")
    #         pass

                    
if __name__ == "__main__":
    if is_logged_in():
        log_in()
    reserve_spot()
    DRIVER.quit()