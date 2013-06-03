import stats
from flask import jsonify, Blueprint
from flask.ext.login import login_required
import database


api1 = Blueprint('api1', __name__)

@api1.route("/stats/history/<int:type_>/<int:start>/<int:stop>")
@login_required
def api_stats(type_, start, stop):
    return jsonify(stats.get_history_for_type(database.query_db, type_, start, stop))

@api1.route("/stats/cool/<int:begin>/<int:end>")
@login_required
def api_cool(begin, end):
    return jsonify(stats.some_cool_stats(database.query_db, begin, end))

@api1.route("/stats/spending_by_type/<int:duration>/<int:length>")
@login_required
def spending_by_type(duration, length):
    return jsonify(results = stats.get_sum_by_type(database.query_db, length, duration))

@api1.route("/stats/histogram/<int:type_>/<int:start>/<int:stop>")
@login_required
def histogram(type_, start, stop):
    return jsonify(stats.get_histogram(database.query_db, type_, start, stop))