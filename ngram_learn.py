# coding:utf-8
"""
Program: 语言模型的简单实现
Description: 简单实现一个N元的语言模型，其中N是可以进行设置的参数.
Author: Flyaway - flyaway1217@gmail.com
Date: 2014-01-16 19:23:29
Last modified: 2014-01-16 21:54:08
Python release: 3.2.3
"""

import math

class LM:
    def __init__(self, train_path, step=2, lam=1):

        # punctuations need to be removed
        self.punctuation = set(["，", "、", "。", "？", "“", "”", "！", "；", "‘", "’", "《", "》", "%"])
        self.step = step
        self.lam = lam
        self.words = []
        self.freq = {}

        # read the train data and remove the punctuation
        with open(train_path) as f:
            unique = set()
            for line in f:
                s = line.strip().split()
                # remove the punctuation
                s = [item.strip() for item in s if item not in self.punctuation]
                # gather the unique word
                for r in s:
                    unique.add(r)
                # add the start/end symbol
                s.insert(0, '<s>')
                s.append('</s>')
                self.words.append(s)
        self.size = len(unique)

    def getNgram(self, sentence):
        for e in range(1, len(sentence) - 1):
            if e > self.step:
                s = e - self.step + 1
            else:
                s = 0
            words = sentence[s:e + 1]
            words.insert(-1, '|')
            words = ','.join(words)
            words = words.replace(',|,', '|')
            yield words

    def train(self):
        for sentence in self.words:
            for words in self.getNgram(sentence):
                s = words.split('|')
                cond = s[0]
                w = s[1]
                if cond not in self.freq:
                    self.freq[cond] = {}
                    self.freq[cond][w] = 1
                else:
                    self.freq[cond][w] = self.freq[cond].get(w, 0) + 1

    def getProb(self, word, condition):
        cond = condition
        cond_num = 0
        w_num = 0
        if cond in self.freq:
            for key in self.freq[cond]:
                cond_num += self.freq[cond][key]
            w_num = self.freq[cond].get(word, 0)
        # smooth
        w_num = w_num + self.lam
        cond_num += (self.size * self.lam)
        return float(w_num / cond_num)

    def sentenceProb(self, sentence):
        mysentence = sentence.strip().split()
        mysentence.insert(0, '<s>')
        mysentence.append('</s>')
        result = 0
        for words in self.getNgram(mysentence):
            s = words.split('|')
            cond = s[0]
            w = s[1]
            result += math.log(self.getProb(w, cond), 2)
        return result


if __name__ == '__main__':
    inpath = './Data/train.in'

    print('Reading data...')
    lm = LM(inpath, 2)
    print('Start training...')
    lm.train()

    s1 = '我 在 北京 天安门'
    s2 = '在 我 北京 天安门'
    s3 = '北京 我 在 天安门'
    s4 = '北京 在 我 天安门'

    for s in [s1, s2, s3, s4]:
        print(s)
        print(lm.sentenceProb(s))