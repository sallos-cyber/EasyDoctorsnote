from kivy.lang import Builder
from kivy.logger import Logger, LOG_LEVELS
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp

from models.data_model import DataModel
from utils.password_handler import PasswordHandler
from utils.password_settings import PasswordSettings
from viewmodels.view_model import ViewModel
from views.main_screen import MainScreen
from views.pick_date_screen import PickDateScreen
from views.show_done_screen import ShowDoneScreen
from views.show_email_screen import ShowEmailScreen
from views.startup_screen import StartupScreen

Logger.setLevel(LOG_LEVELS["debug"])

class ScreenManagement(ScreenManager):
    """
    A class to manage all screens.

    Attributes:
    ----------
    view_model : ViewModel
        The ViewModel contains controls
    show_startup : bool
        A config parameter which determines if a startup screen is added or not.
    """
    def __init__(self, view_model:ViewModel, show_startup: bool, **kwargs):
        super().__init__(**kwargs)
        Logger.debug(f'ScreenManagement: {show_startup=}')
        if show_startup:
            startup_screen = StartupScreen(view_model, name='startup_screen')
            self.add_widget(startup_screen)

        main_screen = MainScreen(view_model, name='main_screen')
        pick_date_screen = PickDateScreen(view_model, name='pick_date_screen')
        show_email_screen = ShowEmailScreen(view_model, name='show_email_screen')
        show_done_screen = ShowDoneScreen(view_model, name='show_done_screen')

        self.add_widget(main_screen)
        self.add_widget(pick_date_screen)
        self.add_widget(show_email_screen)
        self.add_widget(show_done_screen)


class EasyDoctorsnoteApp(MDApp):
    """
    The main entry point into the app EasyDoctorsnote.

    The app first presents a couple of screens in which user inputs are selected.
    These are stored in the Config, the ViewModel and Model. Once all the required
    information is available the according actions can be triggered, which in this
    case is the sending of emails.
    """
    config = ObjectProperty(None)

    def build_config(self, config:dict)-> None:
        config.setdefaults('emailconfig', {
            'senderemail': 'john@doe.com',
            'receiveremails_doctorsnote': 'xxx@xxx.xx',
            'receiveremails_doctorsnote_cc': '',
            'receiveremails_lunch': 'xxx@xxx.xx',
            'smtpserver': 'smtp.xxx.xx',
            'port': 587})
        config.setdefaults('kid', {
            'kidname': 'Jane Doe',
            'classid': 'xx'})
        config.setdefaults('sender', {
            'sendername': 'John Doe',
            'passwd': 'xxx'})
        config.setdefaults('app', {
            'first_use': '1'})
        config.setdefaults('app', {
            'show_startup': 0})
        config.setdefaults('app', {
            'language': 'German'})

    def build(self)-> ScreenManagement:
        self.pw_handler = PasswordHandler()
        self.settings_cls = PasswordSettings
        self.use_kivy_settings = False
        self.set_colors()

        Builder.load_file("kv/main_screen.kv")
        Builder.load_file("kv/pick_date_screen.kv")
        Builder.load_file("kv/show_done_screen.kv")
        Builder.load_file("kv/show_email_screen.kv")
        Builder.load_file("kv/startup_screen.kv")
        Builder.load_file("kv/topbar.kv")

        model = DataModel()
        view_model = ViewModel(model, self.pw_handler, self.config)
        Logger.debug(f'EasyDoctorsnoteApp: builder, {self.show_startup()=}')
        self.screen_manager = ScreenManagement(view_model, self.show_startup())

        # Return the screen manager as the root widget
        return self.screen_manager

    def on_config_change(self, config:dict, section:str, key:str, value:str)-> None:
        if key == 'passwd':
            Logger.debug('EasyDoctorsnoteApp: on_config_change, the user has changed the password!')
            self.save_passwd(value)

    def save_passwd(self, password:str)->None:
        encrypted_password = self.pw_handler.encrypt_password(password)
        self.config.set('sender', 'passwd', encrypted_password.decode())
        self.config.write()

    def build_settings(self, settings)->None:
        settings.add_json_panel('Settings Panel', self.config, 'config.json')

    def if_used_first_time(self)-> None:
        if self.config['app']['first_use'] == '1':
            return True
        else:
            return False

    def show_startup(self)-> None:
        Logger.debug('NoteApp:, show_startup()')
        if self.config['app']['show_startup'] == '1':
            self.config.write()
            return False
        else:
            return True

    def set_colors(self)-> None:
        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.primary_hue = "500"
        # Define custom colors
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.accent_palette = "Amber"
        self.theme_cls.primary_color = [0.0, 0.5, 0.5, 1]  # Teal
        self.theme_cls.secondary_palette = "Amber"
        self.theme_cls.secondary_color = [1.0, 0.75, 0.0, 1]  # Amber
        self.theme_cls.hint_color = [0.5, 0.5, 0.5, 1]  # Grey
        self.theme_cls.error_color = [1.0, 0.0, 0.0, 1]  # Red

if __name__ == '__main__':
    EasyDoctorsnoteApp().run()

