import asyncio


async def monitor_keys(macropad, state):
    while True:
        key_event = macropad.keys.events.get()
        if key_event:
            if key_event.pressed:
                state.key_pressed = key_event.key_number
                print("key pressed: {}".format(key_event))
            elif key_event.released:
                state.key_pressed = None
                print("key released: {}".format(key_event))
        await asyncio.sleep(0)
