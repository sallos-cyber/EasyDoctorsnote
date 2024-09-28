# -*- coding: utf-8 -*-

from kivy.logger import Logger
from email.message import EmailMessage    
from datetime import datetime
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
            
        
    def create_doctors_note_email(self, language:str, sender_email:str, receiver_email:str,  receiver_email_cc:str, sender_person:str, kid_name: str, course:str, from_date:str, to_date:str=None)->EmailMessage:
        # Define the sender and receiver email addresses
    
        # Create the email message
        message = EmailMessage()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['CC'] = receiver_email_cc

        
        if language=="German":        
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
    
        if language=="English":        
            
            # Parse the original date string
            from_date = datetime.strptime(from_date, "%d.%m.%Y")
            # Format the date object to the new format
            from_date = from_date.strftime("%m.%d.%Y")
            if to_date==None:
                message['Subject'] = f"""{kid_name} is ill, Grade {course}, {from_date}"""
                message.set_content("Dear Sir or Madam,\n\n" +
                        f"I am writing to inform you that {kid_name}, Grade {course}, " +
                        f"will be unable to attend school on {from_date} due to illness.\n\n" +
                        "Best regards,\n" +
                        f"{sender_person}")
                message.set_content 
                            
            else:
                # Parse the original date string
                to_date = datetime.strptime(to_date, "%d.%m.%Y")
                # Format the date object to the new format
                to_date = to_date.strftime("%m.%d.%Y")

                message['Subject'] = f"""{kid_name} is ill, Grade {course}, {from_date}-{to_date}"""
                message.set_content("Dear Sir or Madam,\n\n" +
                    f"I am writing to inform you that {kid_name}, Grade {course}, " +
                    f"will be unable to attend school from {from_date} to {to_date} due to illness.\n\n" +
                    "Best regards,\n" +
                    f"{sender_person}")
        return message
    
    def create_cancel_lunch_email(self, language:str,  sender_email:str, receiver_email:str, sender_person:str, kid_name: str, course:str, from_date:str, to_date:str=None)->EmailMessage:
    
        # Create the email message
        message = EmailMessage()
        message['From'] = sender_email
        message['To'] = receiver_email
        
        if language=="German":
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
        
        if language=="English":
            if to_date==None:

                message['Subject'] = f"""Cancellation of School Lunch for {kid_name}, Grade {course}, {from_date}"""

                message.set_content("Dear Sir or Madam,\n\n"+
                    f"I would like to cancel the school lunch for {kid_name}, Grade {course}, "+
                    f"on {from_date}.\n\n"+
                    "Kind regards,\n"+
                    f"{sender_person}")
                            
            else:
                message['Subject'] = f"""Cancellation of School Lunch for {kid_name}, Grade {course}, {from_date} - {to_date}"""

                message.set_content("Dear Sir or Madam,\n\n"+
                    f"I would like to cancel the school lunch for {kid_name}, Grade {course}, "+
                    f"from {from_date} to {to_date}.\n\n"+
                    "Kind regards,\n"+
                    f"{sender_person}")

        return message

