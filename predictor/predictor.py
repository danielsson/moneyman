from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_extraction import DictVectorizer
from sklearn.pipeline import Pipeline
from sklearn.externals import joblib
from os.path import isfile

class TransactionClassifier :
    
    PERSISTED_FILENAME = "/home/mattias/projects/moneyman/predictor/classifier.pkl"

    X = [ #Some test data
        {'tag': "BULLENS", 'amount': 40},
        {'tag': "BULLENS", 'amount': 30},
        {'tag': "IKEA", 'amount': 400}
    ]

    
    def __init__(self):
        if isfile(self.PERSISTED_FILENAME):
            self.classifier = joblib.load(self.PERSISTED_FILENAME)
        
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
        joblib.dump(self.classifier, self.PERSISTED_FILENAME)
