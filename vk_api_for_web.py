import vk_api
import settings


class VkApiForWeb:
    def __init__(self, login, password='', with_app=False):
        if with_app:
            self.session = vk_api.VkApi(
                app_id=settings.vk_app, client_secret=settings.vk_key,
                login=login, password=password, scope='users, friends',
                api_version='5.80'
            )
        else:
            self.session = vk_api.VkApi(
                login=login, scope='users, friends, groups'
            )

        try:
            self.session.auth(reauth=with_app)
            self.error = None
        except vk_api.AuthError:
            self.error = 'Ошибка авторизации'
        except:
            self.error = 'Произошла ошибка. Попробуйте еще раз'
