# def setup_hotword():
#     url = 'https://snowboy.kitt.ai/api/v1/train'
#     hotword = {
#                     "name": "a word",
#                     "language": "en",
#                     "age_group": "10_19",
#                     "gender": "F",
#                     "microphone": "mic type",
#                     "token": "<your auth token>",
#                     "voice_samples": [
#                         {wave: "<base64 encoded wave data>"},
#                         {wave: "<base64 encoded wave data>"},
#                         {wave: "<base64 encoded wave data>"}
#                     ]
#                 }
#
#     model = requests.post(url, data=hotword)


from voice_assistant import VoiceAssistant
import pyjokes


def main():
    voice_assistant = VoiceAssistant()

    print('Welcome to Voice Assistant!')
    print(' Menu    ')
    print('1. Setup')
    print('2. Access Assistant')
    opt = int(input())

    if opt == 1:
        voice_assistant.speak('Welcome')
        voice_assistant.setup_username()
        voice_assistant.setup_assistant_name()
    elif opt == 2:
        voice_assistant.speak('What can I do for you?')
        command = voice_assistant.listen()
        do = voice_assistant.nlp(command)
        print(do)
        if getattr(voice_assistant, do):
            getattr(voice_assistant, do)()

    main()


if __name__ == '__main__':
    main()















