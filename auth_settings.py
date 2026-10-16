AUTH_METHODS = ()
AUTH_SERVER_URL = ''
APP_NAME = 'ZONE'
APP_LOGO = ''
APP_LOGO_TEXT = 'ZO'
LOGIN_ENABLED = False
UI_COMPONENTS = ('logo', 'home', 'menu')
MENU_ITEMS = ({'label': 'na', 'action': 'home', 'message': '', 'row': 1, 'column': 1, 'width': 120, 'height': 40},)
HOME_CONFIG = {'eyebrow': 'YOUR NEXT CHAPTER', 'title': 'Welcome home.', 'description': 'A calmer place to explore, create, and keep everything in one place.', 'cards': [{'title': 'Discover', 'description': 'Find ideas and explore what is new.'}, {'title': 'Make it yours', 'description': 'Your tools and preferences, all in one place.'}, {'title': 'Stay in sync', 'description': 'Pick up where you left off whenever you return.'}]}
BUTTON_STYLE_ENABLED = True
BUTTON_STYLE = {'color': '#00A85A', 'hover_color': '#00C46A', 'text_color': '#07140D', 'width': 120, 'height': 40}
import os
API_BASE_URL = os.environ.get('API_BASE_URL', 'http://127.0.0.1:5002').rstrip('/')
