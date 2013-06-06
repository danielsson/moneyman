from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_extraction import DictVectorizer
from sklearn.pipeline import Pipeline
from sklearn.externals import joblib
from os.path import isfile

class TransactionClassifier :
    
    persisted_filename = "classifier.pkl"
    
    def __init__(self, persist_file):
        self.persisted_filename = persist_file

        if isfile(self.persisted_filename):
            self.classifier = joblib.load(self.persisted_filename)
        
        else:
            self._init_clf()


    def _init_clf(self):
        self.classifier = Pipeline([('vect', DictVectorizer()),
                    ('clf', KNeighborsClassifier())])


    def fit(self, X, target):
        """
        X Should be of the form:
        X = [
            {'tag': "BULLENS", 'amount': 39},
        {'tag': "BULLENS", 'amount': 30}
        {'tag': "IKEA", 'amount': 400}
        ]
        """

        return self.classifier.fit(X, target)

    def predict(self, target):
        return self.classifier.predict(target)


    def persist(self):
        joblib.dump(self.classifier, self.persisted_filename, 3)