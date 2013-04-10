import csv, datetime
from predictor import TransactionClassifier


#The supported transaction types. This is the canonical
#specification used in the classifier.
transactionTypes = {
    0: "All",
    1: "Income",
    2: "Takeout",
    3: "Groceries",
    4: "Coffee",
    5: "Housing",
    6: "Apparel etc.",
    7: "Transportation",
    8: "Entertainment",
    9: "Other"
}

def train_classifier_with_csv(csv_path, classifier_path):
    """Trains a TransactionClassifier using the data in the
    specified CSV file. The format of the file is: (below comma
    separates rows)
        YYYY-MM-DD, message, amount, type
    The csv might use other separators than comma. The type must be 
    one of the ones specified in transactionTypes. 
    classifier_path spcifies which .pkl file to use to persist the
    created classifier. Normally this is classifier.pkl in this dir."""

    X = []
    target = []

    with open(csv_path, 'rb') as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.read(1024))
        csvfile.seek(0)

        reader = csv.reader(csvfile, dialect)
        reader.next() #Skip header
        
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

        clf = TransactionClassifier(classifier_path)

        clf.fit(X, target)
        clf.persist()
    



def row_parser(row):
    """Returns a dict of values from a csv row. This dict must be used
    to interact with the classifier in order to get accurate results."""

    #Determine which string to use from row
    n_split = row[1].split()
    if n_split[0] == "Kortk\xc3\xb6p" and len(n_split) > 2:
        note = n_split[2].lower()
    else:
        note = n_split[0].lower()

    #Determine what weekday it was
    weekday = datetime.datetime.strptime(row[0], '%Y-%m-%d').date().weekday()
    
    #The amount is merely the third col
    amount = int(float(row[2]))


    return {'note': note, 'weekday': weekday, 'amount': amount}


def get_month_id(d):
    return d.year * 12 + d.month

if __name__ == '__main__':
    """Perform a training session using the export.csv file"""
    train_classifier_with_csv('export.csv', 'classifier.pkl')