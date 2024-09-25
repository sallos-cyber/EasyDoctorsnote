from kivy.app import App
from kivy.uix.settings import SettingsWithSidebar
from kivy.properties import ObjectProperty
from kivy.config import ConfigParser

class MyApp(App):
    config = ObjectProperty(None)

    def build(self):
        self.config = ConfigParser()  # Initialize the ConfigParser
        self.build_config(self.config)  # Build the config with defaults
        self.load_config()  # Load the config from the file
        return SettingsWithSidebar()

    def build_config(self, config):
        # Define the configuration options
        config.setdefaults('DEFAULT', {
            'password': '',
            'username': '',
            'email': ''
        })

    def load_config(self):
        # Load the configuration from the config file
        self.config.read('config.ini')

        # Access the configuration values
        if self.config.has_option('DEFAULT', 'password'):
            self.password = self.config.get('DEFAULT', 'password')
        else:
            self.password = ""

        if self.config.has_option('DEFAULT', 'username'):
            self.username = self.config.get('DEFAULT', 'username')
        else:
            self.username = ""

        if self.config.has_option('DEFAULT', 'email'):
            self.email = self.config.get('DEFAULT', 'email')
        else:
            self.email = ""

    def on_config_change(self, config, section, key, value):
        # Handle changes to the configuration
        print(f"Config changed: {key} = {value}")

if __name__ == '__main__':
    MyApp().run()

