from predictor.classifier_utils import transactionTypes, get_month_id
from time import time
from datetime import datetime, date

#This file defines several stats-generating functions for the app
#

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
    """Return the detailed transaction history for the specified
    type under the specified time frame. The data will have internal
    zero padding on non-activity dates due to limitations in the
    front end of the application. If the time frame spans a period
    longer than 70 days, data will be grouped by week."""

    now = long(time())
    breaking_point = now - time_len * num_time

    #Special case: 0 = all types
    if type == 0:
        query = "SELECT SUM(amount) as y, AVG(time) as atime FROM transactions WHERE time > ? GROUP BY %s ORDER BY atime ASC;"
        bindings = [breaking_point]
    else:
        query = "SELECT SUM(amount) as y, AVG(time) as atime FROM transactions WHERE time > ? AND type = ? GROUP BY %s ORDER BY atime ASC;"
        bindings = [breaking_point, type]

    if time_len * num_time < 3600*24*70:
        #If the period is less than two months, display daily
        query = query % "time"
    else:
        #else group by week
        query = query % "strftime('%W', time, 'unixepoch')"
    
    data = []
    lastdate = 0

    for i, point in enumerate(db_query(query, bindings)):

        #Because the graphing lib cant handle linear bar graphs
        #we have to insert zeros on days without transactions
        if i == 0:
            lastdate = point['atime']
        else:
            while lastdate < point['atime']:
                data.append({"x": lastdate, "y": 0})

                if time_len * num_time < 3600*24*70:
                    lastdate = lastdate + 3600 * 24
                else:
                    lastdate = lastdate + 3600*24*70

            if lastdate > point['atime']:
                lastdate = point['atime'] - 1


        data.append({"x": point['atime'], "y":point['y']})

    retval = {
        "xScale": "ordinal",
        "yScale": "linear",
        "type": "bar",
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
            "SELECT SUM(amount) as amt FROM transactions WHERE time BETWEEN ? AND ? AND type = 2", bindings, True)['amt'],
        "total_coffee": db_query(
            "SELECT SUM(amount) as amt FROM transactions WHERE time BETWEEN ? AND ? AND type = 4", bindings, True)['amt'],
        "total_income": db_query(
            "SELECT SUM(amount) as amt FROM transactions WHERE time BETWEEN ? AND ? AND amount > 0", bindings, True)['amt'],
        "total_expenses": db_query(
            "SELECT SUM(amount) as amt FROM transactions WHERE time BETWEEN ? AND ? AND amount < 0", bindings, True)['amt'],
        "avg_spending": db_query(
            "SELECT AVG(amount) as amt FROM transactions WHERE time BETWEEN ? AND ? AND amount < 0", bindings, True)['amt'],
    }


def get_sum_by_type(db_query, num_time, time_len):
    """Return the sum under the specified timeframe for each spending type. This method
    formats for the nvd3 lib"""
    bindings = [time() - num_time * time_len, time()]

    res = db_query("SELECT SUM(amount) as sum_, type FROM transactions WHERE time BETWEEN ? AND ? GROUP BY type;", bindings)

    values = []
    for row in res:
        values.append(
                {
                    "label": transactionTypes[int(row['type'])],
                    "value": abs(int(row['sum_']))
                })

    retval = [
        {
            "key": "Spending by type",
            "values": values
        },
    ]
    return retval

def get_histogram_old(db_query, num_time, time_len):
    """Return account balance history for the specified time frame.
    The balance history will be adjusted for the opening balance
    fot that timeframe"""

    bindings = [time() - num_time * time_len, time()]

    #This ensures that we begin at the correct number
    initial_value = db_query("SELECT SUM(amount) as S FROM transactions WHERE time < ?;", [bindings[0]], True)['S']

    if initial_value == None:
        initial_value = 0

    res = db_query("SELECT SUM(amount) as amount, time FROM transactions WHERE time BETWEEN ? AND ? GROUP BY time ORDER BY time ASC;", bindings)

    data = [{"x": bindings[0], "y": initial_value}]

    for i, row in enumerate(res):
        x = row['time'];
        y = int(row['amount'] + data[i]['y'])

        data.append({
            "x": x,
            "y": y
        })

    retval = {
        "xScale": "time",
        "yScale": "linear",
        "type": "line",
        "main": [
            {"data": data}
        ],
    }

    return retval

def get_histogram(db_query, type_, start, stop):
    """Return account balance history for the specified time frame.
    The balance history will be adjusted for the opening balance
    fot that timeframe"""

    bindings = [type_, start, stop]

    if(type_ == 0):
        #Special case: get all
        bindings = [start, stop]
        #This ensures that we begin at the correct number
        initial_value = db_query("SELECT SUM(amount) as S FROM transactions WHERE time < ?;", [bindings[0]], True)['S']

        res = db_query("SELECT SUM(amount) as amount, time FROM transactions WHERE time BETWEEN ? AND ? GROUP BY time ORDER BY time ASC;", bindings)

    else:
        bindings = [type_, start, stop]
        #This ensures that we begin at the correct number
        initial_value = db_query("SELECT SUM(amount) as S FROM transactions WHERE type = ? AND time < ?;", bindings[0:2], True)['S']

        res = db_query("SELECT SUM(amount) as amount, time FROM transactions WHERE type = ? AND time BETWEEN ? AND ? GROUP BY time ORDER BY time ASC;", bindings)

    if initial_value == None:
        initial_value = 0

    

    data = [{"x": start, "y": initial_value}]

    for i, row in enumerate(res):
        x = row['time'];
        y = int(row['amount'] + data[i]['y'])

        data.append({
            "x": x,
            "y": y
        })

    retval = {
        "xScale": "time",
        "yScale": "linear",
        "type": "line",
        "transactionType": type_,
        "main": [
            {"data": data}
        ],
    }

    return retval