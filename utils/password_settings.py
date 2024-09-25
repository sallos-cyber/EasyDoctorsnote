#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

#took this code from this awesome post!!!
#https://www.reddit.com/r/kivy/comments/cujmfc/kivy_password_setting/
"""
#password_settings.py

from kivy.uix.settings import SettingString 
from kivy.uix.label import Label

class PasswordString(SettingString):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    #overriding parent function
    # Change textinput in the popup into a password field
    def _create_popup(self, instance):
        super()._create_popup(instance)
        #self.textinput.password=True
        self.textinput.allow_copy=False
    
    # overriding parent function
    # When settings panel is being constructed,
    # and if widget being added is a Label, replace it's text
    def add_widget(self, widget, *largs):
        
        if isinstance(widget, Label):
    
            widget = Label(
                text='[color=808080]Click to enter password[/color]',
                markup = True
            )
    
        super().add_widget(widget, *largs)
        
#from kivy.uix.settings import SettingsWithSidebar

from kivy.uix.settings import SettingsWithTabbedPanel

#Sub
class PasswordSettings(SettingsWithTabbedPanel):
    
    """ Settings panel that can use a password field """

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.register_type('password', PasswordString)