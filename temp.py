# from playsound import playsound
#
# # Input an existing wav filename
# wavFile = 'mesin-2.wav'
# # Play the wav file
# playsound(wavFile)

# from msvcrt import getch
# def read_keys():
#     while True:
#         key = getch()
#         if (key == b'\x00' or key == b'\xe0'):
#             key = getch()
#             print('Arrow key', ord(key))
#         else:
#             print("Else", ord(key))
# read_keys()

from playsound import playsound
playsound('crash.wav')