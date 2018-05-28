from .models import User

def add_users(results):
    num = 0
    for status in results:
        user = status['user']
        obj, created = User.objects.update_or_create(
            user_id=user['id'],
            defaults={'screen_name':user['screen_name'],
            'statuses_count':user['statuses_count'],
            'following':user['friends_count'],
            'followers':user['followers_count'],
            'likes':user['favourites_count']
            }
            )
        if created: num+=1
    print("Users added: %s" % num)
def temp():

    print("TEMP IS WORKING>>>")

