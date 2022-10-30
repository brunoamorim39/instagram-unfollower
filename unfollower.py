import json
import time
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

user_agent_desktop = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
headers = {'User-Agent': user_agent_desktop}

def get_login():
    with open('config.json') as config:
        config_data = json.load(config)
    
    return config_data

def log_in(driver, login_info):
    print('LOGGING IN...')
    time.sleep(random.uniform(5, 8))
    inputs = driver.find_elements(By.TAG_NAME, 'input')
    inputs[0].send_keys(login_info['USERNAME'])
    inputs[1].send_keys(login_info['PASSWORD'])
    inputs[1].send_keys(Keys.RETURN)
    time.sleep(random.uniform(8, 10))
    driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div/div/div/button').click()
    time.sleep(random.uniform(5, 10))
    return

def unfollow_users(driver, num_unfollowed):
    unfollow_buttons = driver.find_elements(By.XPATH, '//button/div/div[text()="Following"]')
    for button in unfollow_buttons:
        button.click()
        time.sleep(random.uniform(1, 2))
        confirm_button = driver.find_element(By.XPATH, '//button[text()="Unfollow"]')
        confirm_button.click()
        time.sleep(random.uniform(1, 2))
        if driver.find_element(By.XPATH, '//button[text()="OK"]'):
            cancel_report_prompt_button = driver.find_element(By.XPATH, '//button[text()="OK"]')
            cancel_report_prompt_button.click()
            time.sleep(random.uniform(1, 2))
        num_unfollowed += 1
    if driver.find_elements(By.XPATH, '//button/div/div[text()="Following"]'):
        if num_unfollowed >= 200:
            time.sleep(random.uniform(1800, 3600))
        unfollow_users(driver, num_unfollowed)
    else:
        print('COMPLETED UNFOLLOWING!')
    return

def main():
    login_info = get_login()
    driver = webdriver.Firefox()
    main_url = 'https://www.instagram.com/'
    url = f'{main_url}accounts/login/?next=%2F{login_info["USERNAME"]}/following%2F&source=desktop_nav'
    driver.get(url)
    log_in(driver, login_info)
    print('BEGINNING UNFOLLOWING...')
    num_unfollowed = 0
    unfollow_users(driver, num_unfollowed)

if __name__ == '__main__':
    main()