import csv, datetime
from predictor import TransactionClassifier

def train_classifier_with_csv(path):
    X = []
    target = []

    with open(path, 'rb') as csvfile:
        reader = csv.reader(csvfile)
        reader.next() #Skip title
        for row in reader:
            try:
                X.append(row_parser(row))

                #We assume that row[3] is the target
                target.append(int(row[3]))
            except:
                print "Failed to parse row:"
                print row
                print "Continuing"

            #Clean up; len(X) and len(target) must equal
            if len(X) != len(target):
                X.pop()

        clf = TransactionClassifier()

        clf.fit(X, target)
        clf.persist()
    



def row_parser(row):
    """Returns a dict of values from a csv row"""

    #Determine which string to use from row
    n_split = row[1].split()
    if n_split[0] == "Kortk\xf6p" and len(n_split) > 2:
        note = n_split[2].lower()
    else:
        note = n_split[0].lower()

    #Determine what weekday it was
    weekday = datetime.datetime.strptime(row[0], '%Y-%m-%d').date().weekday()
    
    #The amount is merely the third col
    amount = int(float(row[2]))


    return {'note': note, 'weekday': weekday, 'amount': amount}


transactionTypes = {
    1: "Takeout",
    2: "Clothes etc.",
    3: "Coffee",
    4: "Apartment related",
    5: "Beer",
    6: "Deposit",
    7: "Other"
}


def get_month_id(d):
    return d.year * 12 + d.month

if __name__ == '__main__':
    train_classifier_with_csv('export.csv')