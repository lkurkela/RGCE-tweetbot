import markovify
import random
import re
import spacy
import sys


nlp = spacy.load("en")

class POSifiedText(markovify.Text):
    def word_split(self, sentence):
        return ["::".join((word.orth_, word.pos_)) for word in nlp(sentence)]

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence


with open(argv[1]) as f:
    text = f.read()

gen_state_size = random.randrange(1, 4)
text_model = markovify.Text(text)

for i in range(int(argv[2])):
    print(text_model.make_short_sentence(140))

