import random

# clean extracted noun phrases
hashes = []
with open('nps_spacy_news.txt', 'r') as f:
    with open('nps_news_clean.txt', 'w+') as f2:
        for line in f:
            if hash(line) not in hashes:
                hashes.append(hash(line))
                if len(line.split()) < 3 or '`' in line or 'Mrs.' in line or 'Mr.' in line:
                    continue
                else:
                    f2.write(line.strip() + '\n')
            else:
                continue


# get 200 random NPs from extracted bbc NPs
with open('nps_news_clean.txt', 'r') as infile, open('nps_news_clean_300_examples.txt', 'w') as outfile:
    vda = random.sample(infile.readlines(), 300)
    outfile.writelines(vda)
