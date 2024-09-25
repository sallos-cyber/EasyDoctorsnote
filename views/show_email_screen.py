# -*- coding: utf-8 -*-
from email.message import EmailMessage    
from kivymd.uix.screen import MDScreen
from kivy.properties import ObjectProperty, StringProperty, NumericProperty

class ShowEmailScreen(MDScreen):
    
    view_model = ObjectProperty(None)
    emailtext_to_be_displayed = StringProperty("keine Email")
    email_curr = ObjectProperty()
    email_curr_index = NumericProperty()

    
    def __init__(self, view_model,  **kwargs):
        super().__init__(**kwargs)
        self.view_model = view_model
        view_model.bind(current_email_text=self.get_current_email_text)
        view_model.bind(current_email=self.get_curr_email)
        
    def get_curr_email(self, instance, current_email):
        self.email_curr = current_email
        
    def get_current_email_text(self, instance, email_text):
        self.emailtext_to_be_displayed = email_text       
           # -*- coding: utf-8 -*-

