import kivy
import os
from kivy.utils import platform
from kivy.config import Config
Config.set('kivy', 'keyboard_mode', 'dock' if platform in ('win', 'linux', 'macosx') else 'system')
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from auth_settings import APP_LOGO, APP_NAME, LOGIN_ENABLED
from database.db_helper import DatabaseHelper

Window.clearcolor = (0.1, 0.1, 0.1, 1)
from ui.home_screen import MainScreen, SettingsScreen

class iOSApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = APP_NAME
        self.icon = APP_LOGO if APP_LOGO and os.path.isfile(APP_LOGO) else ''
        self.sm = None
    
    def build(self):
        self.database = DatabaseHelper()
        self.sm = ScreenManager()
        self.sm.add_widget(MainScreen(name='main'))
        
        if LOGIN_ENABLED:
            self.sm.add_widget(SettingsScreen(name='settings'))
            try:
                from login.login_screen import LoginScreen
                from login.register_screen import RegisterScreen
                from login.verification_screen import VerificationScreen
                
                login_screen = LoginScreen(
                    on_login_success=self.on_login_success,
                    on_register_click=self.go_to_register
                )
                login_screen.name = 'login'
                self.sm.add_widget(login_screen)
                
                register_screen = RegisterScreen(
                    on_register_success=self.on_register_success,
                    on_login_click=self.go_to_login
                )
                register_screen.name = 'register'
                self.sm.add_widget(register_screen)
                
                verification_screen = VerificationScreen(
                    email="",
                    on_verification_success=self.on_verification_success,
                    on_resend_code=self.resend_verification_code
                )
                verification_screen.name = 'verification'
                self.sm.add_widget(verification_screen)
            except Exception as error:
                raise RuntimeError("Could not load the login screens.") from error
        
        return self.sm
    
    def go_to_login(self, instance=None):
        if self.sm:
            self.sm.current = 'login'
    
    def go_to_register(self, instance=None):
        if self.sm:
            self.sm.current = 'register'
    
    def resend_verification_code(self, instance=None):
        pass
    
    def on_login_success(self, response):
        print("Login successful!", response)
        if self.sm:
            self.sm.get_screen('main').set_authenticated(response)
            self.sm.current = 'main'
    
    def on_register_success(self, response):
        print("Registration successful!", response)
        if self.sm:
            self.sm.current = 'login'
    
    def on_verification_success(self, response):
        print("Verification successful!", response)
        if self.sm:
            self.sm.get_screen('main').set_authenticated(response)
            self.sm.current = 'main'

if __name__ == '__main__':
    iOSApp().run()
