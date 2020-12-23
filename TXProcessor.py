import spacy
import nltk
from nltk.tokenize import sent_tokenize

class TX_Processor:

    def __init__(self, in_text):
        nltk.download('punkt')
        self.text = in_text #input text given to an instance of TXP
        self.lines = sent_tokenize(self.text)
        self.sp_model = spacy.load('en_core_web_sm') #model for POS tagging

    def print_lines(self):
        print(self.lines)

    def pos_tag(self):
        for line in self.lines:
            sen = self.sp_model(line)
            for word in sen:
                print(f'{word.text:{12}} {word.pos_:{10}} {word.tag_:{8}} {spacy.explain(word.tag_)}')
