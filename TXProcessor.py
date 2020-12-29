import spacy
import nltk
import regex as re
from nltk.tokenize import sent_tokenize
from spacy.matcher import Matcher

class bcolors:
    #IGNORE THIS CLASS
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Sentence:
    def __init__(self,id):
        #TODO - who -> subject
        #WHERE -> place
        #WHEN -> time/date
        #Use nltk or something else to identify places and time
        self.subject = ""
        self.direct_obj = ""
        self.id = id
        self.indirect_obj = list()
        self.verbs = list()
        self.adjectives = list()
        self.adverbs = list()
        self.nouns = list()

    def set_subject(self,subj):
        self.subject += subj

    def set_object(self,obj):
        self.direct_obj += obj

    def add_nouns(self,nun):
        self.nouns.append(nun)

    def add_indirect_object(self,obj):
        if(not isinstance(obj,str)):
            raise NameError("Invaid Argument Type")
        self.indirect_obj.append(obj)

    def add_verb(self,verb):
        if(not isinstance(verb,str)):
            raise NameError("Invaid Argument Type")
        self.verbs.append(verb)

    def add_adj(self,adj):
        if(not isinstance(adj,str)):
            raise NameError("Invaid Argument Type")
        self.adjectives.append(adj)

    def add_adverb(self,obj):
        if(not isinstance(obj,str)):
            raise NameError("Invaid Argument Type")

        self.adverbs.append(obj)

    def show_details(self):
        #self.id = id
        #self.indirect_obj = list()
        #self.verbs = list()
        #self.adjectives = list()
        #self.adverbs = list()
        #self.nouns = list()
        print("From this line the following data was extracted: ")
        print(f"Main subject: {self.subject}")
        print(f"line id: {self.id}")
        print(f"indirect objects: {self.indirect_obj}")
        print(f"verbs: {self.verbs}")
        print(f"adjectives: {self.adjectives}")
        print(f"adverbs: {self.adverbs}")
        print(f"other nouns: {self.nouns}")
        print("\n")


class TX_Processor:
    def __init__(self, in_text):
        nltk.download('punkt')
        #input text given to an instance of TXP:
        #TODO - JSON files for storage | Cache database
        #TODO - A dict for storage
        self.text = re.sub(r'([a-z])\.([A-Z])',r'\1. \2',in_text)
        self.lines = sent_tokenize(self.text) #Sentence tokenize
        self.model = spacy.load('en_core_web_sm') #model for POS tagging
        self.matcher = Matcher(self.model.vocab)
        self.count = 0
        self.data = list()
        self.extract()

    def extract(self):
        for line in self.lines:
            print(f"{bcolors.OKGREEN}{bcolors.BOLD}{line}{bcolors.ENDC}")
            tags = self.pos_tag(line)
            entry = Sentence(self.count)
            self.count += 1
            for tag in tags:
                if(tag[1]=="PROPN"):
                    entry.set_subject(tag[0])
                elif(tag[1]=='VERB'):
                    entry.add_verb(tag[0])
                elif(tag[1]=="NOUN"):
                    entry.add_nouns(tag[0])
                elif(tag[1]=="ADV"):
                    entry.add_adverb(tag[0])
                elif(tag[1]=="ADJ"):
                    entry.add_adj(tag[0])
            entry.show_details()
            self.data.append(entry)


    def print_lines(self):
        for line in self.lines:
            print(line)

    def pos_tag(self,line):
        sen = self.model(line)
        tags = list()
        for word in sen:
            #print(f'{word.text:{12}} {word.pos_:{10}}')
            tags.append((word.text,word.pos_))
        return tags

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
