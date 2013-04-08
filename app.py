import sqlite3
from flask import Flask, request, session, g, redirect, url_for
from flask import abort, render_template, flash, jsonify
from flask.ext.login import (LoginManager, current_user, login_required,
                            login_user, logout_user, UserMixin, AnonymousUser,
                            confirm_login, fresh_login_required)

import os, time, datetime, string


from importer import import_csv
from predictor.classifier_utils import transactionTypes, get_month_id
import stats
import config

app = Flask(__name__)
app.config.from_object(config.DevConfig)

login_manager = LoginManager()
login_manager.login_view = "login"

class User(UserMixin):
    def __init__(self, name, id, active=True):
        self.name = name
        self.id = unicode(id)
        self.active = active

    def is_active(self):
        return self.active

    @staticmethod
    def byId(id):
        res = query_db("SELECT * FROM users WHERE id=? LIMIT 1;", [id], True)

        if res == None:
            return None

        return User(res['username'], res['id'])

    @staticmethod
    def byLogin(username, password):
        res = query_db("SELECT * FROM users WHERE username=? AND password=? LIMIT 1;", [username, password], True)

        if res == None:
            return None

        return User(res['username'], res['id'])



    def get_id(self):
        return self.id;

@login_manager.user_loader
def load_user(i):
    return User.byId(i)
    
login_manager.init_app(app)



def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def query_db(query, args=(), one=False):
    if not hasattr(g, "db"):
        g.db = connect_db()

    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
           for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv

@app.before_request
def before_request():
    if not hasattr(g, "db"):
        g.db = connect_db()


@app.teardown_request
def teardown(ex):
    g.db.close()


@app.template_filter('to_type_string')
def to_type_string(v):
    return transactionTypes[int(v)]

@app.template_filter('to_str_date')
def to_str_date(v):
    return datetime.datetime.fromtimestamp(int(v)).strftime("%Y-%m-%d");


@app.route('/')
@login_required
def index():

    type_spending = stats.get_monthly_spending(query_db, 3)

    type_histograms = stats.get_week_history_for_all_types(query_db, 10)

    cool_stats = stats.some_cool_stats(query_db, time.time() - 3600*24*31, time.time())

    return render_template("index.html", type_spending=type_spending, type_histograms=type_histograms, cool_stats=cool_stats)


@app.route("/list")
@login_required
def list():

    transactions = query_db('SELECT * FROM transactions ORDER BY time DESC;')

    stats = {
        "expenses": query_db('SELECT SUM(amount) as e FROM transactions WHERE amount < 0 AND uid = ?;',[current_user.id],True)['e'],
        "income": query_db('SELECT SUM(amount) as i FROM transactions WHERE amount > 0 AND uid = ?;',[current_user.id],True)['i'],
        "balance": query_db('SELECT SUM(amount) as i FROM transactions WHERE uid = ?;',[current_user.id],True)['i']
    }

    return render_template("list.html", transactions=transactions, stats=stats, types=transactionTypes)

@app.route("/details")
@login_required
def details():
    return render_template('details.html', types=transactionTypes)

@app.route("/histogram")
@login_required
def view_histogram():
    return render_template('histogram.html')

@app.route("/pies")
@login_required
def pies():
    return render_template('pies.html', types=transactionTypes)

@app.route("/upload", methods=['GET', 'POST'])
@login_required
def upload():

    if request.method == 'POST':
        file = request.files['file']
        if file:
            path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(path)

            try:
                import_csv(path, "predictor/classifier.pkl", current_user.id, g.db)
                flash("CSV import successful.")

                return redirect(url_for("list"))
            except Exception as e:
                flash("Error importing csv. %s" % e)
        else:
            flash("Error: File not found.")

    return render_template("upload.html")


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = User.byLogin(request.form['username'], request.form['password'])
        if user != None:
            login_user(user)
            flash('Login successful.')

            return redirect(request.args.get("next") or url_for("index"))
        else:
            flash("Unknown credentials")

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))



@app.route('/balance/adjust', methods=['POST'])
@login_required
def adjust_balance():
    message = request.form['message']
    amount = int(request.form['amount'])

    if amount < 0:
        t = 7 
    else:
        t = 6


    g.db.execute("INSERT INTO transactions (time, message, amount, type, monthid, ) VALUES (?,?,?,?,?);",
        [time.time(), message, amount, t, get_month_id(datetime.date.today())])

    g.db.commit()

    flash("Successfully adjusted balance")

    return redirect(url_for("list"))


@app.route('/type/adjust', methods=['POST'])
@login_required
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
@login_required
def api_stats(etype, duration, length):
    return jsonify(stats.get_history_for_type(query_db, etype, length, duration))

@app.route("/api/stats/cool/<int:begin>/<int:end>")
@login_required
def api_cool(begin, end):
    return jsonify(stats.some_cool_stats(query_db, begin, end))

@app.route("/api/stats/spending_by_type/<int:duration>/<int:length>")
@login_required
def spending_by_type(duration, length):
    return jsonify(results = stats.get_sum_by_type(query_db, length, duration))

@app.route("/api/stats/histogram/<int:duration>/<int:length>")
@login_required
def histogram(duration, length):
    return jsonify(stats.get_histogram(query_db, length, duration))


if __name__ == '__main__':
    app.run(debug=True)