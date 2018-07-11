# Social Graph
Learn Python graduation project

#### settings.py

vk_app = 0000000

vk_key = 'SoMeKeY'

vk_service_key = 'SoMeKeY'

arangodb_root_password = 'SoMeRoOtPaSsWoRd'

arangodb_user = 'arangodb_user'

arangodb_user_password = 'SoMePaSsWoRd'

#### uwsgi

uwsgi --ini social_graph.ini --set-placeholder base_dir=/your/custom/path/to/app/dir
