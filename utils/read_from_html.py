from pprint import pprint
import random
from time import sleep
import traceback
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from data.highlights_data import get_high_data


def get_reel_details(contents, user_name, user_id, media_df):
    try:
        beautifulSoupText = BeautifulSoup(contents, 'html.parser')
        reel_div = beautifulSoupText.find('main')
        if reel_div:
            # reel_div = reel_div.find_all("a", attrs={"class":"qi72231t nu7423ey n3hqoq4p r86q59rh b3qcqh3k fq87ekyn bdao358l fsf7x5fv rse6dlih s5oniofx m8h3af8h l7ghb35v kjdc1dyq kmwttqpk srn514ro oxkhqvkx rl78xhln nch0832m cr00lzj9 rn8ck1ys s3jn8y49 icdlwmnq _a6hd", "role":"link"})
            reel_div = reel_div.find_all("a", attrs={"class":"x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz _a6hd", "role":"link"})
            comments_count = like_count = view_count = 0
            media_url = shortcode = None
            for div in reel_div:
                shortcode = div['href']
                if "reel" in shortcode:
                    shortcode = shortcode.replace("reel","").replace("/","")
                    div_list = div.find_all("div", attrs={"class":"_aag6 _aajx"})
                    for item in div_list:
                        media_url = item['style']
                        media_url = media_url[media_url.index("(\"")+2 : media_url.index("\")")]
                    span_list = div.find_all("span")
                    try:
                        # print('-----',span_list, '------')
                        if span_list:
                            like_count = span_list[0].string
                            stat_dict = {'comments_count': 0, 'view_count':0}
                            key = ''
                            for span in span_list[1:]:
                                if 'class' in span.attrs and span.attrs['class'][-1] == '_9-j_':
                                    key = 'comments_count'
                                    continue
                                elif 'class' in span.attrs and span.attrs['class'][-1] == '_9-k0':
                                    key = 'view_count'
                                    continue
                                else:
                                    stat_dict[key] = span.string
                            comments_count = stat_dict["comments_count"]
                            view_count = stat_dict["view_count"]

                            # comments_count = span_list[2].string
                            # view_count = span_list[4].string
                        # val_list = [0 for i in range(3)]
                        # idx = 0
                        # for span in span_list:
                        #     if span.string != '' and idx <= 2:
                        #         val_list[idx] = span.string
                        #         idx += 1
                        # print('val_list----', val_list)
                        # like_count, comments_count, view_count = val_list

                    except Exception:
                        traceback.print_exc()
                        print('failed to get like,comment and views count-------')
                    media_df = media_df.append({
                                "user_id" : user_id,
                                "user_name" : user_name, 
                                "media_url" : media_url,
                                "shortcode" : shortcode,
                                "like_count" : like_count,
                                "comments_count" : comments_count,
                                "view_count" : view_count
                                }, ignore_index=True)
                    # print('worked till here------')
    except Exception as e:
        traceback.print_exc()
        return media_df, False
    return media_df, True


def get_user_details(driver, user_name, user_id, user_pvt=False):
    user_df = pd.DataFrame(columns=["user_id", "user_name", "insta_user_name", "profile_url", "post_count", "followers_count", "following_count", "bio", "account_type","account_exists_status", "highlights"])
    user_id = insta_user_name = profile_url = post_count = followers_count = following_count = bio = private_account_status = account_exists_status = None
    highlight_list = []
    try:
        user_stats =  WebDriverWait(driver,8).until(EC.presence_of_all_elements_located((By.CLASS_NAME, '_ac2a')))
        post_count = user_stats[0].text
        post_count_int = int(post_count.replace(',', ''))
        followers_count = user_stats[1].text
        following_count = user_stats[2].text
        if not user_pvt or not post_count_int:
            highlight_list = get_high_data(driver)

        desc = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CLASS_NAME, '_aa_c')))
        name_span = desc.find_elements_by_tag_name("span")
        bio_div = desc.find_elements_by_tag_name("div")


        if name_span:
            user_actual_name = name_span[0].text
        else:
            user_actual_name = ''

        if bio_div:
            bio_text = ''
            for each_ele in bio_div:
                bio_text += each_ele.text
            bio_text = bio_text.replace(user_actual_name, '').replace('\n', ' ')
            bio = bio_text
        else:
            bio = ''
        
        beautifulSoupText = BeautifulSoup(driver.page_source, 'html.parser')
        reel_div = beautifulSoupText.find('main')
        if reel_div:
            # profile_header = reel_div.find("header", attrs={"class": "_aa_h"})
            profile_header = reel_div.find("header", attrs={"class": "x1gv9v1y x1dgd101 x186nx3s x1n2onr6 x2lah0s x1q0g3np x78zum5 x1qjc9v5 xlue5dm x1tb5o9v"})
            if profile_header:
                insta_user_name = profile_header.find("h2").text
                profile_url = profile_header.find("img")["src"]
    except Exception:
        traceback.print_exc()
        insta_user_name = user_name
    finally:
        user_df = user_df.append({
                                "user_id" : user_id,
                                "user_name" : user_name,
                                "insta_user_name" : insta_user_name, 
                                "profile_url" : profile_url, 
                                "post_count": post_count, 
                                "followers_count" : followers_count, 
                                "following_count" : following_count, 
                                "bio" : bio, 
                                "account_type" : user_pvt,
                                "account_exists_status" : account_exists_status,
                                "highlights": highlight_list
                            }, ignore_index=True)
        return user_df, post_count_int



def get_full_reel_details(driver, shortcode_set):
    # pprint(shortcode_set)
    shortcode_len = len(shortcode_set)
    if not shortcode_len:
        return

    latest_post = shortcode_set[0]
    get_single_reel_detail(driver, latest_post)
    if shortcode_len < 3:
        oldest_post  = shortcode_set[-1]
        get_single_reel_detail(driver, oldest_post)
    else:
        mid = int(shortcode_len/2)
        mid_post = shortcode_set[mid]
        get_single_reel_detail(driver, mid_post)
        oldest_post  = shortcode_set[-1]
        get_single_reel_detail(driver, oldest_post)

    # add the code for scraping data here
    # here the api for sending data


def get_shortcodes_reels(driver):
    insta_url = 'https://www.instagram.com'
    shortcode_set = []
    try:
        contents = driver.page_source
        beautifulSoupText = BeautifulSoup(contents, 'html.parser')
        post_div = beautifulSoupText.find('main')
        if post_div:
            post_div = post_div.find_all("a", attrs={"class":"x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz _a6hd", "role":"link"})
            for div in post_div:
                shortcode = div['href']
                if "/reel/" in shortcode:
                    # print('shortcode-----', shortcode)
                    shortcode_set.append(insta_url+shortcode)
                    # print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    except Exception as e:
        traceback.print_exc()
    return shortcode_set

def get_single_reel_detail(driver, post_url):
    driver.get(post_url)
    print(post_url)
    time_ht = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'time')))
    print('time_ht----', time_ht.get_attribute('datetime'))
    caption_ele = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, '_a9zs')))
    caption = caption_ele.find_element(By.TAG_NAME, "span")
    caption_text = str(caption.text)
    print('full captions----', caption_text)
    hashtags = caption_ele.find_elements(By.TAG_NAME, "a")
    print('hashtags-----')
    for tag in hashtags:
        print(tag.text)
    # click_on_reels_tagged_users(driver)
    print('***************')

def click_on_reels_tagged_users(driver):
    article = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'article')))
    video_div = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'x1ey2m1c x9f619 xds687c x10l6tqk x17qophe x13vifvy x1ypdohk')))
    
    # button.click()
    # users_div = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, '_abm4')))
    # for user_div in users_div:
    #     print('tagged users----', user_div.text)
    print('done')

def per_hover(driver):
    driver.get('https://www.instagram.com/cristiano/')
    post_grid = WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.TAG_NAME, 'article')))
    all_post = WebDriverWait(post_grid, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'a')))
    ct = 1
    for single_post in all_post:
        print(ct)
        ct += 1
        single_post.get_attribute("href")
        hover = ActionChains(driver).move_to_element(single_post)
        hover.perform()
        single_post_html = single_post.get_attribute('innerHTML')
        # print(single_post.get_attribute('innerHTML'))
        # return
        beautifulSoupText = BeautifulSoup(single_post_html, 'html.parser')
        shortcode = str(single_post.get_attribute("href")).split('/p/')[1].replace('/','')
        print('shortcode-----', shortcode)
        data_div = beautifulSoupText.find_all("div", attrs={"class":"_aacl _aacp _aacw _aad3 _aad6 _aade"})
        for data in data_div:
            print(data.text)
        print()
        print()

def per_hover2(driver):
    driver.get('https://www.instagram.com/cristiano/')
    post_grid = WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.TAG_NAME, 'article')))
    single_post = WebDriverWait(post_grid, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'a')))
    hover = ActionChains(driver).move_to_element(single_post)
    hover.perform()
    single_post_html = single_post.get_attribute('innerHTML')
    # print(single_post.get_attribute('innerHTML'))
    beautifulSoupText = BeautifulSoup(single_post_html, 'html.parser')
    data_div = beautifulSoupText.find_all("div", attrs={"class":"_aacl _aacp _aacw _aad3 _aad6 _aade"})
    for data in data_div:
        print(data.text)
    


def get_post_details(contents, user_name, user_id, covered_shortcodes, media_df):
    try:
        beautifulSoupText = BeautifulSoup(contents, 'html.parser')
        reel_div = beautifulSoupText.find('main')
        if reel_div:
            # reel_div = reel_div.find_all("a", attrs={"class":"qi72231t nu7423ey n3hqoq4p r86q59rh b3qcqh3k fq87ekyn bdao358l fsf7x5fv rse6dlih s5oniofx m8h3af8h l7ghb35v kjdc1dyq kmwttqpk srn514ro oxkhqvkx rl78xhln nch0832m cr00lzj9 rn8ck1ys s3jn8y49 icdlwmnq _a6hd", "role":"link"})
            reel_div = reel_div.find_all("a", attrs={"class":"x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz _a6hd", "role":"link"})
            comments_count = like_count = view_count = None
            media_url = shortcode = None
            for div in reel_div:
                shortcode = div['href']
                if "/p/" in shortcode and shortcode not in covered_shortcodes:
                    # print('post shortcode-----', 'https://www.instagram.com'+shortcode)
                    covered_shortcodes[shortcode] = 1
                    img = div.find('img')
                    # print('alt_text------', img.attrs.get('alt', None))
                    alt_text = img.attrs.get('alt', None)
                    # print('@@@@@@@@@@@@@@@@@@@@@@@')
                    # print()
                    shortcode = shortcode.replace('/','')
                    shortcode = shortcode.replace('p','')
                    media_df = media_df.append({
                                "user_id" : user_id,
                                "user_name" : user_name, 
                                "media_url" : media_url,
                                "shortcode" : shortcode,
                                "like_count" : like_count,
                                "comments_count" : comments_count,
                                "view_count" : view_count,
                                "alt_text": alt_text
                                }, ignore_index=True)
                    # print('worked till here------')
    except Exception as e:
        traceback.print_exc()
        return media_df, False
    return media_df, True