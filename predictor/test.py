import unittest
from predictor import TransactionClassifier
from os.path import isfile
import os

class PredictorTest(unittest.TestCase):
    TEST_DATA = [{"tag":"BULLE", "amount":400}]
    TEST_TYPE = [4]
    TEST_PERS_FILE = "test.pkl"

    def setUp(self):
        self.clf = TransactionClassifier(self.TEST_PERS_FILE)
        self.clf._init_clf()

    def tearDown(self):
        if(isfile(self.TEST_PERS_FILE)):
            os.remove(self.TEST_PERS_FILE)
            for i in range(1,5):
                os.remove(self.TEST_PERS_FILE + "_0" + str(i) + ".npy")

    def test_fit(self):
        self.clf.fit(self.TEST_DATA, self.TEST_TYPE)

    def test_predict(self):
        self.test_fit()

        self.assertEquals(self.TEST_TYPE, self.clf.predict(self.TEST_DATA))

    def test_persist(self):
        self.test_fit()

        self.clf.persist()
        
        self.assertTrue(isfile(self.TEST_PERS_FILE))
