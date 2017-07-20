import unittest
from Question import Question

class QuestionTestCase(unittest.TestCase):
    def setUp(self):
        self.q1 = Question()
        fakeM = '{"response_code":0,"results":[{"category":"Entertainment: Music","type":"multiple","difficulty":"medium","question":"Cryoshell, known for &quot;Creeping in My Soul&quot; did the advertising music for what Lego Theme?","correct_answer":"Bionicle","incorrect_answers":["Hero Factory","Ben 10 Alien Force","Star Wars"]}]}'
        self.q1.fromJson(fakeM)

        self.q2 = Question()
        fakeTF = '{"response_code":0,"results":[{"category":"General Knowledge","type":"boolean","difficulty":"easy","question":"The Lego Group was founded in 1932.","correct_answer":"True","incorrect_answers":["False"]}]}'
        self.q2.fromJson(fakeTF)

    def testTextQuestion(self):
        self.assertFalse(self.q1.checkAnswer("Star wars"), 'incorrect false existing text answer validation')
        self.assertFalse(self.q1.checkAnswer("sdhsgd"), 'incorrect false random text answer validation')
        self.assertFalse(self.q1.checkAnswer("6"), 'incorrect out of range answer validation')
        self.assertFalse(self.q1.checkAnswer(str(self.q1.randomOrder.index(self.q1.answer))), 'incorrect out of range answer validation')
        self.assertTrue(self.q1.checkAnswer(str(self.q1.randomOrder.index(self.q1.answer)+1)), 'incorrect good numerical answer non-validation')
        self.assertTrue(self.q1.checkAnswer("bianicl"), 'incorrect close enough answer non-validation')
        self.assertTrue(self.q1.checkAnswer("Bionicle"), 'incorrect perfect answer non-validation')

    def testTFQuestion(self):
        self.assertTrue(self.q2.checkAnswer("1"), 'incorrect good numerical answer non-validation')
        self.assertTrue(self.q2.checkAnswer("vrai"), 'incorrect good textual answer non-validation')
        self.assertFalse(self.q2.checkAnswer("dsfdf"), 'incorrect garbage answer validation')
        self.assertFalse(self.q2.checkAnswer("faux"), 'incorrect bad answer validation')

if __name__ == '__main__':
    unittest.main()
