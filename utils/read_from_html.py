import traceback
from bs4 import BeautifulSoup
import pandas as pd


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
                    if span_list:
                        like_count = span_list[0].string
                        comments_count = span_list[2].string
                        view_count = span_list[4].string
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
        return media_df, False
    return media_df, True


def get_user_details(contents, user_name, user_id):
    user_df = pd.DataFrame(columns=["user_id", "user_name", "insta_user_name", "profile_url", "post_count", "followers_count", "following_count", "bio", "account_type"])
    user_id = insta_user_name = profile_url = post_count = followers_count = following_count = bio = private_account_status = account_exists_status = None
    try:
        beautifulSoupText = BeautifulSoup(contents, 'html.parser')
        reel_div = beautifulSoupText.find('main')
        if reel_div:
            # profile_header = reel_div.find("header", attrs={"class": "_aa_h"})
            profile_header = reel_div.find("header", attrs={"class": "x1gv9v1y x1dgd101 x186nx3s x1n2onr6 x2lah0s x1q0g3np x78zum5 x1qjc9v5 xlue5dm x1tb5o9v"})
            if profile_header:
                insta_user_name = profile_header.find("h2").text
                profile_url = profile_header.find("img")["src"]

                profile_div_list = profile_header.find_all("div", attrs={"class":"_aacl _aacp _aacu _aacx _aad6 _aade"})
                post_count = profile_div_list[0].find_all("span")[0].string
                followers_count = profile_div_list[1].find_all("span")[0].string
                following_count = profile_div_list[2].find_all("span")[0].string
                inner_text = [r.text.strip() for r in profile_header.find_all("div", attrs={"class": "_aa_c"})]
                bio = ' '.join(inner_text)

                private_account = reel_div.find("div", attrs={"class":"_aa_t"})
                private_account_status = True if private_account else False

                # print(insta_user_name, profile_url, post_count, followers_count, following_count, bio, private_account_status)
                
            else:
                page_exist_status = beautifulSoupText.find_all("h2")
                if len(page_exist_status) > 1:
                    if page_exist_status[0].text == '''"Sorry, this page isn't available."''':
                        account_exists_status = False
            
        user_df = user_df.append({
                                "user_id" : user_id,
                                "user_name" : user_name,
                                "insta_user_name" : insta_user_name, 
                                "profile_url" : profile_url, 
                                "post_count": post_count, 
                                "followers_count" : followers_count, 
                                "following_count" : following_count, 
                                "bio" : bio, 
                                "account_type" : private_account_status,
                                "account_exists_status" : account_exists_status
                            }, ignore_index=True)
        return user_df
        # else:
        #     with open(user_name + '.html', 'w') as f:
        #         f.write(beautifulSoupText.prettify())
    except Exception as e:
        traceback.print_exc()
        pass
    finally:
        return user_df