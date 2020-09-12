import pyttsx3
import speech_recognition as sr
import pyjokes
import nltk
from nltk.corpus import wordnet
import spacy


class VoiceAssistant:
    def __init__(self):
        self.engine = pyttsx3.init('nsss')
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', self.voices[0].id)
        self.ner = spacy.load("en_core_web_sm")
        self.sim = spacy.load("en_core_web_lg")
        self.username = ""
        self.assistant_name = ""

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print('Say something...')
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source)
        try:
            command = r.recognize_google(audio).lower()
            print('You said: ' + command + '\n')
        except sr.UnknownValueError:
            print('....')
            command = self.listen()
        return command

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

    def tell_joke(self):
        joke = pyjokes.get_joke()
        self.speak(joke)
        print(joke)

    def nlp(self, query):
        text = nltk.word_tokenize(query.lower())
        tags = nltk.pos_tag(text)
        text_map = {}

        for (word, tag) in tags:
            if tag in text_map.keys():
                text_map[tag].append(word)
            else:
                text_map[tag] = [word]

        verbs = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
        potential_actions = []
        for verb in verbs:
            for key in text_map.keys():
                if verb == key:
                    actions = text_map[key]
                    for action in actions:
                        potential_actions.append(action)

        if not potential_actions:
            return 'No func found!'

        synonyms = []
        for action in potential_actions:
            for syn in wordnet.synsets(action):
                for word in syn.lemmas():
                    synonyms.append(word.name().lower())
        synonyms = set(synonyms)

        method_list = [func for func in dir(VoiceAssistant) if
                       callable(getattr(VoiceAssistant, func)) and not func.startswith("__")]

        do_list = []
        for syn in synonyms:
            if any(method.startswith(syn) for method in method_list):
                do_list.append(syn)

        potential_do = []
        for do in do_list:
            for method in method_list:
                if method.startswith(do):
                    potential_do.append(method)

        sim_arr = []
        for do in potential_do:
            max_sim = 0
            tokens = do.split('_')[1:]
            for token in tokens:
                token1 = self.sim(token)
                for key, value in text_map.items():
                    for val in value:
                        token2 = self.sim(val)
                        if token1.similarity(token2) > max_sim:
                            max_sim = token1.similarity(token2)
            sim_arr.append(max_sim)

        if max(sim_arr) < 0.75:
            return 'No func found!'
        else:
            return potential_do[sim_arr.index(max(sim_arr))]





