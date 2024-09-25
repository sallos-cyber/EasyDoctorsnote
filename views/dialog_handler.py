from kivymd.uix.dialog.dialog import MDDialog, MDDialogHeadlineText, MDDialogButtonContainer
from kivy.uix.widget import Widget
from kivymd.uix.button import MDButton, MDButtonText

class DialogHandler:
    def __init__(self):
        self.dialog = None

    def show_dialog(self, text, close_callback):
        if not self.dialog:
            self.dialog = MDDialog(
                    
                    MDDialogHeadlineText(
                        text=text,
                        halign="left",
                    ),
                    MDDialogButtonContainer(
                        Widget(),
                        MDButton(
                            MDButtonText(text="Ok"),
                            style="text",
                            on_release=lambda x: close_callback()
                        ),
                    ),
            )
        else:
            self.dialog.text = text
        self.dialog.open()

    def close_dialog(self):
        if self.dialog:
            self.dialog.dismiss()
            self.dialog = None  # Reset dialog reference


