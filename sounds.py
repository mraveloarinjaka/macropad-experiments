import asyncio

import adafruit_rtttl
import board

# def play_tune(key_number):
#     audio_files = ["chorus_of_angels4.mp3"]
#     # audio_files = ["slow.mp3", "happy.mp3", "beats.mp3", "upbeats.mp3"]
#     key_index = key_number % len(audio_files)
#     macropad.play_file("macropad_mp3/" + audio_files[key_index])
#     # play_file("macropad_mp3/" + audio_files[key_index])


def play_snowman(macropad):
    # spkrenable = DigitalInOut(board.SPEAKER_ENABLE)
    # spkrenable.direction = Direction.OUTPUT
    # spkrenable.value = True
    macropad._speaker_enable.value = True
    adafruit_rtttl.play(
        board.SPEAKER,
        "Snowman:d=8,o=5,b=200:2g,4e.,f,4g,2c6,b,c6,4d6,4c6,4b,a,2g.,b,c6,4d6,4c6,4b,a,a,g,4c6,4e.,g,a,4g,4f,4e,4d,2c.,4c,4a,4a,4c6,4c6,4b,4a,4g,4e,4f,4a,4g,4f,2e.,4e,4d,4d,4g,4g,4b,4b,4d6,d6,b,4d6,4c6,4b,4a,4g,4p,2g",
    )
    macropad._speaker_enable.value = True


EVENT_DURATION = 1


KEY_C = 130.8
KEY_D = 146.8
KEY_E = 164.8
KEY_F = 174.6
KEY_G = 196
KEY_A = 220
KEY_B = 246.9


async def play_tone(macropad, key_number):
    if key_number is 0:
        # play_snowman(macropad)
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


async def play_tone_loop(macropad, state):
    while True:
        if state.key_pressed is not None:
            print("play tone: {}".format(state.key_pressed))
            await play_tone(macropad, state.key_pressed)
        await asyncio.sleep(0)
