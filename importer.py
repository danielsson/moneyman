import csv, time, datetime
from predictor.predictor import TransactionClassifier

from predictor.classifier_utils import row_parser, get_month_id


def import_csv(path, db):
    """Import a csv file into the database, using the predictor
        to select type."""

    clf = TransactionClassifier()

    with open(path, 'rb') as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.read(1024))
        csvfile.seek(0)

        reader = csv.reader(csvfile, dialect)
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

            the_date = datetime.date.fromtimestamp(timestamp)

            monthid = get_month_id(the_date)

            db.execute(
                'INSERT INTO transactions (time, message, amount, type, monthid) ' +
                'VALUES (?,?,?,?,?);',
                [timestamp, unicode(row[1], "ISO-8859-1"), int(trans['amount']), int(prediction[0]), monthid])

            db.commit()

    print "Imported %s to the db" % path


