with open('svr_w.txt', 'r') as f, open('svr_w_silver.txt', 'w+') as g:
    # print line by line tab seperated
    idx = 0
    for line in f:
        g.write(line.strip().split('\t')[0] + '\n')
        idx += 1
        if idx % 5 == 0:
            g.write('\n')