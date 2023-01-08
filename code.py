import asyncio
import time

import adafruit_rtttl
import board
import neopixel
from adafruit_led_animation.animation.blink import Blink
from adafruit_led_animation.animation.chase import Chase
from adafruit_led_animation.animation.colorcycle import ColorCycle
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.customcolorchase import CustomColorChase
from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.animation.rainbow import Rainbow
from adafruit_led_animation.animation.rainbowchase import RainbowChase
from adafruit_led_animation.animation.rainbowcomet import RainbowComet
from adafruit_led_animation.animation.rainbowsparkle import RainbowSparkle
from adafruit_led_animation.animation.solid import Solid
from adafruit_led_animation.animation.sparkle import Sparkle
from adafruit_led_animation.animation.sparklepulse import SparklePulse
from adafruit_led_animation.color import AMBER, JADE, MAGENTA, ORANGE, PURPLE, WHITE
from adafruit_led_animation.sequence import AnimationSequence
from adafruit_macropad import MacroPad
from digitalio import DigitalInOut, Direction
from rainbowio import colorwheel


def play_snowman():
    # spkrenable = DigitalInOut(board.SPEAKER_ENABLE)
    # spkrenable.direction = Direction.OUTPUT
    # spkrenable.value = True
    macropad._speaker_enable.value = True
    adafruit_rtttl.play(
        board.SPEAKER,
        "Snowman:d=8,o=5,b=200:2g,4e.,f,4g,2c6,b,c6,4d6,4c6,4b,a,2g.,b,c6,4d6,4c6,4b,a,a,g,4c6,4e.,g,a,4g,4f,4e,4d,2c.,4c,4a,4a,4c6,4c6,4b,4a,4g,4e,4f,4a,4g,4f,2e.,4e,4d,4d,4g,4g,4b,4b,4d6,d6,b,4d6,4c6,4b,4a,4g,4p,2g",
    )
    macropad._speaker_enable.value = True


KEY_NUMBERS = 12

macropad = MacroPad()
last_macropad_encoder_value = macropad.encoder


def monitor_encoder_switch():
    macropad.encoder_switch_debounced.update()
    if macropad.encoder_switch_debounced.pressed:
        print("encoder pressed with value {}".format(macropad.encoder))
    if macropad.encoder_switch_debounced.released:
        print("encoder released with value {}".format(macropad.encoder))
    if last_macropad_encoder_value != macropad.encoder:
        print("encoder changed to value {}".format(macropad.encoder))
    return macropad.encoder


class KeysMonitor:
    def __init__(self):
        self.key_pressed = None


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


async def light_up_key_loop(keys_monitor):
    while True:
        if keys_monitor.key_pressed:
            print("light up key: {}".format(keys_monitor.key_pressed))
            light_up_key(keys_monitor.key_pressed)
            await asyncio.sleep(EVENT_DURATION)
            reset_lights()
        await asyncio.sleep(0)


async def animate_keys(keys_monitor):
    # pixels = neopixel.NeoPixel(board.NEOPIXEL, 12)
    pixels = macropad.pixels
    blink = Blink(pixels, speed=0.5, color=JADE)
    colorcycle = ColorCycle(pixels, speed=0.4, colors=[MAGENTA, ORANGE])
    comet = Comet(pixels, speed=0.01, color=PURPLE, tail_length=10, bounce=True)
    chase = Chase(pixels, speed=0.1, size=3, spacing=6, color=WHITE)
    pulse = Pulse(pixels, speed=0.1, period=3, color=AMBER)
    sparkle = Sparkle(pixels, speed=0.1, color=PURPLE, num_sparkles=10)
    solid = Solid(pixels, color=JADE)
    rainbow = Rainbow(pixels, speed=0.1, period=2)
    sparkle_pulse = SparklePulse(pixels, speed=0.1, period=3, color=JADE)
    rainbow_comet = RainbowComet(pixels, speed=0.1, tail_length=7, bounce=True)
    rainbow_chase = RainbowChase(pixels, speed=0.1, size=3, spacing=2, step=8)
    rainbow_sparkle = RainbowSparkle(pixels, speed=0.1, num_sparkles=15)
    custom_color_chase = CustomColorChase(
        pixels, speed=0.1, size=2, spacing=3, colors=[ORANGE, WHITE, JADE]
    )
    animations = AnimationSequence(
        comet,
        blink,
        rainbow_sparkle,
        chase,
        pulse,
        sparkle,
        rainbow,
        solid,
        rainbow_comet,
        sparkle_pulse,
        rainbow_chase,
        custom_color_chase,
        advance_interval=5,
        auto_clear=True,
    )
    while True:
        animations.animate()
        await asyncio.sleep(0)


def play_tune(key_number):
    audio_files = ["chorus_of_angels4.mp3"]
    # audio_files = ["slow.mp3", "happy.mp3", "beats.mp3", "upbeats.mp3"]
    key_index = key_number % len(audio_files)
    macropad.play_file("macropad_mp3/" + audio_files[key_index])
    # play_file("macropad_mp3/" + audio_files[key_index])


KEY_C = 130.8
KEY_D = 146.8
KEY_E = 164.8
KEY_F = 174.6
KEY_G = 196
KEY_A = 220
KEY_B = 246.9


async def play_tone(key_number):
    if key_number is 0:
        # play_snowman()
        # play_snowman()
        # play_snowman()
        pass
    else:
        key2tone = {
            1: KEY_C,
            2: KEY_D,
            3: KEY_E,
            4: KEY_F,
            5: KEY_G,
            6: KEY_A,
            7: KEY_B,
        }
        key_index = (key_number % 7) + 1
        macropad.start_tone(key2tone[key_index])
        await asyncio.sleep(EVENT_DURATION)
        macropad.stop_tone()


async def play_tone_loop(keys_monitor):
    while True:
        if keys_monitor.key_pressed is not None:
            print("play tone: {}".format(keys_monitor.key_pressed))
            await play_tone(keys_monitor.key_pressed)
        await asyncio.sleep(0)


async def keys_monitor_loop(keys_monitor):
    while True:
        key_event = macropad.keys.events.get()
        if key_event:
            if key_event.pressed:
                keys_monitor.key_pressed = key_event.key_number
                print("key pressed: {}".format(key_event))
            elif key_event.released:
                keys_monitor.key_pressed = None
                print("key released: {}".format(key_event))
        await asyncio.sleep(0)


async def main():
    keys_monitor = KeysMonitor()
    keys_monitor_task = asyncio.create_task(keys_monitor_loop(keys_monitor))
    # light_up_key_task = asyncio.create_task(light_up_key_loop(keys_monitor))
    play_tone_task = asyncio.create_task(play_tone_loop(keys_monitor))
    keys_animation = asyncio.create_task(animate_keys(keys_monitor))
    # play_tune_task = asyncio.create_task(play_tune(0))
    # await asyncio.gather(
    #     keys_monitor_task, play_tone_task, light_up_key_task, play_tune_task
    # )
    await asyncio.gather(keys_monitor_task, play_tone_task, keys_animation)


asyncio.run(main())

# light_up_key(1)
# time.sleep(2)

# while True:
#    key_event = macropad.keys.events.get()
#    if key_event:
#        if key_event.pressed:
#            print(key_event)
#            light_up_key(key_event.key_number)
#            make_sound(key_event.key_number)
#    else:
#        reset_lights()
#    macropad.encoder_switch_debounced.update()
#    if macropad.encoder_switch_debounced.pressed:
#        print("sending {}".format(macropad.Keycode.A))


# while True:
#    last_macropad_encoder_value = monitor_encoder_switch()
#    key_event = macropad.keys.events.get()
#
#    if key_event:
#        if key_event.pressed:
#            light_up_keys(key_event.key_number)
#            result = play_tune(key_event.key_number)
#    else:
#        reset_lights()


# To include more MP3 files, add the names to this list in the same manner as the others.
# Then, press the key associated with the file's position in the list to play the file!
# audio_files = ["slow.mp3", "happy.mp3", "beats.mp3", "upbeats.mp3"]
# if key_event.key_number < len(audio_files):
#     macropad.play_file("macropad_mp3/" + audio_files[key_event.key_number])

# import audiomp3
# import audiopwmio
# import board

# def play_file(file_path):
#     macropad.stop_tone()
#     macropad._speaker_enable.value = True
#     with audiopwmio.PWMAudioOut(board.SPEAKER) as audio:
#         mp3file = audiomp3.MP3Decoder(open(file_path, "rb"))
#         audio.play(mp3file)
#         # while audio.playing:
#         #     print("Playing...")
#     macropad._speaker_enable.value = False
