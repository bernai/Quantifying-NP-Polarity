import spacy
import glob

nlp = spacy.load("en_core_web_sm")

# read in sentences from txt files and get noun chunks
for filepath in glob.iglob('news/*.txt'):
    with open(filepath, 'r') as f, open('nps_spacy_news.txt', 'a+') as f2:
        for sent in f:
            doc = nlp(sent)
            for nc in doc.noun_chunks:
                f2.write(nc.text+'\n')
