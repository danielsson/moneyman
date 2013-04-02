import sqlite3
from flask import Flask, request, session, g, redirect, url_for
from flask import abort, render_template, flash, jsonify
import os, time, datetime, string


from importer import import_csv
from predictor.classifier_utils import transactionTypes, get_month_id
import stats
import config

app = Flask(__name__)
app.config.from_object(config.DevConfig)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
           for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv

@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown(ex):
    g.db.close()


@app.template_filter('to_type_string')
def to_type_string(v):
    return transactionTypes[int(v)]


@app.route('/')
def index():

    type_spending = stats.get_monthly_spending(query_db, 3)

    type_histograms = stats.get_week_history_for_all_types(query_db, 10)

    cool_stats = stats.some_cool_stats(query_db, time.time() - 3600*24*31, time.time())

    return render_template("index.html", type_spending=type_spending, type_histograms=type_histograms, cool_stats=cool_stats)


@app.route("/list")
def list():

    transactions = query_db('SELECT * FROM transactions ORDER BY time DESC;')

    stats = {
        "expenses": query_db('SELECT SUM(amount) as e FROM transactions WHERE amount < 0;')[0]['e'],
        "income": query_db('SELECT SUM(amount) as i FROM transactions WHERE amount > 0;')[0]['i'],
        "balance": query_db('SELECT SUM(amount) as i FROM transactions;')[0]['i']
    }

    return render_template("list.html", transactions=transactions, stats=stats, types=transactionTypes)

@app.route("/details")
def details():
    return render_template('details.html', types=transactionTypes)

@app.route("/upload", methods=['GET', 'POST'])
def upload():


    if request.method == 'POST':
        file = request.files['file']
        if file:
            path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(path)

            try:
                import_csv(path, g.db)
                flash("CSV import successful.")

                return redirect(url_for("list"))
            except Exception as e:
                flash("Error importing csv. %s" % e.strerror)
        else:
            flash("Error: File not found.")

    return render_template("upload.html")


@app.route('/balance/adjust', methods=['POST'])
def adjust_balance():
    message = request.form['message']
    amount = int(request.form['amount'])

    if amount < 0:
        t = 7
    else:
        t = 6


    g.db.execute("INSERT INTO transactions (time, message, amount, type, monthid) VALUES (?,?,?,?,?);",
        [time.time(), message, amount, t, get_month_id(datetime.date.today())])

    g.db.commit()

    flash("Successfully adjusted balance")

    return redirect(url_for("list"))


@app.route('/type/adjust', methods=['POST'])
def adjust_type():
    tid = int(request.form['id'])
    t = int(request.form['type'])

    g.db.execute("UPDATE transactions SET type = ? WHERE id = ? LIMIT 1;",
        [t, tid])
    g.db.commit()

    flash("Successfully adjusted type")

    row = query_db("SELECT * FROM transactions WHERE id = ? LIMIT 1", [tid], True)
    with open('predictor/export.csv', 'a') as f:
        date = datetime.datetime.fromtimestamp(row['time']).strftime("%Y-%m-%d");
        f.write(string.join([date, row['message'].encode("ISO-8859-1", "replace"), str(row['amount']), str(row['type']) + "\n"], ','))


    return redirect(url_for("list"))

@app.route("/api/stats/history/<int:etype>/<int:duration>/<int:length>")
def api_stats(etype, duration, length):
    return jsonify(stats.get_history_for_type(query_db, etype, length, duration))

@app.route("/api/stats/cool/<int:begin>/<int:end>")
def api_cool(begin, end):
    return jsonify(stats.some_cool_stats(query_db, begin, end))


if __name__ == '__main__':
    app.run(debug=True)