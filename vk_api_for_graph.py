import vk
import settings


class VkApiForGraph:
    def __init__(self):
        self.session = vk.Session(access_token=settings.vk_service_key)
        self.api = vk.API(self.session, v='5.78')

    def get_friends(self, user_id):
        try:
            friends = self.api.friends.get(user_id=user_id)
        except vk.exceptions.VkAPIError:
            friends = {'items': []}
        # Limit number of loaded friends for development
        # TODO: remove limitation in production
        friends_list = friends.get('items', [])[:20]

        return friends_list
