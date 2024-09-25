# -*- coding: utf-8 -*-
from kivymd.uix.screen import MDScreen
from kivy.properties import ObjectProperty
from .dialog_handler import DialogHandler
from kivymd.uix.pickers import MDModalDatePicker
from kivy.logger import Logger

class PickDateScreen(MDScreen):
    
    view_model = ObjectProperty(None)
    """ Lets you pick a date
    """
    def __init__(self, view_model,  **kwargs):
        super().__init__(**kwargs)
        self.dialog_handler = DialogHandler()
        self.view_model = view_model

        
    def show_date_dialog(self,dialog_text):
        self.dialog_handler.show_dialog("This is Screen One", self.dialog_handler.close_dialog)

    def show_modal_date_picker(self, *args):
            date_dialog = MDModalDatePicker(mode="range")
            date_dialog.bind(on_ok=self.finish_data_collection_and_trigger_actions, on_cancel=self.on_cancel)
            date_dialog.open()
            
    def finish_data_collection_and_trigger_actions(self, instance_date_picker):
        """now the data collection is finished: 
        which email to write
        the dates
        the config
        This should be controlled by the main app, which can 
        give it to the EmailHandler. 
        The EmailHandler creates two emails and these get presented by the show email screen
        """
        date_range = instance_date_picker.get_date()
        Logger.debug('PickDateScreen: setting date_range in on_ok()')
        if  self.view_model.are_dates_ok(date_range):
            self.view_model.set_date_range(date_range)
            instance_date_picker.dismiss()
            Logger.debug("PickDateScreen: calling view_model.coordinate_email_send_process, data callection completed, trigger action now")
            self.view_model.coordinate_email_send_process()          

    def on_cancel(self, instance_date_picker):
        instance_date_picker.dismiss()
        
