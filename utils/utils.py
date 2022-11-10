import traceback
from data import process_batch
from datetime import datetime
from utils.fb_apis import get_user_details_from_api, get_details_from_response

def user_details_from_api_scrapper(user):
    start_time = datetime.now()
    print("start time", start_time) 
    try:
        if user:
            acc_name = user.get("acc_name").strip()
            user["acc_name"] = acc_name
            if acc_name:
                response = get_user_details_from_api(user)
                if response:
                    get_details_from_response(user, response)
                else:
                    process_batch.start_batch_processing({acc_name : user.get("user_id")})
        end_time = datetime.now()
        print("end time", end_time)
        print(end_time - start_time)
    except Exception as e:
        traceback.print_exc()
