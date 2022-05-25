with open('SemEval2016-overall.txt', 'r') as f, open('SemEval2016-multiple.txt', 'w+') as f1, open('SemEval2016-single.txt', 'w+') as f2:
    for line in f:
        word, score = line.split('\t')
        if len(word.split()) > 1:
            f1.write(word + '\t' + score)
        else:
            f2.write(word + '\t' + score)
            continue
