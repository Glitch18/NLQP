import spacy
import nltk
import regex as re
from nltk.tokenize import sent_tokenize
from spacy.matcher import Matcher

class TX_Processor:

    def __init__(self, in_text):
        nltk.download('punkt')
        #input text given to an instance of TXP:
        self.text = re.sub(r'([a-z]).([A-Z])',r'\1. \2',in_text)

        self.lines = sent_tokenize(self.text) #Sentence tokenize
        self.model = spacy.load('en_core_web_sm') #model for POS tagging
        self.matcher = Matcher(self.model.vocab)

    def print_lines(self):
        for line in self.lines:
            print(line)

    def pos_tag(self):
        for line in self.lines:
            sen = self.model(line)
            for word in sen:
                print(f'{word.text:{12}} {word.pos_:{10}} {word.tag_:{8}} {spacy.explain(word.tag_)}')

    def isActive(self,sentence):
        line = self.model(sentence)
        passive_rule = [{'DEP': 'nsubjpass'}, {'DEP': 'aux', 'OP': '*'},\
                        {'DEP': 'auxpass'}, {'TAG': 'VBN'}]
        self.matcher.add('Passive', None, passive_rule)
        matches = self.matcher(line)

        if matches:
            return 0
        else:
            return 1
