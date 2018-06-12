import pandas as pd
import sqlite3
import json
import datetime
import requests

import configparser

Config = configparser.ConfigParser()


def setup_config():
    Config.read("config.ini")
    try:
        cfgfile = open("config.ini", 'r')
    except Exception as e:
        logger.info("Error: {}".format(e))
        logger.info("Creating config file")
        cfgfile = open("config.ini", 'w')
        Config.add_section('config')
        Config.set('config', 'ACCESS_TOKEN', "")

        Config.write(cfgfile)
        cfgfile.close()
        Config.read("config.ini")


def getdata(coinname, githuburl):

    setup_config()

    token = Config.get("config", "ACCESS_TOKEN")

    if token == "":
        return False

    headers = {'Authorization': 'token ' + token}

    r = requests.get(githuburl, headers=headers)
    raw = r.text
    results = json.loads(raw)

    # print(pd.DataFrame(results))

    pd.options.display.float_format = '{:,.0f}'.format

    df = pd.DataFrame(results)

    conn = sqlite3.connect("db.sqlite")
    cursor = conn.cursor()

    df['date'] = pd.to_datetime(df.week, unit='s')  # seconds from epoch time

    # df['week_no'] = df.apply(lambda x: '{:d}-{:02d}'.format(x['date'].year, x['date'].weekofyear), axis=1)

    # mensal
    df['month'] = df.apply(lambda x: '{:d}/{:02d}/{:02d}'.format(x['date'].year, x['date'].month, x['date'].month),
                           axis=1)

    # df['epoch'] = df.date.values.astype(np.int64)

    # from monthly to timestamp (needed in highcharts)
    df['epoch'] = df.apply(
        lambda x: datetime.datetime(x['date'].year, x['date'].month, 1, 0, 0).timestamp(), axis=1)

    # from weekly to timestamp
    df['epochs'] = df.apply(
        lambda x: datetime.datetime(x['date'].year, x['date'].month, x['date'].day, 0, 0).timestamp(), axis=1)

    df['coinname'] = coinname.lower()

    # df['month'].sum()

    # ds = df.groupby('month')['total'].sum()
    df['epochs'] = df['epochs'].astype(int)
    ds = df.groupby(['coinname', 'epochs']).sum()

    ds['epoch'] = ds['epoch'].astype(int)
    # ds = df.groupby('epochs')['total'].sum()
    # cursor.execute("delete from coins where coinname=(?)", (coinname.lower(),))
    try:

        cursor.execute("delete from coins where coinname=(?)", (coinname.lower(),))
        conn.commit()
    except:
        pass

    # save data to table
    ds.to_sql("coins", conn, if_exists="append")
    conn.close()
    return True
