# !/usr/bin/env python3
"""
You need to download model for Russian language (a small one) from here
 https://alphacephei.com/vosk/models/vosk-model-small-ru-0.15.zip
 and unpack as 'model' in the current folder
 for vosk library to work.
"""

import argparse
import os
import queue
import sounddevice as sd
import vosk
import sys
import json
import logging
import _api_calls

logging.basicConfig(filename='voice_vosk.log', level=logging.DEBUG)


def determine_command(phrase):
    print()
    print("Вы сказали:", phrase)
    command_dict = {0: "получить курс биткоина",
                    1: "получить баланс",
                    2: "получить курс эфира",
                    3: "получить курс доллара",
                    4: "приветствие",
                    5: "запуск бота",
                    }

    bitcoin_words = {"бетховен", "битком", "коэн", "бид конкурс", "битка"}
    balance_words = {"остаток", "баланс", "сколько у меня денег", "сколько у меня в кошельке"}
    ethereum_words = {"эфир"}
    dollar_words = {"доллар"}
    hello_words = {"привет", "здравствуй", "начнем"}
    goodbye_words = {"делать деньги"}
    commands = [bitcoin_words, balance_words, ethereum_words, dollar_words,
                hello_words, goodbye_words]
    functions = [_api_calls.get_bitcoin, _api_calls.get_balance, _api_calls.get_ethereum,
                 _api_calls.get_dollar,  _api_calls.hello, _api_calls.bye]
    for count, command in enumerate(commands):
        for word in command:
            if word in phrase:
                print("Задача:", command_dict[count])
                print(functions[count]())
                break


q = queue.Queue()


def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))


parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    '-f', '--filename', type=str, metavar='FILENAME',
    help='audio file to store recording to')
parser.add_argument(
    '-m', '--model', type=str, metavar='MODEL_PATH',
    help='Path to the model')
parser.add_argument(
    '-d', '--device', type=int_or_str,
    help='input device (numeric ID or substring)')
parser.add_argument(
    '-r', '--samplerate', type=int, help='sampling rate')
args = parser.parse_args(remaining)

try:
    if args.model is None:
        args.model = "model"
    if not os.path.exists(args.model):
        print("Please download a model for your language from https://alphacephei.com/vosk/models")
        print("and unpack as 'model' in the current folder.")
        parser.exit(0)
    if args.samplerate is None:
        device_info = sd.query_devices(args.device, 'input')
        # soundfile expects an int, sounddevice provides a float:
        args.samplerate = int(device_info['default_samplerate'])

    model = vosk.Model(args.model)

    if args.filename:
        dump_fn = open(args.filename, "wb")
    else:
        dump_fn = None

    with sd.RawInputStream(samplerate=args.samplerate, blocksize=18000, device=args.device, dtype='int16',
                           channels=1, callback=callback):
        print('#' * 80)
        print('Press Ctrl+C to stop the recording')
        print('#' * 80)

        rec = vosk.KaldiRecognizer(model, args.samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                temp_rec = json.loads(rec.Result())
                determine_command(temp_rec['text'])

            if dump_fn is not None:
                dump_fn.write(data)

except KeyboardInterrupt:
    print('\nDone')
    parser.exit(0)
except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))
