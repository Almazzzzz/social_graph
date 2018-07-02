import vk
import settings

session = vk.Session(access_token=settings.vk_service_key)
api = vk.API(session, v='5.78')


def get_friends(user_id):
    # user = api.users.get(user_ids=user_id)
    try:
        friends = api.friends.get(user_id=user_id)
    except vk.exceptions.VkAPIError:
        friends = { 'items': [] }
    friends_list = friends.get('items', [])

    return friends_list
