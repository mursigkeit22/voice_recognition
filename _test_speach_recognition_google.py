"""
works slow cause of API calls; unpredictable.
"""


import speech_recognition as sr

print(sr.__version__)

r = sr.Recognizer()

# harvard = sr.AudioFile('harvard.wav')
# with harvard as source:
#     audio = r.record(source)
#
# # print(type(audio))
# # print(r.recognize_google(audio))
#
# jackhammer = sr.AudioFile('jackhammer.wav')
#
# with jackhammer as source:
#     r.adjust_for_ambient_noise(source, duration=0.5)
#     # The adjust_for_ambient_noise() method reads the first second of the file stream and calibrates the recognizer to the noise level of the audio.
#     # Hence, that portion of the stream is consumed before you call record() to capture the data.
#     # You can adjust the time-frame that adjust_for_ambient_noise() uses for analysis with the duration keyword argument.
#     # This argument takes a numerical value in seconds and is set to 1 by default.
#     audio1 = r.record(source, )
# print(r.recognize_google(audio1))


# print(r.recognize_google(audio1, show_all=True))
# When working with noisy files, it can be helpful to see the actual API response.
# Most APIs return a JSON string containing many possible transcriptions.
# The recognize_google() method will always return the most likely transcription unless you force it to give you the full response.
# You can do this by setting the show_all keyword argument of the recognize_google() method to True.


mic = sr.Microphone(device_index=0)
# print(sr.Microphone.list_microphone_names())

with mic as source:
    r.adjust_for_ambient_noise(source, duration=1)
    audio = r.listen(source)


print(r.recognize_google(audio, language="ru"))
# print(r.recognize_google_cloud(audio, language="ru"))