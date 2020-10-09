import pyjokes
import nltk
from nltk.corpus import wordnet
from voice_assistant import VoiceAssistant


class VoiceAssistantActions(VoiceAssistant):
    def __init__(self):
        super(VoiceAssistant, self).__init__()

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

        method_list = [func for func in dir(VoiceAssistantActions) if
                       callable(getattr(VoiceAssistantActions, func)) and not func.startswith("__")]

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

    def tell_joke(self):
        joke = pyjokes.get_joke()
        self.speak(joke)
        print(joke)