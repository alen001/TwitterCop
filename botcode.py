import tweepy
import logging
from config import create_api
import time
from oauth2client.service_account import ServiceAccountCredentials
from gspread import client
import gspread

scope = ['https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name('theKey.json',scope)
client = gspread.authorize(creds)
python_test = client.open("TweetCop Data").sheet1
i=2
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def check_mentions(api, since_id):
    logger.info("Retrieving mentions")
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline,
        since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        i=2
        logger.info(f"Answering to {tweet.user.name}")
        statusa = api.get_status(tweet.id, tweet_mode = "extended")
        full_text = statusa.full_text
        save_t = str(tweet.id)
        print("The text of the status is : \n\n" + full_text)
        

        if tweet.in_reply_to_status_id is not None:
            
            parent_tweet=api.get_status(tweet.in_reply_to_status_id)
            statusb = api.get_status(parent_tweet.id, tweet_mode = "extended")
            replytwt = statusb.full_text
            print(parent_tweet.user.screen_name+": "+replytwt)
        else:
            replytwt = "."            
           
        
        msg = "Your complaint has been registered"
        api.send_direct_message(tweet.user.id, msg)
        save_f = "https://twitter.com/twitter/statuses/" + save_t
        python_test.update_cell(i,2,save_f) 
        i=i+1
        
    return new_since_id

def main():
    api = create_api()
    since_id = 1
    
    while True:
        since_id = check_mentions(api, since_id)
        print (since_id)
        logger.info("Waiting...")
        time.sleep(60)

if __name__ == "__main__":
    main()