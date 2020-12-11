import spacy
sp = spacy.load('en_core_web_sm')

inp_string = input("Text: ")
#sen = sp(u"I like to play football. I hated it in my childhood though")
lines = inp_string.split('.')
lines = [x for x in lines if len(x)!=0]

sen = sp(lines[0])
#print(sen.text)
#print(sen[7].pos_)
#print(sen[7].tag_)
#print(spacy.explain(sen[7].tag_))

for line in lines:
    sen = sp(line)
    for word in sen:
        print(f'{word.text:{12}} {word.pos_:{10}} {word.tag_:{8}} {spacy.explain(word.tag_)}')
