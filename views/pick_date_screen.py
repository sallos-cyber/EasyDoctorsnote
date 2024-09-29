# -*- coding: utf-8 -*-
from kivymd.uix.screen import MDScreen
from kivy.properties import ObjectProperty
from .dialog_handler import DialogHandler
from kivymd.uix.pickers import MDModalDatePicker
from kivy.logger import Logger

class PickDateScreen(MDScreen):
    """Screen for picking a date range and coordinating email sending."""

    view_model = ObjectProperty(None)

    def __init__(self, view_model,  **kwargs)->None:
        """Initialize the PickDateScreen with a view model."""
        super().__init__(**kwargs)
        self.dialog_handler = DialogHandler()
        self.view_model = view_model

        
    def show_date_dialog(self,dialog_text)->None:
        """Show a dialog with the specified text."""
        self.dialog_handler.show_dialog("This is Screen One", self.dialog_handler.close_dialog)

    def show_modal_date_picker(self, *args)->None:
        """Open a modal date picker for selecting a date range."""
        date_dialog = MDModalDatePicker(mode="range")
        date_dialog.bind(on_ok=self.finish_data_collection_and_trigger_actions, on_cancel=self.on_cancel)
        date_dialog.open()

    def finish_data_collection_and_trigger_actions(self, instance_date_picker):
         """Handle the date selection and trigger actions based on the selected dates."""
         date_range = instance_date_picker.get_date()
         Logger.debug('PickDateScreen: setting date_range in on_ok()')
         if  self.view_model.are_dates_ok(date_range):
            self.view_model.set_date_range(date_range)
            instance_date_picker.dismiss()
            Logger.debug("PickDateScreen: calling view_model.coordinate_email_send_process, data callection completed, trigger action now")
            self.view_model.coordinate_email_send_process()

    def on_cancel(self, instance_date_picker)->None:
        """Handle the cancellation of the date picker."""
        instance_date_picker.dismiss()
        
