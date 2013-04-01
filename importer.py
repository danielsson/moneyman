import csv, time, datetime
from predictor.predictor import TransactionClassifier

from predictor.classifier_utils import row_parser


def import_csv(path, db):
    """Import a csv file into the database"""

    clf = TransactionClassifier()

    with open(path, 'rb') as csvfile:
        reader = csv.reader(csvfile)
        reader.next() #Skip header

        for row in reader:
            try:
                trans = row_parser(row)

                prediction = clf.predict([trans])
            except:
                print "Failed to predict:"
                print trans
                continue

            timestamp = time.mktime(
                datetime.datetime.strptime(row[0], '%Y-%m-%d').timetuple())
            print [timestamp, trans['note'], trans['amount'], prediction[0]]
            db.execute(
                'INSERT INTO transactions (time, message, amount, type) ' +
                'VALUES (?,?,?,?);',
                [timestamp, unicode(trans['note'], "ISO-8859-1"), int(trans['amount']), int(prediction[0])])

            db.commit()

    print "Imported %s to the db" % path