import asyncio
from state import State

class Encoder:
    def __init__(self, macropad, state: State):
        self.macropad = macropad
        self.last_macropad_encoder_value = self.macropad.encoder
        self.state = state

    def monitor_encoder_switch(self):
        self.macropad.encoder_switch_debounced.update()
        if self.macropad.encoder_switch_debounced.pressed:
            self.state.toggle_encoder()
            # self.macropad.keyboard_layout.write("encoder switch pressed")
            print("encoder pressed with value {}".format(self.macropad.encoder))
        if self.macropad.encoder_switch_debounced.released:
            print("encoder released with value {}".format(self.macropad.encoder))
        if self.last_macropad_encoder_value != self.macropad.encoder:
            print("encoder changed to value {}".format(self.macropad.encoder))
        return self.macropad.encoder


async def monitor_encoder(macropad, state):
    encoder = Encoder(macropad, state)
    while True:
        encoder.last_macropad_encoder_value = encoder.monitor_encoder_switch()
        await asyncio.sleep(0)



