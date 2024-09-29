from kivymd.uix.screen import MDScreen

class MainScreen(MDScreen):
    """
    Represents the main screen of the app.
    Lets you choose if you want to send a "cancel_lunch" and/or a
    "send_doctors_note" notification to school.
    """
    def __init__(self, view_model, **kwargs):
        super().__init__(**kwargs)
        self.view_model = view_model

