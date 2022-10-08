import os
from time import sleep
import traceback
from utils.selenium_driver import get_web_driver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from dotenv import load_dotenv

load_dotenv()
CHROMEDRIVER = os.getenv('CHROMEDRIVER')
HEADLESS = True if os.getenv('HEADLESS') == '1' else False


def get_account_details(driver, acc_name='ishaansharma711'):
    url = "https://www.instagram.com/"
    driver.get(url + acc_name)

    user_stats = []
    user_details = {
        'posts': None,
        'followers': None,
        'following': None,
        'profile_pic_url': None,
        'name': None,
        'bio': None,
        'privacy_status': 'private',
        'scrape_status': 'failed'
    }

    # scrape profile pic url if public
    try:
        img_ele =  WebDriverWait(driver,8).until(EC.presence_of_element_located((By.CLASS_NAME, '_aa8j')))
        img_url = img_ele.get_attribute('src')
        user_details['profile_pic_url'] = img_url
    except Exception:
        traceback.print_exc()
        print('unable to get user profile_pic--------')


    # scrape posts, followers, following
    try:
        ul =  WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CLASS_NAME, '_aa_7')))
        options = ul.find_elements_by_tag_name("li")
        for li in options:
            user_stats.append(li.text.split()[0])
        user_details.update({'posts': user_stats[0], 'followers': user_stats[1], 'following': user_stats[2]})
        user_details['scrape_status'] = 'partial'
    except Exception:
        traceback.print_exc()
        print('user_details failed------', user_details)
        return user_details


    # scrape name and bio
    try:
        desc = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CLASS_NAME, '_aa_c')))
        name_span = desc.find_elements_by_tag_name("span")
        bio_div = desc.find_elements_by_tag_name("div")
        user_details['name'] = ''
        user_details['bio'] = ''
        if name_span:
            user_details['name'] = name_span[0].text
        if bio_div:
            bio_text = ''
            for each_ele in bio_div:
                bio_text += each_ele.text
            bio_text = bio_text.replace(user_details['name'], '').replace('\n', ' ')
            user_details['bio'] = bio_text
            user_details['scrape_status'] = 'complete'
    except Exception:
        traceback.print_exc()

    # public/private
    try:
        private_ele =  WebDriverWait(driver,2).until(EC.presence_of_element_located((By.CLASS_NAME, '_aa_u')))
        user_details['privacy_status'] = 'private'
    except TimeoutException:
        user_details['privacy_status'] = 'public'

    return user_details

if __name__ == '__main__':
    driver = get_web_driver(CHROMEDRIVER, HEADLESS)
    acc_list = ['ishaansharma711', 'anuj.suman']
    driver.maximize_window()
    ct = 0
    # for each in ['ishaansharma711', 'rishabhhh20', 'iam_lalit']:
    for each in acc_list:
        ct += 1
        print(f'-----------{ct}, {each}-----------')
        try:
            print(get_account_details(driver, each))
        except Exception:
            traceback.print_exc()
        print('----------------------------------')
        sleep(2)
    driver.close()