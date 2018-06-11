# from pandas_highcharts.display import display_charts
import pandas as pd
import sqlite3
# from highcharts import Highchart
from flask import Flask, session, redirect, url_for, escape, request, render_template, jsonify
import json


# chart = Highchart()

app = Flask(__name__)


def data():
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()
    results = []

    df = pd.DataFrame(columns=['coin', 'date', 'commits'])

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    results = cursor.fetchall()

    for i, coin in enumerate(results):
        # cursor.execute("SELECT 1000*timestamp, measure from measures")

        sql = "SELECT coinname, 1000*epochs, total from coins"

        # df = pd.read_sql_query(sql)
        # cursor.execute(("SELECT '%s', 1000*epochs, total from %s" % (coin ,coin)))
        # cursor.execute(("SELECT 'bitcoin', 1000*epochs, total from bitcoin"))
        cursor.execute(sql)

        results = cursor.fetchall()

        # df.append(pd.DataFrame.from_records(results[i], columns=['coin', 'date', 'commits']), ignore_index=True)

        # df = pd.read_sql_query("select coinname, 1000*epochs, total from  coins;" , conn)

        return results
        # return df

# return json.dumps({'coin1': results[0], 'coin2': results[1]})
# data1, data2 = data()


options = {

        'title': {
        'text': 'Crypto Github commits'
    },
    'subtitle': {
        'text': 'Repo popularity by commits index'
    },
    'xAxis': {
        'type': 'datetime',
        'title': {
            'enabled': True,
            'text': 'Week'
        },
        'labels': {
            'formatter': 'function () {\
                return this.value;\
            }'
        },
        'maxPadding': 0.05,
        'showLastLabel': True
    },
    'yAxis': {
        'title': {
            'text': 'Commits'
        },
        'labels': {
            'formatter': "function () {\
                return this.value + '°';\
            }"
        },
        'lineWidth': 2
    },
    'legend': {
        'enabled': False
    },
    'tooltip': {
        'headerFormat': '<b>{series.name}</b><br/>',
        'pointFormat': '{point.x} km: {point.y}°C'
    }
}

# chart.set_dict_options(options)
# chart.set_options('chart', {'inverted': False})
# chart.set_options('chart', {'resetZoomButton': {'relativeTo': 'plot', 'position': {'x': 0,'y': -30}}})
# chart.set_options('xAxis', {'events': {'afterBreaks': 'function(e){return}'}})
# chart.set_options('tooltip', {'formatter': 'default_tooltip'})
# chart.set_options('chart', {'style': {"fontSize": '22px'}})
# chart.set_options('chart', {'resetZoomButton': {'position': {'x': 10}}})
# chart.set_options('chart', {'resetZoomButton': {'relativeTo': 'chart'}})
# chart.set_options('xAxis', {'plotBands': {'color': '#FCFFC5', 'from': 2, 'to': 4}})
# chart.set_options('xAxis', {'plotBands': {'color': '#FCFFC5', 'from': 6, 'to': 8}})
# chart.set_options('xAxis', {'plotBands': {'color': '#FCFFC5', 'from': 10, 'to': 12}})

# chart.add_data_set(data1, series_type='line', name='Example Series')
# chart.add_data_set(data2, series_type='line', name='Example Series')

# chart.add_drilldown_data_set(data2, 'column', 'Chrome', name='Chrome')

# This will generate and save a .html file at the location you assign
# chart.save_file()


@app.route('/', methods=['POST', 'GET'])
def index1(chartid='chart_ID', chart_type='line', chart_height=640):

    res1 = data()

    labels = ['coin','date','total']

    df = pd.DataFrame.from_records(res1, columns=labels)
    pd.options.display.float_format = '{:,.0f}'.format

    coins = df['coin'].drop_duplicates().values.tolist()

    # init plist list of lists
    plist = [[] for i in range(len(coins))]
    json_data = [[] for i in range(len(coins))]

    # use unix time format
    # dates = df['date'].values.tolist()

    # dateint = df['date'].fillna(0).astype(int).values.tolist()
    # change date format to m-d-Y if needed
    # df['dates'] = pd.to_datetime(df['date'], unit='s')
    # dates = df['dates'].dt.strftime('%m-%d-%Y').tolist()

    # dates = pd.to_datetime(df['dates'].unique()).tolist()

    # change date to INT as highcharts expects

    df['date'] = df['date'].astype(int)

    totals = df['total'].values.tolist()

    for x, row in enumerate(coins):

        date1 = df[df['coin'].isin([row])]
        plist[x] = date1['total'].values.tolist()

        json_data[x] = date1[['date', 'total']].values.tolist()


        # plist.append(df[df['coin'].isin([row])].values.tolist())
    # try:
    #     for row in res1:
            # print pDict1
            # pList.append(str(row[0]))
            # plist[0].append(int(row[1]))
            # plist[1].append(int(row[2]))
    # except IndexError:
    #    return render_template("nochart.html")

    chart = {"renderTo": chartid, "type": chart_type, "height": chart_height}

    series = "[{name: '" + coins[0] + "' ,data: " + str(json_data[0]) + "},{name: '" + coins[
        1] + "' ,data: " + str(json_data[1]) + "} ]"

    title = "Github Commits"
    subtitle = "Source: Github API"
    xAxis = "Date (Weekly)"


    return render_template('chart2.html', chartID=chartid, series=series, title=title, xAxis=xAxis, yAxis="Commits", yAxis2="Commits",
                           chart=chart, subtitle=subtitle)

# display_charts(df, chart_type='stock')


if __name__ == '__main__':
    app.run()
