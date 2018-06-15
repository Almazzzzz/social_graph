import vk
import settings

session = vk.Session(access_token=settings.vk_service_key)
api = vk.API(session, v='5.78')


def get_friends(user_id):
    user = api.users.get(user_ids=user_id)
    friends_list = api.friends.get(user_id=user_id)

    print(user, friends_list)


get_friends(1001)
