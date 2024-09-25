# -*- coding: utf-8 -*-

from kivymd.uix.screen import MDScreen

class StartupScreen(MDScreen):
    def __init__(self, view_model,  **kwargs):
        super().__init__(**kwargs)
        self.view_model = view_model


