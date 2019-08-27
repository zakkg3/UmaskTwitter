import tweepy
from simple_settings import settings
import os


os.environ[ 'SIMPLE_SETTINGS'] = 'umask_config'


def debug_print(text):
    """Print text if debugging mode is on"""
    if settings.debug:
        print (text)


def get_last_id(statefile):
    """Retrieve last status ID from a file"""

    debug_print('Getting last ID from %s' % (statefile,))
    try:
        f = open(statefile,'r')
        id = int(f.read())
        f.close()
    except IOError:
        debug_print('IOError raised, returning zero (0)')
        return 0
    debug_print('Got %d' % (id,))
    return id


def save_id(statefile,id):
    """Save last status ID to a file"""
    last_id = get_last_id(statefile)

    if last_id < id:
        debug_print('Saving new ID %d to %s' % (id,statefile))
        f = open(statefile,'w')
        f.write(str(id)) # no trailing newline
        f.close()
    else:
        debug_print('Received smaller ID, not saving. Old: %d, New: %s' % (
            last_id, id))

def add_trolls(tweet):
    debug_print('Agregando trolles')

# Authenticate to Twitter
auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

try:
    api.verify_credentials()
    debug_print("Authentication OK")
except:
    debug_print("Error during authentication")

# tweets = []
last_id = get_last_id(settings.last_id_file)
# debug_print ("Busqueda:")
# debug_print (settings.busqueda)
# search_terms = settings.busqueda
# tweets = api.search(q=search_terms,since_id=last_id,count=3)
# 
# for tweet in tweets:
#     print(f'{tweet.id} ----- {tweet.text}')
#     tweet.text = '#antitroll'+tweet.text
#     #api.retweet(tweet.id)
#     save_id(settings.last_id_file,tweet.id)

public_tweets = api.mentions_timeline() #since_id=last_id)
for mention in public_tweets:
    print(f'{mention.id} ----- {mention.text}')
    # save_id(settings.last_id_file,mention.id)
    if '#macritrolldetected' in mention.text:
        debug_print("trolltdeteted!!")
        if '#esuntrolldemacri' in mention.text:
            debug_print("Quiere preguntar y agregar!")
            api.send_direct_message(recipient_id=mention.user.id, text=' Ei '+mention.user.name+' no podes denunciar un troll y preguntar en el emismo tweet')
        else:
            add_trolls(mention)
