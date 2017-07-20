import json
import random
import difflib


class Question(object):

    DIFFICULTIES = ["easy", "medium", "hard", "undefined"]
    TYPES = ["multiple", "boolean", "undefined"]

    def __init__(self, data=None):
        super(Question, self).__init__()
        self.category = "none"
        self.text = "none"
        self.answer = "none"
        self.difficulty = 3
        self.qtype = 2
        self.others = []
        self.randomOrder = []
        self.idAnswer = -1
        if data != None:
            self.fromJson(data)

    def setCategory(self, category):
        self.category = category

    def setText(self, text):
        self.text = text

    def setAnswer(self, answer):
        self.answer = answer

    def setOthers(self, others):
        self.others = list(others)

    def setDifficulty(self, difficulty):
        try :
            self.difficulty = Question.DIFFICULTIES.index(difficulty)
        except ValueError:
            print "value error: " + difficulty
            self.difficulty = 3

    def setQtype(self, qtype):
        try :
            self.qtype = Question.TYPES.index(qtype)
        except ValueError:
            self.qtype = 2

    # convenient string representation
    def __repr__(self):
        res = "cat: " + self.category
        res += "\ntype: " + Question.TYPES[self.qtype]
        res += "\ntext: " + self.text
        res += "\nanswer: " + self.answer
        res += "\nothers: " + str(self.others)
        res += "\ndifficulty: " + Question.DIFFICULTIES[self.difficulty]
        res += "\nrandom Order: " + str(self.randomOrder)
        return res

    # load from JSON data
    def fromJson(self, data):
        try:
            if type(data) == str:
                jdata = json.loads(data)
            else : # already a dict
                jdata = data
            self.setCategory(jdata["category"])
            self.setQtype(jdata["type"])
            self.setText(jdata["question"])
            self.setAnswer(jdata["correct_answer"])
            self.setOthers(jdata["incorrect_answers"])
            self.setDifficulty(jdata["difficulty"])
            self.shuffle()
        except Exception as e:
            print "JSON parsing error:", e
            print type(data)

    # create a random array of answers
    def shuffle(self):
        if self.qtype == 0:
            self.randomOrder = [self.answer] + self.others
            random.shuffle(self.randomOrder)
        else :
            self.randomOrder = ["True", "False"]

    # check textual answer
    def checkAnswerText(self, answer):
        answer = answer.lower()
        choices = [c.lower() for c in self.randomOrder]
        closeAns = difflib.get_close_matches(answer, choices, 1, 0.7)
        if len(closeAns) == 0:
            return False
        else :
            closeAns = closeAns[0]
            if closeAns == self.answer.lower():
                return True
            else :
                return False

    # check if numerical answer is the right one
    def checkAnswerWithNumber(self, n):
        if n>4 or n<1:
            return False
        if n-1 == self.randomOrder.index(self.answer):
            return True
        else :
            return False

    # check true/false answer
    def checkAnswerTF(self, answer):
        if answer.lower() in ("true", "vrai", "1"):
            answer = "true"
        elif answer.lower() in ("false", "faux", "2"):
            answer = "false"
        else :
            return False
        return answer == self.answer.lower()

    # global check, dispatch to the right function based on input and expected data
    def checkAnswer(self, answer):
        if self.qtype == 1:
            return self.checkAnswerTF(answer)
        else :
            if self.checkAnswerText(answer):
                return True
            else :
                try :
                    n = int(answer)
                    return self.checkAnswerWithNumber(n)
                except :
                    return False


if __name__ == '__main__':
    print "if you wish to test this class please refer to test.py"
