from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import ObjectProperty, ConfigParserProperty
from kivy.logger import Logger, LOG_LEVELS
from views.startup_screen import StartupScreen
from views.show_email_screen import ShowEmailScreen
from views.show_done_screen import ShowDoneScreen
from views.pick_date_screen import PickDateScreen
from utils.password_handler import PasswordHandler
from utils.password_settings import PasswordSettings
from viewmodels.view_model import ViewModel
from models.data_model import DataModel

Logger.setLevel(LOG_LEVELS["debug"])

class ScreenManagement(ScreenManager):
    
    def __init__(self, view_model, show_startup:bool, **kwargs):
        super().__init__(**kwargs)
        # Gemeinsames Model
        # model = DataModel()
        # view_model = ViewModel(model)
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


"""Using MVVM Pattern: First some required user inputs are collected. This data
is stored in the DataModel class. The check of the data and some control
is done in the ViewModel class  It also updates the model"""




    
        
class MainScreen(MDScreen):
    
    """ Lets you choose if you want to send  a "cancel_lunch" and/Or a 
    "send_doctors_note" notification to school.
    
    """  

        
    def __init__(self, view_model, **kwargs):
        super().__init__(**kwargs)
        self.view_model = view_model
        

        
class DoctorsnoteApp(MDApp):
    email_receiver_doctors_note = ConfigParserProperty('defaultvale','emailconfig','receiveremails_doctorsnote','configparser')

    config = ObjectProperty(None) 
    
    def build_config(self, config):
        config.setdefaults( 'emailconfig',{
            'senderemail':'john@doe.com',
            'receiveremails_doctorsnote':'xxx@xxx.xx',
            'receiveremails_doctorsnote_cc': '',
            'receiveremails_lunch':'xxx@xxx.xx',
            'smtpserver':'smtp.xxx.xx',
            'port':000})
        config.setdefaults( 'kid',{
            'kidname':'Jane Doe',
            'classid':'xx'})
        config.setdefaults( 'sender',{
            'sendername':'John Doe',
            'passwd':'xxx'})
        config.setdefaults( 'app',{
            'first_use':'1'})
        config.setdefaults( 'app',{
            'show_startup': 0})

    
    def build(self):
        
        self.pw_handler = PasswordHandler()
        #self.create_secret_key()  

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
        Logger.debug(f'DoctorsnoteApp: builder, {self.show_startup()=}')
        self.screen_manager = ScreenManagement(view_model, self.show_startup())

        # Return the screen manager as the root widget
        return self.screen_manager


        
    def on_config_change(self, config, section, key, value):
        if key == 'passwd':
            Logger.debug('DoctorsnoteApp: on_config_change, the user has changed the password!')
            # Ensure 'value' is in bytes
            # if isinstance(value, str):
            #     value = value.encode('utf-8')  # Convert string to bytes
            
            self.save_passwd(value)

          
    def save_passwd(self, password):
        encrypted_password = self.pw_handler.encrypt_password(password)
        self.config.set('sender', 'passwd', encrypted_password.decode())
        self.config.write()
    def build_settings(self, settings):
         settings.add_json_panel('Settings Panel', self.config, 'config.json')
         
    def if_used_first_time(self):
        if self.config['app']['first_use']=='1':

            #self.config.write()
            return True
        else:
            return False
        
    def show_startup(self):
        Logger.debug('NoteApp:, show_startup()')
        if self.config['app']['show_startup']=='1':
            self.config.write()
            return False
        else:
            return True        
             
    def set_colors(self):
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
        

    
if __name__=='__main__':
    DoctorsnoteApp().run()
    

class AnotherScreen(MDScreen):
    pass
