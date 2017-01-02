# -*- coding: UTF-8 -*-
from numpy import *

class NaiveBayesModel:

    def __init__(self):
        # file = open("training.txt")
        # self.lens = [inst.strip().split("\t") for inst in file.readlines()]
        self.postingList = \
            [
                ['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']
            ]
        self.classVec = [0, 1, 0, 1, 0, 1]

    def createWordSet(self, dataSet):
        wordSet = set([])
        for data in dataSet:
            wordSet |= set(data)

        print 'list word set:', list(wordSet)
        return list(wordSet)

    def setOfWordToVec(self, vocabList, inputList):
        returnVec = zeros(len(vocabList))
        for index in range(0, len(vocabList)):
            word = vocabList[index]
            if word in inputList:
                returnVec[index] = 1
        return returnVec

    def trainNaiveBayes(self, trainMaxtrix, trainCategory):
        numberOfPost = len(trainMaxtrix)
        numberOfWords = len(trainMaxtrix[0])
        positiveProbability = sum(trainCategory) / float(numberOfPost)
        positiveWordTotal = 2.0
        # positiveWordAppearanceVec = zeros(numberOfWords)
        ## Laplace smoothing
        positiveWordAppearanceVec = ones(numberOfWords)
        negativeWordTotal = 2.0
        #negativeWordAppearanceVec = zeros(numberOfWords)
        ## Laplace smoothing
        negativeWordAppearanceVec = ones(numberOfWords)

        for index in range(0, numberOfPost):
            if trainCategory[index] == 0:
                negativeWordAppearanceVec += trainMaxtrix[index]
                negativeWordTotal += sum(trainMaxtrix[index])
            else:
                positiveWordAppearanceVec += trainMaxtrix[index]
                positiveWordTotal += sum(trainMaxtrix[index])

        positiveProbabilityVec = positiveWordAppearanceVec/positiveWordTotal
        negativeProbabilityVec = negativeWordAppearanceVec/negativeWordTotal
        print positiveProbabilityVec, negativeProbabilityVec, positiveProbability
        return positiveProbabilityVec, negativeProbabilityVec, positiveProbability

    def getCategory(self, inputList):
        vacabularyList = self.createWordSet(self.postingList)
        inputWordVec = self.setOfWordToVec(vacabularyList, inputList)
        dataMatrix = []
        for input in self.postingList:
            vec = self.setOfWordToVec(vacabularyList, input)
            dataMatrix.append(vec)
        positiveProbabilityVec, negativeProbabilityVec, probabilityAbuse = self.trainNaiveBayes(dataMatrix, self.classVec)

        positiveProbability = probabilityAbuse
        negativeProbability = 1 - probabilityAbuse
        for index in range(0, len(inputWordVec)):
            item = inputWordVec[index]
            if item == 1:
                positiveProbability *= positiveProbabilityVec[index]
            else:
                negativeProbability *= negativeProbabilityVec[index]
        print positiveProbability, negativeProbability
        if positiveProbability > negativeProbability:
            return 1
        elif positiveProbability == negativeProbability:
            return 0
        else:
            return -1

    def getFileWords(self, fileName):
        file = open(fileName)
        wordList = [inst.strip().split("\t") for inst in file.readlines()]
        return wordList[0]

nbc = NaiveBayesModel()
nbc.getCategory(nbc.getFileWords("classify.txt"))