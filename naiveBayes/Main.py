class NaiveBayesModel:

    def __init__(self):
        file = open("training.txt")
        self.lens = [inst.strip().split("\t") for inst in file.readlines()]
        self.postingList = []
        self.classVec = []

    def createWordSet(self, dataSet):
        wordSet = set([])
        for data in dataSet:
            wordSet |= set(data)
        return list(wordSet)

    def setOfWordToVec(self, vocabList, inputSet):
        returnVec = zeros(len(vocabList))
        for index in range(0, len(vocabList)):
            word = vocabList[index]
            if word in inputSet:
                returnVec[index] = 1
        return returnVec

    def trainNaiveBayes(self, trainMaxtrix, trainCategory):
        numberOfPost = len(trainCategory)
        numberOfWords = len(trainCategory[0])
        positiveProbability = sum(trainCategory) / float(numberOfPost)
        positiveWordTotal = 0.0
        positiveWordAppearanceVec = zeros(numberOfWords)
        negativeWordTotal = 0.0
        negativeWordAppearanceVec = zeros(numberOfWords)

        for index in range(0, numberOfPost):
            if trainCategory[index] == 0:
                negativeWordAppearanceVec += trainMaxtrix[index]
                negativeWordTotal += sum(trainMaxtrix[index])
            else:
                positiveWordAppearanceVec += trainMaxtrix[index]
                positiveWordTotal += sum(trainMaxtrix[index])

        positiveProbabilityVec = positiveWordAppearanceVec/positiveWordTotal
        negativeProbabilityVec = negativeWordAppearanceVec/negativeWordTotal
        return positiveProbabilityVec, negativeProbabilityVec, positiveProbability

    def getCategory(self, inputSet):
        vacabularyList = self.createWordSet(self.postingList)
        inputWordVec = self.setOfWordToVec(vacabularyList, inputSet)
        dataMatrix = []
        for input in self.postingList:
            vec = self.setOfWordToVec(input)
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
        file = file = open(fileName)
        wordList = [inst.strip().split("\t") for inst in file.readlines()]
        return wordList

nbc = NaiveBayesModel()
nbc.getCategory(nbc.getFileWords("class.txt"))