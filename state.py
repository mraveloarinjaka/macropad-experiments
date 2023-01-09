class State:
    def __init__(self):
        self.key_pressed = None
        self.encoder_toggled = False

    def toggle_encoder(self):
        self.encoder_toggled = not self.encoder_toggled
