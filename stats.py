from predictor.classifier_utils import transactionTypes, get_month_id
from time import time
from datetime import datetime, date

def get_type_total(db_query):
    """Return chart data for spenditure per spending type"""

    query = "SELECT SUM(amount) as y, type as x FROM transactions WHERE time BETWEEN ? AND ? GROUP BY type;"

    datasets = get_monthly(query, 4, db_query, [])

    retval = {
        "xScale": "ordinal",
        "yScale": "linear",
        "type": "bar",
        "main": datasets,
    }

    return retval

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

    query = "SELECT SUM(amount) as y, AVG(time) as atime FROM transactions WHERE time > ? AND type = ? GROUP BY time;"
    data = []

    for i, point in enumerate(db_query(query, [breaking_point, type])):

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

def get_recurring(
    query, time_len, num_time, db_query, params, yTrans = None, xTrans = None):
    now = long(time())

    if yTrans == None:
        def yTrans(e,i):
            return e['y']
    if xTrans == None:
        xTrans = lambda e,i: transactionTypes[int(e['x'])]

    datasets = []

    for i in range(num_time):
        datasets.append(
        {
            "data": [{"x": xTrans(e, i), "y": yTrans(e, i)}
                for e in db_query(query, params + [now - time_len * (i+1), now - time_len * i])
                if e['y'] != None]
        })
    if not len(datasets[-1]['data']):
        datasets.pop()

    return datasets

def get_monthly(query, num_months, db_query, params, yTrans = None, xTrans = None):
    month = 3600l * 24 * 10 #Lies!! TODO

    return get_recurring(query, month, num_months, db_query, params, yTrans, xTrans)

def get_weekly(query, num_weeks, db_query, params, yTrans = None, xTrans = None):
    week = 3600l * 24 * 7

    return get_recurring(query, week, num_weeks, db_query, params, yTrans, xTrans)



def some_cool_stats(db_query):
    now = long(time())
    breaking_point = now - 3600*24*31

    return {
        "total_takeout": db_query(
            "SELECT SUM(amount) as amt FROM transactions WHERE time > ? AND type = 1", [breaking_point], True)['amt'],
        "total_coffee": db_query(
            "SELECT SUM(amount) as amt FROM transactions WHERE time > ? AND type = 3", [breaking_point], True)['amt'],
        "total_income": db_query(
            "SELECT SUM(amount) as amt FROM transactions WHERE time > ? AND amount > 0", [breaking_point], True)['amt'],
        "total_expenses": db_query(
            "SELECT SUM(amount) as amt FROM transactions WHERE time > ? AND amount < 0", [breaking_point], True)['amt'],
        "avg_spending": db_query(
            "SELECT AVG(amount) as amt FROM transactions WHERE time > ? AND amount < 0", [breaking_point], True)['amt'],
    }

