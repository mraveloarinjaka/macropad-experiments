from rainbowio import colorwheel
from adafruit_macropad import MacroPad
import time
import asyncio

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
    flamingo_pink=16225950
    macropad_blue=48959
    dark_aquamarine=1015159
    dark_teal=286045
    midnight_blue=528699
    #color = colorwheel((255 / KEY_NUMBERS) * from_key)
    macropad.pixels.brightness = 1
    if from_key in [3,6,9]:
        macropad.pixels[from_key] = midnight_blue
    elif from_key in [2,5,8,11]:
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


def play_tune(key_number):
    audio_files = ["chorus_of_angels4.mp3"]
    # audio_files = ["slow.mp3", "happy.mp3", "beats.mp3", "upbeats.mp3"]
    key_index = key_number % len(audio_files)
    macropad.play_file("macropad_mp3/" + audio_files[key_index])
    # play_file("macropad_mp3/" + audio_files[key_index])


KEY_C=130.8
KEY_D=146.8
KEY_E=164.8
KEY_F=174.6
KEY_G=196
KEY_A=220
KEY_B=246.9


async def play_tone(key_number):
    key2tone = {1:KEY_C,
                2:KEY_D,
                3:KEY_E,
                4:KEY_F,
                5:KEY_G,
                6:KEY_A,
                7:KEY_B}
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
    light_up_key_task = asyncio.create_task(light_up_key_loop(keys_monitor))
    play_tone_task = asyncio.create_task(play_tone_loop(keys_monitor))
    play_tune_task = asyncio.create_task(play_tune(0))
    await asyncio.gather(keys_monitor_task, play_tone_task, light_up_key_task, play_tune_task)


asyncio.run(main())

#light_up_key(1)
#time.sleep(2)

#while True:
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
