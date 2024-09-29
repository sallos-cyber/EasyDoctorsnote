from kivymd.uix.dialog.dialog import MDDialog, MDDialogHeadlineText, MDDialogButtonContainer
from kivy.uix.widget import Widget
from kivymd.uix.button import MDButton, MDButtonText
from typing import Callable, Optional

class DialogHandler:
    """
    A class to handle the display of dialogs in the application.

    Attributes:
    ----------
    dialog : Optional[MDDialog]
        The current dialog instance, if any.
    """
    def __init__(self)->None:
        self.dialog = None

    def show_dialog(self, text:str, close_callback:Callable[[], None]) -> None:
        """
           Show a dialog with the specified text and a callback for when it is closed.

           Parameters:
           ----------
           text : str
               The text to display in the dialog.
           close_callback : Callable[[], None]
               A callback function to be called when the dialog is closed.
           """
        if self.dialog is None:
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

    def close_dialog(self)->None:
        if self.dialog:
            self.dialog.dismiss()
            self.dialog = None  # Reset dialog reference


