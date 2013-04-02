from predictor.classifier_utils import transactionTypes, get_month_id
from time import time
from datetime import datetime, date


def get_monthly_spending(db_query, num_months):

    """Return chart data for spenditure per spending type"""
    current_month_id = get_month_id(date.today())

    query = "SELECT SUM(amount) as y, type, monthid FROM transactions WHERE monthid BETWEEN ? AND ? GROUP BY type, monthid;"

    datasets = [{"data": []} for _ in range(num_months+1)]

    for row in db_query(query, [current_month_id - num_months, current_month_id]):
        datasets[current_month_id - int(row['monthid'])]['data'].append(
            {"x": transactionTypes[int(row['type'])], "y": row['y']})


    retval = {
        "xScale": "ordinal",
        "yScale": "exponential",
        "type": "bar",
        "main": datasets,
    }

    return retval

def get_history_for_type(db_query, type, num_time, time_len):
    now = long(time())
    breaking_point = now - time_len * num_time

    #Special case: 0 = all types
    if type == 0:
        query = "SELECT SUM(amount) as y, AVG(time) as atime FROM transactions WHERE time > ? GROUP BY time;"
        bindings = [breaking_point]
    else:
        query = "SELECT SUM(amount) as y, AVG(time) as atime FROM transactions WHERE time > ? AND type = ? GROUP BY time;"
        bindings = [breaking_point, type]
    
    data = []

    for i, point in enumerate(db_query(query, bindings)):

        x = datetime.fromtimestamp(point['atime']).strftime("%Y-%m-%d");

        data.append({"x": x, "y":point['y']})

    retval = {
        "xScale": "time",
        "yScale": "linear",
        "type": "line-dotted",
        "main": [
            {"data": data}
        ],
    }

    return retval


def get_detailed_history_all_types(db_query, num_time, time_len):
    out = []
    for i in range(1, 8):
        out.append(get_history_for_type(db_query, i, num_time, time_len))

    return out


def get_week_history_for_all_types(db_query, num_weeks):
    """Returns the graph data for each type ordered by week"""
    week = 3600l * 24 * 7
    now = long(time())
    todayWeekNumber = int(datetime.today().strftime("%W"))

    query = "SELECT SUM(amount) as y, type FROM transactions WHERE time BETWEEN ? AND ? GROUP BY type;"

    td = [[] for _ in range(10)]
    retval = []

    for i in range(num_weeks): 
        res = db_query(query, [now - week * (i+1), now - week * i])
        for tpair in res:
            td[int(tpair['type'])].insert(i, tpair['y'])

    
    for i, typ in enumerate(td):
        retval.append({
            "xScale": "ordinal",
            "yScale": "linear",
            "type": "line",
            "main": [
                {
                    "data": [{'x':str(todayWeekNumber - x + num_weeks), 'y':y} for x, y in enumerate(typ)],
                    "className": "type" + str(i)
                }
            ],
        })

    return retval


def some_cool_stats(db_query, begin, to):
    """Return some cool stats from the period between begin and to.
    begin and to are unix timestamps in seconds"""
    
    bindings = [begin, to]

    return {
        "total_takeout": db_query(
            "SELECT SUM(amount) as amt FROM transactions WHERE time BETWEEN ? AND ? AND type = 1", bindings, True)['amt'],
        "total_coffee": db_query(
            "SELECT SUM(amount) as amt FROM transactions WHERE time BETWEEN ? AND ? AND type = 3", bindings, True)['amt'],
        "total_income": db_query(
            "SELECT SUM(amount) as amt FROM transactions WHERE time BETWEEN ? AND ? AND amount > 0", bindings, True)['amt'],
        "total_expenses": db_query(
            "SELECT SUM(amount) as amt FROM transactions WHERE time BETWEEN ? AND ? AND amount < 0", bindings, True)['amt'],
        "avg_spending": db_query(
            "SELECT AVG(amount) as amt FROM transactions WHERE time BETWEEN ? AND ? AND amount < 0", bindings, True)['amt'],
    }

