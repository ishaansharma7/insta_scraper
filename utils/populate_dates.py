import pandas as pd
from data.send_data_to_apis import populate_reels_date
from datetime import datetime
import traceback
from dateutil.parser import parse


def gen_date_range(start_date, end_date, periods):
    datelist = pd.date_range(start=start_date, end=end_date, periods=periods)
    return reversed(datelist.to_list())


def populate_reel_dates(m_index, shortcode_set, shortcode_and_date):
    local_date = {}
    l_index = 0
    o_index = len(shortcode_set) - 1
    # between latest and mid
    if m_index - l_index -1 >= 1:
        # find date intervals and populate dates
        intervals = m_index - l_index -1
        start_date = shortcode_and_date[shortcode_set[m_index]]
        end_date = shortcode_and_date[shortcode_set[l_index]]
        date_range = gen_date_range(start_date, end_date, 2+intervals)
        curr_date = {curr_code: str(its_date) for curr_code, its_date in zip(shortcode_set[l_index:m_index+1], date_range)}
        local_date.update(curr_date)
    if o_index - m_index - 1 >= 1:
        intervals = o_index - m_index -1
        start_date = shortcode_and_date[shortcode_set[o_index]]
        end_date = shortcode_and_date[shortcode_set[m_index]]
        date_range = gen_date_range(start_date, end_date, 2+intervals)
        curr_date = {curr_code: str(its_date) for curr_code, its_date in zip(shortcode_set[m_index:o_index+1], date_range)}
        local_date.update(curr_date)
    # pprint(local_date)
    # pprint(shortcode_set)
    populate_reels_date(local_date)



def can_populate_post(scraped_post_list):
    if len(scraped_post_list) >= 10:
        date_count = 0
        for each_post in scraped_post_list:
            if each_post['media_date']: date_count += 1
        if date_count >= 5:
            return True
    return False

def remove_pinned_post(scraped_post_list):
    pinned_idx = 0
    len_post_list = len(scraped_post_list)
    for idx in range(0, len_post_list):
        post_dict = scraped_post_list[idx]
        if 'pinned_post' in post_dict and post_dict['pinned_post'] == True:
            pinned_idx += 1
        else:
            break
    return scraped_post_list[pinned_idx:]


def populate_posts_date(scraped_post_list=[]):
    try:
        # scraped_post_list = SCRAPED_POST_LIST
        print('populate posts -----')
        if not can_populate_post(scraped_post_list): return
        rmv_pinned_list = remove_pinned_post(scraped_post_list)
        len_post_list = len(rmv_pinned_list)
        left_date_idx = 0
        missed_date = False
        for idx in range(0, len_post_list):
            post_dict = rmv_pinned_list[idx]
            if idx == 0 and not post_dict['media_date']:    # always give date to latest post
                post_dict['media_date'] = str(datetime.now().date())
                left_date_idx = idx
                continue
            if post_dict['media_date'] and not missed_date:
                left_date_idx = idx
                continue
            if not post_dict['media_date']:
                missed_date = True
                continue
            if post_dict['media_date'] and missed_date:
                missed_date = False
                # print('indexs:',left_date_idx, ',',idx)
                fill_date_in_posts(left_date_idx, idx, rmv_pinned_list)
                left_date_idx = idx
        if missed_date:
            last_date = rmv_pinned_list[left_date_idx]['media_date']
            for i in range(left_date_idx+1, len_post_list):
                post_dict = rmv_pinned_list[i]
                post_dict['media_date'] = last_date
        # print(rmv_pinned_list)
    except Exception:
        traceback.print_exc()


def date_range(start_date, end_date, intervals):
    date_list = []
    # start_date = datetime.strptime(start_date, '%Y-%m-%d')
    start_date = parse(str(start_date))
    # end_date = datetime.strptime(end_date, '%Y-%m-%d')
    end_date = parse(str(end_date))
    interval = (end_date - start_date) / intervals
    for i in range(intervals+1):
        date_list.append(str(start_date + interval * i))
    # print()
    # print('intervals:', intervals)
    # print('start_date:', start_date)
    # print('end_date:', end_date)
    # print(date_list)
    # print()
    return date_list

def fill_date_in_posts(left_date_idx, idx, scraped_post_list):
    start_date = scraped_post_list[idx]['media_date']
    end_date = scraped_post_list[left_date_idx]['media_date']
    date_list = date_range(start_date, end_date, idx-left_date_idx)
    for i in range(left_date_idx, idx + 1):
        post_dict = scraped_post_list[i]
        post_dict['media_date'] = date_list[-1]
        date_list.pop()