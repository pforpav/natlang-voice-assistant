import requests
import math
from voice_assistant import VoiceAssistant


class VoiceAssistantSetup(VoiceAssistant):
    def __init__(self):
        super(VoiceAssistant, self).__init__()
        self.snowboyurl = 'https://snowboy.kitt.ai/api/v1/train'

    def setup_username(self):
        self.speak('What should I call you?')
        username_map = self.ner(self.listen())
        if any(w.pos_ in ['PROPN', 'NOUN', 'ADJ'] for w in username_map):
            self.username = [w.text for w in username_map if w.pos_ in ['PROPN', 'NOUN', 'ADJ']]
            self.speak('Welcome, {}'.format(self.username[-1]))
            self.speak('Did I get that right?')
            check = self.listen()
            if any(word in check.split() for word in ['yes', 'yeah', 'ya', 'totally', 'sure']):
                self.speak('Great!')
            else:
                self.speak('Sorry, please type your name.')
                self.username = input()
                self.speak("Welcome, {}".format(self.username))
        else:
            self.speak('Sorry, I did not get that. Please type your name.')
            self.username = input()
            self.speak("Welcome, {}".format(self.username))

    def setup_assistant_name(self):
        self.speak("What would you like to call me?")
        assistant_name_map = self.ner(self.listen())
        if any(w.pos_ in ['PROPN', 'NOUN', 'ADJ'] for w in assistant_name_map):
            self.assistant_name = [w.text for w in assistant_name_map if w.pos_ in ['PROPN', 'NOUN', 'ADJ']]
            self.speak("Is my name {}?".format(self.assistant_name[-1]))
            check = self.listen()
            if any(word in check.split() for word in ['yes', 'yeah', 'ya', 'totally', 'sure']):
                self.speak('Great! I am henceforth called {}'.format(self.assistant_name[-1]))
            else:
                self.speak('Sorry, please type my name.')
                self.assistant_name = input()
                self.speak("I am henceforth called {}".format(self.assistant_name))
        else:
            self.speak('Sorry, I did not get that. Please type my name.')
            self.assistant_name = input()
            self.speak("I am henceforth called {}".format(self.assistant_name))

    def setup_hotword(self, gender, age):

        self.speak('Please speak your preferred hotword 3 times.')
        self.speak('1.')
        rec1 = self.listen()
        self.speak('2.')
        rec2 = self.listen()
        self.speak('3.')
        rec3 = self.listen()
        self.speak('Please enter your age:')
        age = int(input())
        self.speak('Please enter your gender (F/M):')
        gender = input()

        a = math.floor(age/10)
        age_range = ''.join([str(a), '0', '_', str(a), '9' ])

        hotword = {
                        "name": "va_call",
                        "language": "en",
                        "age_group": age_range,
                        "gender": gender,
                        "microphone": "macbook microphone",
                        "token": "25c6c1e4645e3b55e68134c5fbb20fc038c59a20",
                        "voice_samples": [
                            {"wave": rec1},
                            {"wave": rec2},
                            {"wave": rec3}
                        ]
                    }

        response = requests.post(self.snowboyurl, json=hotword)
        out = 'snowboy/resources/out.pmdl'
        if response.ok:
            with open(out, "w") as outfile:
                outfile.write(response.content)
            print("Saved model to {}.".format(out))
        else:
            print("Request failed.")
            print(response.text)
