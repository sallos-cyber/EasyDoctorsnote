# -*- coding: utf-8 -*-

from kivy.logger import Logger
from email.message import EmailMessage    

from smtplib import SMTP

class EmailHandler:
            
    def send_email(self, email:EmailMessage, smtpserver:str, port:int, passwd:str)->bool:
        Logger.info('EmailHandler: I am in send_mail')
        Logger.info(f'EmailHandler: {email=}')
        Logger.info(f'sm: {email=}')
        try:
            with SMTP(smtpserver, port) as server:
                server.starttls()
                server.login(email['From'],passwd)
                if email['Cc'] == None:     
                    server.sendmail(email['From'], [email['To']], email.as_string())
                else:
                    server.sendmail(email['From'], [email['To'],email['Cc']], email.as_string())

            return(True, 'Email sent successfully.')
        except Exception as e:
            return(False, 'Email could not be send. Reason: '+str(e))            
            
        
    def create_doctors_note_email(self, sender_email:str, receiver_email:str,  receiver_email_cc:str, sender_person:str, kid_name: str, course:str, from_date:str, to_date:str=None)->EmailMessage:
        # Define the sender and receiver email addresses
    
        # Create the email message
        message = EmailMessage()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['CC'] = receiver_email_cc

        
        
        #message =""
        if to_date==None:
            message['Subject'] = f"""{kid_name} krank, Klasse {course}, {from_date}"""
        
            message.set_content("Sehr geehrte Damen und Herren,\n\n"+
                                f"leider muss ich {kid_name}, Klasse {course}, "+
                                f"für den {from_date} krank melden.\n\n"+
                                "Mit freundlichen Grüssen\n"+
                                f"{sender_person}")
        
        else:
            message['Subject'] = f"""{kid_name} krank, Klasse {course}, {from_date}-{to_date}"""
        
            message.set_content("Sehr geehrte Damen und Herren,\n\n"+
                                f"leider muss ich {kid_name}, Klasse {course}, "+
                                f"vom {from_date} bis {to_date} krank melden.\n\n"+
                                "Mit freundlichen Grüssen\n"+
                                f"{sender_person}")

        return message
    
    def create_cancel_lunch_email(self, sender_email:str, receiver_email:str, sender_person:str, kid_name: str, course:str, from_date:str, to_date:str=None)->EmailMessage:
    
        # Create the email message
        message = EmailMessage()
        message['From'] = sender_email
        message['To'] = receiver_email
        
        #message =""
        if to_date==None:
            message['Subject'] = f"""Abbestellung Mittagessen fuer {kid_name}, Klasse {course}, {from_date}"""
        
        
            message.set_content("Sehr geehrte Damen und Herren,\n\n"+
                                f"ich möchte das Mittagessen für mein Kind {kid_name}, Klasse {course}, "+
                                f"für den {from_date} abbestellen.\n\n"+
                                "Mit freundlichen Grüssen\n"+
                                f"{sender_person}")
        
        else:
            message['Subject'] = f"""Abbestellung Mittagessen fuer {kid_name}, Klasse {course}, {from_date}-{to_date}"""
        
            message.set_content("Sehr geehrte Damen und Herren,\n\n"+
                                f"ich möchte das Mittagessen für mein Kind {kid_name}, Klasse {course}, "+
                                f"vom {from_date} bis {to_date} abbestellen.\n\n"+
                                "Mit freundlichen Grüssen\n"+
                                f"{sender_person}")
    
        return message

