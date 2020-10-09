from voice_assistant import VoiceAssistant
from voice_assistant_setup import VoiceAssistantSetup
from voice_assistant_actions import VoiceAssistantActions
from snowboy import snowboydecoder
import sys
import signal

interrupted = False

voice_assistant = VoiceAssistant()
voice_assistant_setup = VoiceAssistantSetup()
voice_assistant_actions = VoiceAssistantActions()
model_loc = 'snowboy/resources/out.pmdl'


def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted


def attend_user():
    voice_assistant.speak('What can I do for you, {}?'.format(voice_assistant.username))
    command = voice_assistant.listen()
    do = voice_assistant_actions.nlp(command)
    print(do)
    if getattr(voice_assistant_actions, do):
        getattr(voice_assistant_actions, do)()


def main():
    print('Welcome to Voice Assistant!')
    print(' Menu ')
    print('1. Setup')
    print('2. Access Assistant')
    print('Please enter your option:')
    opt = int(input())

    if opt == 1:
        print(' Setup Menu ')
        print('1. Set Username')
        print('2. Set Assistant Name')
        print('3. Set Hotword')
        print('Please enter your option:')
        num = int(input())
        if num == 1:
            voice_assistant.speak('Welcome')
            voice_assistant_setup.setup_username()
        elif num == 2:
            voice_assistant.speak('Welcome')
            voice_assistant_setup.setup_assistant_name()
        elif num == 3:
            voice_assistant.speak('Welcome')
            voice_assistant_setup.setup_hotword()
        main()

    elif opt == 2:
        if not voice_assistant.username or voice_assistant.assistant_name:
            voice_assistant.speak('Please set up voice assistant first')
        else:
            signal.signal(signal.SIGINT, signal_handler)
            detector = snowboydecoder.HotwordDetector(model_loc, sensitivity=0.5)
            print('Listening... Press Ctrl+C to exit')
            detector.start(detected_callback=attend_user(),
                           interrupt_check=interrupt_callback,
                           sleep_time=0.03)

            detector.terminate()


if __name__ == '__main__':
    main()















