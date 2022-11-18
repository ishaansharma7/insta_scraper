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
from data.send_data_to_apis import single_reel_data_to_api, post_data_to_api
from data.highlights_data import get_high_data
from utils.populate_dates import populate_reel_dates


def get_reel_details(contents, user_name, user_id, media_df, reel_short_code):
    try:
        beautifulSoupText = BeautifulSoup(contents, 'html.parser')
        reel_div = beautifulSoupText.find('main')
        if reel_div:
            reel_div = reel_div.find_all("a", attrs={"class":"x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz _a6hd", "role":"link"})
            comments_count = like_count = view_count = 0
            media_url = shortcode = None
            for div in reel_div:
                shortcode = div['href']
                if "reel" in shortcode and shortcode not in reel_short_code:
                    reel_short_code[shortcode] = 1
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

                    except Exception:
                        traceback.print_exc()
                        print('failed to get like,comment and views count, POS:rfh-1 -------')
                    media_df = media_df.append({
                                "user_id" : user_id,
                                "user_name" : user_name, 
                                "media_url" : media_url,
                                "shortcode" : shortcode,
                                "like_count" : like_count,
                                "comments_count" : comments_count,
                                "view_count" : view_count
                                }, ignore_index=True)
    except Exception as e:
        traceback.print_exc()
        print('failure in scraping reels basic info, POS:rfh-2 -------')
        return media_df, False
    return media_df, True


def get_user_details(driver, user_name, user_id, user_pvt=False):
    user_df = pd.DataFrame(columns=["user_id", "user_name", "insta_user_name", "profile_url", "post_count", "followers_count", "following_count", "bio", "account_type","account_exists_status", "highlights"])
    user_id = insta_user_name = profile_url = post_count = followers_count = following_count = bio = private_account_status = account_exists_status = None
    highlight_list = []
    try:
        user_stats =  WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, '_ac2a')))
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
        insta_user_name = user_name
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
    try:
        insta_url = 'https://www.instagram.com'
        shortcode_len = len(shortcode_set)
        shortcode_and_date = {}
        if not shortcode_len:
            return
        latest_post = shortcode_set[0]
        shortcode_and_date[latest_post] = get_single_reel_detail(driver, insta_url+ '/reel/' +latest_post)
        if shortcode_len < 3:
            oldest_post  = shortcode_set[-1]
            get_single_reel_detail(driver, insta_url+ '/reel/' + oldest_post)
        else:
            mid = int(shortcode_len/2)
            mid_post = shortcode_set[mid]
            shortcode_and_date[mid_post] = get_single_reel_detail(driver, insta_url+ '/reel/' + mid_post)
            oldest_post = shortcode_set[-1]
            shortcode_and_date[oldest_post] = get_single_reel_detail(driver, insta_url+ '/reel/' + oldest_post)
            # add the code for populating date here
            # pprint(shortcode_and_date)
            if shortcode_and_date[mid_post] and shortcode_and_date[oldest_post] and shortcode_and_date[latest_post]:
                populate_reel_dates(mid, shortcode_set, shortcode_and_date)
            else:
                print('failure in getting reels upload date -----')
        # here the api for sending data
    except Exception:
        traceback.print_exc()
        print('single reel failure-----')


def get_shortcodes_reels(driver, reel_short_code2):
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
                if "/reel/" in shortcode and shortcode not in reel_short_code2:
                    reel_short_code2[shortcode] = 1
                    parsed_shortcode = shortcode.replace('/reel/', '').replace('/', '')
                    # print('shortcode-----', shortcode)
                    # shortcode_set.append(insta_url+shortcode)
                    shortcode_set.append(parsed_shortcode)
                    # print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    except Exception as e:
        traceback.print_exc()
    return shortcode_set

def get_single_reel_detail(driver, post_url):
    driver.get(post_url)
    data_dict = {'shortcode': None, 'caption': None, 'hashtags':[]}
    shortcode = post_url.split('/reel/')[1].replace('/', '')
    # print(shortcode)
    data_dict['shortcode'] = shortcode
    time_str = None
    try:
        time_ht = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'time')))
        time_str = str(time_ht.get_attribute('datetime'))
    except Exception:
        traceback.print_exc()
        print('media date not found -----')
    data_dict['media_date'] = time_str

    try:
        # caption_ele = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="mount_0_0_Ab"]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/div[1]/ul/div')))
        caption_ele = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, '_a9zs')))
        caption = caption_ele.find_element(By.TAG_NAME, "span")
        caption1 = str(caption.text)
        # print('caption detected----',caption1)

        caption2 = ''
        try:
            ul_section = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.TAG_NAME, 'ul')))
            ul_section = WebDriverWait(ul_section, 2).until(EC.presence_of_element_located((By.TAG_NAME, 'ul')))
            caption = ul_section.find_element(By.CLASS_NAME, "_a9zs")
            caption = caption.find_element(By.TAG_NAME, "span")
            caption2 = str(caption.text)
            # print('new detected----', caption2)
        except Exception:
            pass
        if caption1 == caption2:
            data_dict['caption'] = None
        else:
            data_dict['caption'] = caption1
    except Exception:
        # traceback.print_exc()
        print('no caption-----')

    # print('full captions----', caption_text)
    try:
        hashtags = caption_ele.find_elements(By.TAG_NAME, "a")
        for tag in hashtags:
            data_dict['hashtags'].append(str(tag.text))
    except Exception:
        print('no hahtags')
    print(post_url, 'reel scraped -----')
    single_reel_data_to_api(data_dict)
    return time_str


def click_on_reels_tagged_users(driver):
    article = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'article')))
    video_div = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'x1ey2m1c x9f619 xds687c x10l6tqk x17qophe x13vifvy x1ypdohk')))
    
    # button.click()
    # users_div = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, '_abm4')))
    # for user_div in users_div:
    #     print('tagged users----', user_div.text)
    print('done')

def per_hover(driver, covered_shortcodes, ct_dict, user_name, user_id):
    sleep(10)
    try:
        post_grid = WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.TAG_NAME, 'article')))
        all_post = WebDriverWait(post_grid, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'a')))
    except Exception:
        traceback.print_exc()
        print('unable to locate posts-----')
        return []
    scraped_post_list = []
    hover_success = True
    for single_post in all_post:
        try:
            if str(single_post.get_attribute("href")) in covered_shortcodes:
                continue
            # print(ct_dict['ct'])
            ct_dict['ct'] += 1
            covered_shortcodes[str(single_post.get_attribute("href"))] = 1
            single_post.get_attribute("href")
            hover = ActionChains(driver).move_to_element(single_post)
            hover.perform()
            single_post_html = single_post.get_attribute('innerHTML')
            # print(single_post.get_attribute('innerHTML'))
            # return
            beautifulSoupText = BeautifulSoup(single_post_html, 'html.parser')
            shortcode = str(single_post.get_attribute("href")).split('/p/')[1].replace('/','')
            # print('shortcode-----', shortcode)
            data_div = beautifulSoupText.find_all("div", attrs={"class":"_aacl _aacp _aacw _aad3 _aad6 _aade"})
            like_comment_div_count = 0
            like_comment_storage = []
            for data in data_div:
                # print(data.text)
                like_comment_storage.append(str(data.text))
                like_comment_div_count += 1
            like_count = comment_count = 0
            if like_comment_div_count > 1:
                like_count = like_comment_storage[0]
                comment_count = like_comment_storage[-1]
            elif like_comment_div_count == 1:
                comment_count = like_comment_storage[0]
            # print(f'like: {like_count},  comment: {comment_count}')

            img_ele = beautifulSoupText.find('img')
            alt_text = ''
            media_url = ''
            if 'alt' in img_ele.attrs:
                alt_text = img_ele.attrs['alt']
            # print('alt_text-----', alt_text)
            if 'src' in img_ele.attrs:
                media_url = img_ele.attrs['src']
            # print('src-----', media_url)

            scraped_post_list.append({
                'shortcode': shortcode,
                'like_count': like_count,
                'comments_count': comment_count,
                'alt_text': alt_text,
                'user_name': user_name,
                'user_id': user_id,
                'media_url': media_url
            })
            hover_success = True
            sleep(.3)
        except Exception:
            # traceback.print_exc()
            print('exception in per hover-----')
            hover_success = False
            # driver.refresh()
            # sleep(5)
            # continue
    if hover_success:   print('hover success -----')
    return scraped_post_list

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