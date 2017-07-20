from Question import Question
import threading
import requests
import json
from Queue import Queue


class QuestionFactory(object):

    MINSIZE = 10
    REQSIZE = 10
    URL = 'https://opentdb.com/api.php'

    def __init__(self):
        super(QuestionFactory, self).__init__()
        self.buffer = Queue()
        self.lockBuffer = threading.Lock()
        self.lockRefill = threading.Lock()
        self.requestRefill()

    # get the queue size
    def size(self):
        with self.lockBuffer:
            return self.buffer.qsize()

    # add one or many questions
    def push(self, question):
        # list of questions
        if type(question) is list:
            with self.lockBuffer:
                for q in question:
                    self.buffer.put(q)
        else: # single question
            with self.lockBuffer:
                self.buffer.put(question)

    # get the next question
    def pop(self, wait=False):
        if self.size() > 0: # there are questions ready
            with self.lockBuffer:
                res = self.buffer.get()
            if self.size()<QuestionFactory.MINSIZE: # is the buffer close to empty ?
                self.requestRefill(False)
            return res
        else: # empty, let's refill
            self.requestRefill(wait)
            if wait :
                return self.pop(wait)
            else :
                return None

    # request a refill of question, can be blocking or non-blocking
    def requestRefill(self, wait=False):
        if wait:
            self.refill()
        else :
            worker = threading.Thread(target=self.refill)
            worker.start()

    # actuall blocking refill function
    def refill(self, extraArgs={}):
        # if we are not already refilling
        if self.lockRefill.acquire(False):
            payload = extraArgs.copy()
            payload["amount"] = str(QuestionFactory.REQSIZE)
            r = requests.post(QuestionFactory.URL, params=payload)
            jdata = json.loads(r.text)
            JsonQuestions = jdata["results"]
            questions = [Question(data) for data in JsonQuestions]
            self.push(questions)
            self.lockRefill.release()
        else : # if we are already refilling, just wait for the operation to be over
            self.waitCurrentRefill()

    def waitCurrentRefill(self):
        self.lockRefill.acquire()
        self.lockRefill.release()


if __name__ == '__main__':
    import time
    qf = QuestionFactory()
    q = qf.pop(True)
    print qf.size()
    # should be too fast for refill
    for i in range(5) :
        q = qf.pop(True)
    print qf.size()
    qf.refill()
    qf.requestRefill(True)
    print qf.size()
