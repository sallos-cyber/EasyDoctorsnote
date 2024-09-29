# -*- coding: utf-8 -*-
from kivy.event import EventDispatcher
from kivy.properties import ObjectProperty, StringProperty
from views.dialog_handler import DialogHandler
from utils.email_handler import EmailHandler
from kivy.logger import Logger
from kivymd.app import MDApp
from datetime import date
from typing import Optional, Tuple
from email.message import EmailMessage    


class ViewModel(EventDispatcher):

    current_email_text = StringProperty("no message for display")
    current_email = ObjectProperty(None)    
    
    def __init__(self, model, pw_handler, config, **kwargs):
        super().__init__(**kwargs)

        self.model = model
        self.pw_handler = pw_handler
        self.config = config
        self.dialog_handler = DialogHandler()
        self.email_handler = EmailHandler()
        self.current_email_text = "no text so far"
        self.current_email = None
        
        self.emails_to_send=[]
        self.email_pointer = 0


    def coordinate_email_send_process(self):
        """All necessary data has been collected. Now the emails must 
        be created, displayed and sent. There are n=2 emails to send.
        The current function cannot control the entire process, because as 
        soon as it calls the display method it has to return.
        It can only set a pointer to the first email to display.
        In the gui a user can then click the send button which triggers
        the send process of the email. Then the send process or else must move
        the pointer curr_email to the next email in the list self.emails_to_send.
        Also the display method has to be called again until all emails are sent.
        """
        #0) delete all entries from self.emails_to_send, because if someone pressed
        #the back button after emails have been genrated, to adjust the date
        #the list will contain those obsolete emails.
        self.emails_to_send.clear()
        
        #1) determine which emails should be send, generate them and make them available as member-variable
        if self.get_send_doctors_note():
            doctorsnote_email = self.compute_email("doctorsnote", self.get_date_range())
            self.emails_to_send.append({'email_indicator':'doctorsnote', 'email':doctorsnote_email, 'send_status':False})
            
        if self.get_cancel_lunch():
            cancel_lunch_email = self.compute_email("cancel_lunch", self.get_date_range())
            self.emails_to_send.append({'email_indicator':'cancel_lunch', 'email':cancel_lunch_email, 'send_status':False})
            
        Logger.debug(f'ViewModel: coordinate_email_send_process, {self.emails_to_send=}')
            
        #2)set the pointer curr_email to the first entry in the list, then call the display method
        #which will display the email and offers the send button to the user
        self.current_email = self.emails_to_send[self.email_pointer]['email']
        self.current_email_text = self.current_email.get_content()
        
        #3) display the current email
        self.display_email_screen()

    def send_curr_email(self):
        """the method simply send the email from self.emails_to_send that 
        self_email_pointer is pointing at
        It then increases the counter and if there are more emails to send it updates the pointer and 
        calls display_email_screen
        
        If there are no more emails to send - what to do? Show a message to close the app, or simply close it?"""
        
        Logger.debug(f'ViewModel:,{self.email_pointer=},{self.emails_to_send=}')
        #collect the necessary data from the config
        #smtpserver = DoctorsnoteApp.get_running_app().config.get('emailconfig','smtpserver')
        smtpserver = self.config.get('emailconfig','smtpserver')

        #port = DoctorsnoteApp.get_running_app().config.get('emailconfig','port')
        port = self.config.get('emailconfig','port')

        #get the password and decrypt!
        #passwd_encrypted = DoctorsnoteApp.get_running_app().config.get('sender','passwd')

        passwd_encrypted = self.config.get('sender','passwd')
        passwd = self.pw_handler.decrypt_password(passwd_encrypted)
        #Logger.debug(f'ViewModel: send_email, {self.get_send_doctors_note()=}, {self.get_send_doctors_note_send_status()=}')
        if self.email_pointer > len(self.emails_to_send):
            Logger.debug(f"ViewModel:send_curr_email, the {self.email_curr_index=} pointer exceeds {self.emails_to_send=} list length, exit!")
            #DoctorsnoteApp.stop()
            
            
        #if self.email_curr_index == 0: #doctorsnote
        #has the email already been sent?
        if self.emails_to_send[self.email_pointer]['send_status'] :
            Logger.debug("ViewModel:send_curr_email, the email has already been sent")
            #DoctorsnoteApp.stop()
        else:#email has not been sent
            Logger.debug('ViewModel:, send_curr_email, about to send email')
            if_successfully_sent, email_sent_feedback = self.email_handler.send_email(self.emails_to_send[self.email_pointer]['email'], smtpserver, port, passwd)
            Logger.debug(f"ViewModel:, send_email, {if_successfully_sent=}, {email_sent_feedback=}")
            self.dialog_handler.show_dialog(email_sent_feedback, self.dialog_handler.close_dialog)
            self.emails_to_send[self.email_pointer]['send_status'] = True

        #increase the counter and call display method again
        self.move_to_next_email()
        
            
    def move_to_next_email(self):
        """increase counter and display screen"""
        self.email_pointer += 1

        len_mails = len(self.emails_to_send)
        Logger.debug(f'ViewModel,  move_to_next_email, {self.email_pointer=}, {len_mails=})')
        if self.email_pointer >= len(self.emails_to_send):
            self.display_done_screen()
            return(0)
        
        Logger.debug(f'ViewModel, move_to_next_email after increase, {self.email_pointer=}')
        Logger.debug(f'ViewModel, move_to_next_email, {self.emails_to_send=}')

        self.current_email = self.emails_to_send[self.email_pointer]['email']
        self.current_email_text = self.current_email.get_content()
        
        #3) display the current email
        self.display_email_screen()
        
    def set_show_startup_checkbox(self):
        if self.model.show_startup_checkbox:
            self.model.show_startup_checkbox=False
        else:    
            self.model.show_startup_checkbox = True
            Logger.debug(f'ViewModel: set_show_startup_checkbox, {self.get_show_startup_checkbox=}')
        #remember this setting in the config file
        if self.get_show_startup_checkbox():
            self.config.set('app','show_startup', '1')
        else:
            self.config.set('app','show_startup','0')
        self.config.write()

    def get_show_startup_checkbox(self):
        return self.model.show_startup_checkbox
        
    def set_cancel_lunch_send_status(self, value):
        self.model.cancel_lunch_send_status = value
    def get_cancel_lunch_send_status(self):
        return self.model.cancel_lunch_send_status

    def set_send_doctors_note_send_status(self, value):
        self.model.send_doctors_note_send_status = value
    def get_send_doctors_note_send_status(self):
        return self.model.send_doctors_note_send_status
        
    def set_send_doctors_note(self):
        if self.model.send_doctors_note:
            self.model.send_doctors_note=False
        else:    
            self.model.send_doctors_note = True
    def get_send_doctors_note(self):
        return self.model.send_doctors_note
        
    def set_cancel_lunch(self):
        if self.model.cancel_lunch:
            self.model.cancel_lunch=False
        else:
            self.model.cancel_lunch=True
    def get_cancel_lunch(self):
        return self.model.cancel_lunch
    
    def set_date_range(self, date_range: list):
        Logger.debug('ViewModel: in set_date_range')
        Logger.debug(f'ViewModel: this is {date_range=}')
        self.model.date_range = date_range
        
    def get_date_range(self)->list:
        Logger.info('ViewModel: in get_date_range')
        Logger.info(f'{self.model.date_range=}')
        return self.model.date_range 
            
    def save_email_doctors_note(self, email_doctors_note_text):
        self.model.email_doctors_note_text = email_doctors_note_text
            
    def call_pick_date_screen(self, *args):
        """checks if options were chosen properly and then calls the next screen"""
        if not self.model.cancel_lunch and not self.model.send_doctors_note:
            self.dialog_handler.show_dialog("You need to choose an option, first", self.dialog_handler.close_dialog)
        else:
            MDApp.get_running_app().screen_manager.current = 'pick_date_screen'
    
    def are_dates_ok(self, date_range:list)->bool:
        #check if any date was chosen
        Logger.info('ViewModel: in are_dates_ok()')
        if len(date_range)==0:
            Logger.debug('ViewModel: len of date_range is null')
            self.dialog_handler.show_dialog("You need to pick a date.", self.dialog_handler.close_dialog)
            Logger.debug('PickDateScreen: the dates are not ok - no date chosen')

            return False
        #if a date was chosen, is it a valid one or in the past?
        Logger.debug(f'ViewModel: {len(date_range)=}')
        from_date=date_range[0]
        Logger.debug(f'ViewModel: this is {from_date=}')
        if from_date < date.today():
            self.dialog_handler.show_dialog("The chosen date is in the past. Pick a different date.", self.dialog_handler.close_dialog)
            Logger.debug('PickDateScreen: the dates are not ok- dates in the past')
            return False
        return True
        
    def compute_from_to_date_from_list(self, date_range:list)->Tuple[str, Optional[str]]:
        """
        date_range is a list, but for the email text, it must be eiter a from_date
        and the to_date is None, or both dates in the appropriate format

        Parameters
        ----------
        date_range : List
            DESCRIPTION.

        Returns
        -------
        from_date : date
        to_date : date or None
        """
        from_date = date_range[0].strftime("%d.%m.%Y")
        to_date=None
        Logger.debug(f'ViewModel:,compute_from_to_date, {date_range=}')
        if len(date_range)>1:
            to_date=date_range[len(date_range)-1].strftime("%d.%m.%Y")

        return from_date, to_date
        

    def compute_email(self, email_indicator:str,  date_range:list)->EmailMessage:
        Logger.debug('ViewModel: in prepare_show_email_screen')
        Logger.debug(f'ViewModel: this is the date_range in the view_model: {self.model.date_range=}')
        from_date, to_date = self.compute_from_to_date_from_list(date_range)

        if email_indicator=="doctorsnote":
            #self.model.send_doctors_note = False # this might raise a problem when the back button is pressed
            email_doctors_note = self.email_handler.create_doctors_note_email(self.config['app']['language'],self.config['emailconfig']['senderemail'], 
                                          self.config['emailconfig']['receiveremails_doctorsnote'],
                                          self.config['emailconfig']['receiveremails_doctorsnote_cc'],
                                          self.config['sender']['sendername'],
                                          self.config['kid']['kidname'],
                                          self.config['kid']['classid'],
                                          from_date,
                                          to_date
                                          )
            Logger.debug(f'ViewModel: in compute_email, doctors_note, {email_doctors_note=}')
            return email_doctors_note  
       
        if email_indicator=="cancel_lunch":
            #self.model.cancel_lunch = False
            cancel_lunch_note = self.email_handler.create_cancel_lunch_email(self.config['app']['language'],self.config['emailconfig']['senderemail'], 
                                          self.config['emailconfig']['receiveremails_lunch'],
                                          self.config['sender']['sendername'],
                                          self.config['kid']['kidname'],
                                          self.config['kid']['classid'],
                                          from_date,
                                          to_date
                                          )
            return cancel_lunch_note
        

        
    def get_doctors_note_email(self):
        Logger.debug('ViewModel: get_doctors_note_email')
        #date_range = self.get_date_range()
        #config = MDApp.get_running_app().config
        #email= self.email_handler.prepare_doctors_note_mail(date_range, config)
        #Logger.debug('ViewModel: in get_doctors_note_email')
        Logger.debug(f'ViewModel:{self.email_text=}')
        return "  fajlskdf"#self.email_text

    def display_email_screen(self):
            MDApp.get_running_app().screen_manager.current = 'show_email_screen'
            
    def display_done_screen(self):
         MDApp.get_running_app().screen_manager.current = 'show_done_screen'
 
