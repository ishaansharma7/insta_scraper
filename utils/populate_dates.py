from dateutil.parser import parse
import pandas as pd
from datetime import datetime, timedelta
from pprint import pprint
from data.send_data_to_apis import populate_reels_date

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
