# -*- coding: utf-8 -*-
from kivy.properties import ObjectProperty
from kivymd.uix.screen import MDScreen

class ShowDoneScreen(MDScreen):

    view_model = ObjectProperty(None)
    """ only displays a 'you are done message'
    """
    def __init__(self, view_model,  **kwargs):
        super().__init__(**kwargs)
        self.view_model = view_model

# -*- coding: utf-8 -*-

