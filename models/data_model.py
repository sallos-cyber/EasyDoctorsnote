# -*- coding: utf-8 -*-

from kivy.logger import Logger

class DataModel:
    def __init__(self):
        #get this from MainScreen
        self.cancel_lunch = False
        self.send_doctors_note = False
        self.cancel_lunch_send_status = False
        self.send_doctors_note_send_status = False
        self.show_startup_checkbox = False
        #from  PickDateScreen
        self.date_range = []
        self.email_list = []
        

    @property
    def show_startup_checkbox(self):
        return self._show_startup_checkbox
    
    @property
    def cancel_lunch(self):
        return self._cancel_lunch
    
    @property
    def send_doctors_note(self):
        return self._send_doctors_note
    
    @property
    def date_range(self):
        Logger.debug('DataModel: in get date_range')
        return self._date_range
    
    @property
    def cancel_lunch_send_status(self):
        return self._cancel_lunch_send_status
    
    @property
    def send_doctors_note_send_status(self):
        return self._send_doctors_note_send_status
    
    @show_startup_checkbox.setter
    def show_startup_checkbox(self, value):
        self._show_startup_checkbox = value
        
    @cancel_lunch.setter
    def cancel_lunch(self, value):
        self._cancel_lunch = value
    
    @send_doctors_note.setter
    def send_doctors_note(self, value):
        self._send_doctors_note = value

    @date_range.setter
    def date_range(self, value):
        Logger.debug(f'DataModel: setting date_range to {value}')
        Logger.debug('DataModel: date range in the model is updated')
        self._date_range = value
        
    @send_doctors_note_send_status.setter
    def send_doctors_note_send_status(self, value):
        Logger.debug(f'Model:send_doctors_note_send_status.setter {value=}')
        self._send_doctors_note_send_status = value
        
    @cancel_lunch_send_status.setter
    def cancel_lunch_send_status(self, value):
        Logger.debug(f'Model:cancel_lunch_send_status.setter {value=}')
        self._cancel_lunch_send_status = value
        