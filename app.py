import sqlite3
from flask import Flask, request, session, g, redirect, url_for
from flask import abort, render_template, flash, jsonify
import os


from importer import import_csv
from predictor.classifier_utils import transactionTypes
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

    return render_template("index.html", type_spending=type_spending, type_histograms=type_histograms)


@app.route("/list")
def list():

    transactions = query_db('SELECT * FROM transactions')

    stats = {
        "expenses": query_db('SELECT SUM(amount) as e FROM transactions WHERE amount < 0;')[0]['e'],
        "income": query_db('SELECT SUM(amount) as i FROM transactions WHERE amount > 0;')[0]['i']
    }

    return render_template("list.html", transactions=transactions, stats=stats)

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

            #try:
            import_csv(path, g.db)
            flash("CSV import successful.")

            return redirect(url_for("list"))
            #except Exception as e:
            #    flash("Error importing csv. %s" % e.strerror)
        else:
            flash("Error: File not found.")

    return render_template("upload.html")


@app.route("/api/stats/history/<int:etype>/<int:duration>/<int:length>")
def api_stats(etype, duration, length):
    return jsonify(stats.get_history_for_type(query_db, etype, length, duration))


if __name__ == '__main__':
    app.run(debug=True)