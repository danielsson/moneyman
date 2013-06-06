import csv, time, datetime
from os import path
from predictor.predictor import TransactionClassifier

from predictor.classifier_utils import row_parser, get_month_id


def import_csv(csv_path, classifier_path, user_id, db):
    """Import a csv file into the database, using the predictor
        to select type."""

    if not path.isfile(classifier_path):
        raise ValueError("Not a file: " + classifier_path)


    clf = TransactionClassifier(classifier_path)


    with open(csv_path, 'rb') as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.read(1024))
        csvfile.seek(0)

        reader = csv.reader(csvfile, dialect)
        reader.next() #Skip header
        try:
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

                the_date = datetime.date.fromtimestamp(timestamp)

                monthid = get_month_id(the_date)

                db.execute(
                    'INSERT INTO transactions (time, message, amount, type, monthid, uid) ' +
                    'VALUES (?,?,?,?,?,?);',
                    [timestamp, unicode(row[1], "UTF-8"), int(trans['amount']), int(prediction[0]), monthid, user_id])
        except:
            #If there was an error, undo changes
            db.rollback()
            raise
            
        db.commit()

    print "Imported %s to the db" % csv_path


