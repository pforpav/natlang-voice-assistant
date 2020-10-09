import pyttsx3
import speech_recognition as sr
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








