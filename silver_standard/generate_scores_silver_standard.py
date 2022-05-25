import math
import re
from scipy.stats import kendalltau
from scipy.stats import spearmanr
import nltk

clueslen_dict = {}  # "word": [strength] where strength is either weaksubj or strongsubj
lemmatizer = nltk.WordNetLemmatizer()
emotion_lex = {}  # for each word, contains sentiment and its conveyed emotions (e.g. 'competent' -> 'positive'
# and 'trust')
polex = {}  # for each word, contains its effect ('positive', 'negative', 'shifter', 'intensifier'),
# its kind (A; actual, F; emotional, J; moral/judgmental) and its tag (noun, adjective, etc.)
#  example: 'powerful': {'effect': 'POS', 'kind': 'A', 'tag': 'adjektiv'}
# in the final version, kind is not used as it did not lead to any improvement



with open('lexicon/subjclueslen1-HLTEMNLP05.tff', 'r') as f:
    for line in f:
        line = line.split(' ')
        strength = line[0].split('=')[1]
        word = line[2].split('=')[1]
        clueslen_dict[word] = strength

    with open('lexicon/polex_en.pl', 'r') as f:
        # PREPARE LEXICONS

        for line in open('lexicon/NRC-emotion-lexicon.txt', 'r'):
            word, emotion, score = line.rstrip().split('\t')
            if word in emotion_lex:
                emotion_lex[word][emotion] = score
            else:
                emotion_lex[word] = {emotion: score}
        # pprint(emotion_lex)

        for line in f:
            line = re.sub(r'polex\((.+)\)', r'\1', line)
            line = line[:-2].split(',')
            if line != ['']:  # if line not empty
                word, kind, effect, tag = line[0].strip("\"'"), line[1].strip("\"'"), line[2].strip("\"'"), line[
                    3].strip(
                    "\"'")
                if word in polex:
                    polex[word] = (polex[word], {'kind': kind, 'effect': effect, 'tag': tag})
                else:
                    polex[str(word)] = ({'kind': kind, 'effect': effect, 'tag': tag})

        # pprint(polex)


def calculate_score(phrase_str='best example'):
    scores = []
    shifters = 0
    intensifiers = 0
    # PROCESS INPUT STRING
    phrase_str = phrase_str.replace('-', ' ').replace("'", ' ')  # remove hyphens and apostrophe for processing
    phrase_str = phrase_str.split(' ')  # split string into words
    pos = nltk.pos_tag(phrase_str)  # get the part of speech of each word

    pos_convert_dict = {'RB': 'adverb', 'RBR': 'adverb', 'RBS': 'adverb', 'JJ': 'adjective', 'JJR': 'adjective',
                        'JJS': 'adjective', 'NN': 'noun', 'NNS': 'noun', 'NNP': 'noun', 'NNPS': 'noun'}
    translations = {'nomen': 'noun', 'adjektiv': 'adjective'}
    pos_list = []
    all_words_and_emotions = {}  # contains all polex and their information from cluelsen and polex lexicon
    # e.g. string 'seriously great' ->
    # {'great': {'cluelsen': ['strongsubj', 'positive'], 'polex': ''},
    #  'seriously': {'cluelsen': ['strongsubj', 'negative'], 'polex': ''}}

    for word, pos in pos:
        emotion_dict = {"cluelsen": '', "polex": ''}  # for adding results if word exists in the dictionaries
        # only look at lemmas for generalized results
        if lemmatizer.lemmatize(word) in clueslen_dict:
            emotion_dict["cluelsen"] = clueslen_dict[lemmatizer.lemmatize(word)]
        if lemmatizer.lemmatize(word) in emotion_lex:
            emotion_dict["polex"] = emotion_lex[lemmatizer.lemmatize(word)]
        if pos in pos_convert_dict:
            pos_list.append(pos_convert_dict[pos])
        else:
            pos_list.append(pos)
        all_words_and_emotions[word] = emotion_dict

    negative_words = ['anger', 'disgust', 'fear', 'sadness', 'negative']
    positive_emotions = ['joy', 'surprise', 'anticipation', 'trust', 'positive']
    for word, pos in zip(phrase_str, pos_list):
        neg_count = 0
        pos_count = 0
        effect = ''
        if word in polex:
            # process polex information, get effect and count of negative and positive words
            # print(f'INFO WORD: {word}'.center(50, '-'))
            if type(polex[word]) == tuple:
                for dictionary_word in polex[word]:
                    if len(dictionary_word) == 2:  # if result is a tuple, e.g. when there is ambiguity
                        dictionary_word = dictionary_word[0]
                    if dictionary_word['tag'] in translations and len(dictionary_word) == 1:
                        pos_lex = translations[dictionary_word['tag']]  # get part of speech in english
                    else:
                        pos_lex = dictionary_word['tag']
                    if pos == pos_lex:  # if pos of word in input string matches pos of word in polex, get effect
                        effect = dictionary_word['effect']
            else:  # if result is a dictionary, when there is only one option
                effect = polex[word]['effect']

        # count positive and negative words based on NRC emotion lexicon
        if word in emotion_lex:
            # print(f'EMOTION WORD: {word}'.center(50, '-'))
            for neg in negative_words:
                if emotion_lex[word][neg] == '1':
                    neg_count += 1
            for pos in positive_emotions:
                if emotion_lex[word][pos] == '1':
                    pos_count += 1

        elif lemmatizer.lemmatize(word) in emotion_lex:  # if word is not found, try lemmatizing
            # print(f'EMOTION WORD: {word}'.center(50, '-'))
            word_lem = lemmatizer.lemmatize(word)
            for neg in negative_words:
                if emotion_lex[word_lem][neg] == '1':
                    neg_count += 1
            for pos in positive_emotions:
                if emotion_lex[word_lem][pos] == '1':
                    pos_count += 1

        # print(f'WORD: {word}\npositive wrds: {pos_count}\nnegative wrds: {neg_count}\n')

        calc_dict = {0: 0, 1: -0.9, 2: -1, 3: -1.4, 4: -1.5, 5: -1.7, 6: -1.8}
        score = 0
        if effect == 'NEG':
            neg_count += 1
        if effect == 'POS':
            pos_count += 1
        if neg_count:
            score = calc_dict[neg_count]
        if pos_count:
            score = (-calc_dict[pos_count] + score) / 2  # average positive and negative
        if effect == 'SHI':
            shifters += 1
        if effect == 'INT':
            intensifiers += 1

        if word in clueslen_dict:
            if 'strongsubj' in clueslen_dict[word]:  # if word is strong
                score = score * 3
        elif lemmatizer.lemmatize(word) in clueslen_dict:
            if 'strongsubj' in clueslen_dict[lemmatizer.lemmatize(word)]:  # if word not found, try lemmatizing
                score = score * 3
        scores.append(score)
    scores = [i for i in scores if i != 0]  # remove 0s from scores list
    if len(scores) == 0:
        scores = [0]  # if no scores, set score to 0
    score = sum(scores) / len(scores)
    if shifters > 0:  # if shifters exist, reduce intensity
        score = score / (shifters * 0.5 + 1)  # reduce intensity of score
    if intensifiers > 0:
        # intensify score
        score = score * (intensifiers * 0.5 + 1)

    mathscore = math.sinh(score) / math.cosh(score)  # to squish values for cleaner view
    # print('final', (mathscore))
    return mathscore


def calc(infilepath, outfilepath):
    with open(infilepath, 'r') as f, open(
            outfilepath, 'w+') as f2:
        lines = []
        idx = 0
        for line in f:
            line = line.split('\t')
            line[1] = float(line[1].strip())
            line.append(idx)
            idx += 1
            lines.append(line)

        # sort lines by descending score
        lines.sort(key=lambda x: x[1], reverse=True)

        original_idx = [x[-1] for x in lines]  # as input file was sorted, initial index was original
        pred_idx = list(range(0, len(lines)))  # as the list is sorted, it goes by descending score
        # calculate kendall tau

        # write sorted words and scores to file
        for line in lines:
            f2.write(line[0] + '\t' + str(line[1]) + '\n')

        tau, p_value = kendalltau(original_idx, pred_idx)
        spearman, p_value = spearmanr(original_idx, pred_idx)
        print(f'Kendall tau: {tau}, p-value: {p_value}')
        print(f'Spearman: {spearman}, p-value: {p_value}')


#with open('scl_nma/SCL-NMA.txt', 'r') as f1, open('scl_nma/SCL-NMA-single.txt', 'r') as f2, \
     #open('scl_nma/SCL-NMA-multiple.txt', 'r') as f3, open('predictions/predictions_overall.txt', 'w+') as o1, \
     #open('predictions/predictions_single.txt', 'w+') as o2, open('predictions/predictions_multiple.txt', 'w+') as o3:
with open('scl_nma/SemEval2016-overall.txt', 'r') as f1, open('predictions/predictions_overall.txt', 'w+') as o1, \
        open('scl_nma/SemEval2016-single.txt', 'r') as f2, open('predictions/predictions_single.txt', 'w+') as o2, \
        open('scl_nma/SemEval2016-multiple.txt', 'r') as f3, open('predictions/predictions_multiple.txt', 'w+') as o3:
    for line in f1:
        line = line.split('\t')
        o1.write(f'{line[0]}\t{calculate_score(line[0])}\n')
    for line in f2:
        line = line.split('\t')
        o2.write(f'{line[0]}\t{calculate_score(line[0])}\n')
    for line in f3:
        line = line.split('\t')
        o3.write(f'{line[0]}\t{calculate_score(line[0])}\n')

    print('OVERALL')
    calc(infilepath='predictions/predictions_overall.txt', outfilepath='predictions/predictions_overall_sorted.txt')

    print('\nSINGLE')
    calc(infilepath='predictions/predictions_single.txt', outfilepath='predictions/predictions_single_sorted.txt')

    print('\nMULTIPLE')
    calc(infilepath='predictions/predictions_multiple.txt', outfilepath='predictions/predictions_multiple_sorted.txt')


with open('np_extraction/nps_news_clean_300_examples.txt', 'r') as f, open('predictions_nps.txt', 'w+') as f2:
    lines = []
    # write sorted words and scores to file
    for line in f:
        score = calculate_score(line)
        lines.append((line, score))
    lines.sort(key=lambda x: x[1], reverse=True)
    for line in lines:
        f2.write(f'{line[0].rstrip()}\t{line[1]}\n')


