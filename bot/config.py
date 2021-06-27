import tweepy
import logging
import os

logger = logging.getLogger()

def create_api():
    
    auth = tweepy.OAuthHandler('xxxxxxxxxxxxxxxl','gxxxxxxxxxxxxxxxxxxU')
    auth.set_access_token('1xxxxxxxxxxxxxxxxxxxxxxxxx','xxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
    api = tweepy.API(auth, wait_on_rate_limit=True, 
        wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API created")
    return api
