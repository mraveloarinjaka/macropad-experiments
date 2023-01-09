import asyncio
import time

import animations
import board
import encoder
import keys
import sounds
from adafruit_macropad import MacroPad
from digitalio import DigitalInOut, Direction
from state import State
from rainbowio import colorwheel


KEY_NUMBERS = 12

macropad = MacroPad()


EVENT_DURATION = 1


def reset_lights():
    macropad.pixels.fill((0, 0, 0))


def light_up_keys(from_key):
    for i in range(KEY_NUMBERS):
        macropad.pixels.brightness = (KEY_NUMBERS - i) / KEY_NUMBERS
        key_index = (from_key + i) % KEY_NUMBERS
        macropad.pixels[key_index] = colorwheel(int(255 / KEY_NUMBERS) * key_index)
        time.sleep(0.1)


def light_up_key(from_key):
    flamingo_pink = 16225950
    macropad_blue = 48959
    dark_aquamarine = 1015159
    dark_teal = 286045
    midnight_blue = 528699
    # color = colorwheel((255 / KEY_NUMBERS) * from_key)
    macropad.pixels.brightness = 1
    if from_key in [3, 6, 9]:
        macropad.pixels[from_key] = midnight_blue
    elif from_key in [2, 5, 8, 11]:
        macropad.pixels[from_key] = macropad_blue
    elif from_key == 0:
        macropad.pixels[from_key] = flamingo_pink
    else:
        macropad.pixels[from_key] = dark_teal


async def light_up_key_loop(state):
    while True:
        if state.key_pressed:
            print("light up key: {}".format(state.key_pressed))
            light_up_key(state.key_pressed)
            await asyncio.sleep(EVENT_DURATION)
            reset_lights()
        await asyncio.sleep(0)


async def main():
    state = State()
    # state_task = asyncio.create_task(state_loop(state))
    # light_up_key_task = asyncio.create_task(light_up_key_loop(state))
    # play_tone_task = asyncio.create_task(play_tone_loop(state))
    # keys_animation = asyncio.create_task(animations.animate_keys(macropad.pixels))
    # play_tune_task = asyncio.create_task(play_tune(0))
    # await asyncio.gather(
    #     state_task, play_tone_task, light_up_key_task, play_tune_task
    # )
    await asyncio.gather(
        keys.monitor_keys(macropad, state),
        sounds.play_tone_loop(macropad, state),
        animations.animate_keys(macropad, state),
        encoder.monitor_encoder(macropad, state),
    )


asyncio.run(main())

