# this is for back testingging
import os
from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException
from datetime import datetime

import talib
import numpy
import csv
import pandas as pd
open('trades.csv', 'w+').close()
filet = open('trades.csv', 'a', newline='')
file = 'oport.csv'
open(file, 'w+').close()
file = open('oport.csv', 'a', newline='')
client = Client('SS2',
                'TFU')

sltp = 1
EMATP = 14
ATRTP = 7
tradesval = 100


def historicbt():
    klines = client.get_historical_klines(
        'SANDUSDT', Client.KLINE_INTERVAL_5MINUTE,  "1 Nov, 2021", )

    #"1 Jan, 2021", "30 Jan, 2021"
    #"1 Feb, 2021", "28 Feb, 2021"
    #"1 March, 2021", "30 March, 2021"
    #"1 April, 2021", "30 April, 2021"
    # "1 Oct, 2021", "31 Oct, 2021"
    #"1 Sep, 2021", "30 Sep, 2021"
    #"1 June, 2021", "30 June, 2021"
    #"1 May, 2021", "30 May, 2021"
    #"16 Oct, 2021", "19 Oct, 2021"
    #"1 July, 2021", "30 July, 2021"
    #"1 August, 2021", "30 August, 2021"
    df = pd.DataFrame(klines)

    df = df.apply(pd.to_numeric)

    df = df.set_axis(['time', 'opens', 'highs', 'lows', 'closes',
                     'volumes', '7', '8', '9', '10', '11', '12'], axis=1)

    fileh = 'november15.csv'  # str(file) + str('history.csv')
    df.to_csv(fileh)
    #df = pd.read_csv('SANDUSDThistory.csv')

    #"1 Jan, 2021", "30 Jan, 2021"
    #"1 Feb, 2021", "28 Feb, 2021"
    #"1 March, 2021", "30 March, 2021"
    #"1 April, 2021", "30 April, 2021"
    # "1 Oct, 2021", "31 Oct, 2021"
    #"1 Sep, 2021", "30 Sep, 2021"
    #"1 June, 2021", "30 June, 2021"
    #"1 May, 2021", "30 May, 2021"
    #"16 Oct, 2021", "19 Oct, 2021"
    #"1 July, 2021", "30 July, 2021"
    #"1 August, 2021", "30 August, 2021"

    #"2 Hours ago UTC"
    # processed_klinesbt = []

    # processed_klinesbt.append(kline)
    # pkll = list(processed_klinesbt)
    # print(close)

    listedc = list()
    listedt = list()
    for nu in range(len(df)):
        time = df['time'][nu]
        time = time/1000

        listedt.append(datetime.utcfromtimestamp(
            int(time)).strftime('%Y-%m-%d %H:%M'))

    i = 15
    output = talib.EMA(df['closes'], timeperiod=20)
    ema = talib.EMA(df['closes'], timeperiod=20)
    #ema6 = talib.EMA(arr, timeperiod=6)
    #ema9 = talib.EMA(arr, timeperiod=9)
    real = talib.ATR(df['highs'], df['lows'], df['closes'], timeperiod=ATRTP)

    #tstart = listedt[0]
    #startts = datetime.fromtimestamp('1633860000000')

    print("timestamp start: " + str(listedt[0]))
    print("timestamp end: " + str(listedt[19]))

    return i, listedt, listedc, output,
    # probably have to new fx def


RSITime = 14


def is_dumping(df):
    i = 1
    p = i+10
    while (i < p):
        if df['closes'].iloc[i]:
            print("hello")
        return True


def is_consolidating(i, df, percentage=1):

    m = i-15
    recent_candlesticks = df[(df.index < i) & (df.index > m)]

    max_close = recent_candlesticks['closes'].max()
    min_close = recent_candlesticks['closes'].min()

    threshold = 1 - (percentage / 100)
    if min_close > (max_close * threshold):

        time = df['time'].iloc[i]
        time = time/1000
        time = datetime.utcfromtimestamp(
            int(time)).strftime('%Y-%m-%d %H:%M')
        timett = [time, df['closes'].iloc[i]]
        csv.writer(file, delimiter=',').writerow(timett)
        return True


listedt = list()


def is_breaking_out(i, df, percentage=1):
    for nu in range(len(df)):
        time = df['time'][nu]
        time = time/1000

        listedt.append(datetime.utcfromtimestamp(
            int(time)).strftime('%Y-%m-%d %H:%M'))
    output = talib.EMA(df['closes'], timeperiod=20)
    while i < len(df['closes']):
        last_close = df['closes'].iloc[i]

        if is_consolidating(i, df, percentage=percentage):
            m = i-16
            recent_closes = df[(df.index < i) & (df.index > m)]
            print("consolidating")
            size_candlenow = df['closes'].iloc[i]-df['opens'].iloc[i]
            real = talib.ATR(df['highs'], df['lows'],
                             df['closes'], timeperiod=ATRTP)

            size_candleprev = abs(df['closes'].iloc[i-1]-df['opens'].iloc[i-1])
            if last_close > recent_closes['closes'].max() and size_candlenow > real.iloc[i-1]:
                time = df['time'].iloc[i]
                time = time/1000
                time = datetime.utcfromtimestamp(
                    int(time)).strftime('%Y-%m-%d %H:%M')
                timett = [time, df['closes'].iloc[i], 'brokeout']
                csv.writer(file, delimiter=',').writerow(timett)

                i = fibvalue(i, listedt, df, output)

            else:
                print("not brokeout")

        i += 1


def fibvalue(i, listedt, df, output):

    loww = df['lows'].iloc[i]
    print("curent low"+str(df['lows'].iloc[i]))
    m = i-3
    # p = 0
    print("this is i before tp/sl hit: " + str(i))
    # print(df['lows'][m])
    while m <= i:
        if df['lows'][m] <= loww:
           #print("this is:" + str(df['lows'][m]))
            loww = df['lows'][m]
            #print("low has changed " + str(loww))

        # else:
           #print("low stay same:" + str(loww) + "  " + str(m))
        m += 1

    print("lowest from last five low: " + str(loww))

    i = buytpsl(i, listedt, df, output, loww)

    return i


totalval = 0


def buytpsl(i, listedt, df, output, loww):
    # setbuy order
    currclose = df['closes'].iloc[i]
    diff = currclose-loww
    buy1 = currclose
    buy2 = loww
    buy3 = buy1-(0.5*diff)
    buy4 = buy1-(0.68*diff)
    buy5 = buy1-(0.5*diff)
    avgbuy = buy1
    global sltp, tradesval, totalval
    avgbuylist = []

    file = open('trades.csv', 'a', newline='')
    real = talib.ATR(df['highs'], df['lows'], df['closes'], timeperiod=ATRTP)
    lowavgbuy = buy1

    avgbuylistratio = []
    # set sl
    stoploss = loww - 0.025*buy1
    # set tp
    diffreal = buy1 - stoploss

    factp = 1.75
    #print("plratio" + str(plratio))

    #print("plratio" + str(plratio))
    '''if stocsd[i] >= 60:
        tp1 = buy2+1.2*diffreal
    elif stocsd[i] < 60:
        tp1 = buy2+1.5*diffreal'''
    tp1 = buy2+0.05*buy2
    avgbuyratio = 100
    maxavgbuyratio = 100
    avgbuylist.append(avgbuy)
    avgbuylistratio.append(avgbuyratio)
    print("this is h: "+str(df['highs'].iloc[i+1]))
    print("this tp1: " + str(tp1))
    print("this is sl: " + str(stoploss))
    print("this is buy1: " + str(buy1))
    tp2 = buy1+2.2*diffreal
    # check tp for hit
    print("this is diff " + str(diff))

    #a = len(df['highs'])
    #liml = a-1
    enti = i
    i = i+1

    while i < len(df['highs']):

        if df['highs'].iloc[i] >= tp1:
            print("time tp hit" + str(listedt[i]))
            profittped = ((tp1-lowavgbuy)/lowavgbuy)+(-0.002)
            tradesval = profittped*maxavgbuyratio
            totalval += tradesval

            plratio = (tp1-lowavgbuy)/(lowavgbuy-stoploss)

            buystat = 'tphit'
            tradestped = [listedt[enti], listedt[i], buy1,
                          lowavgbuy, tp1, stoploss, buystat, profittped, maxavgbuyratio, plratio, tradesval, totalval, ]

            csv.writer(filet, delimiter=',').writerow(tradestped)
            print("total val: " + str(totalval))
            # file.write(str(tp1))
            #file.write(", tphit ,")

            sltp = 1

            break
        elif df['lows'].iloc[i] <= stoploss:
            print("stopped out")
            maxavgbuyratio = 100
            lossifsled = ((stoploss-lowavgbuy)/lowavgbuy)+(-0.002)
            tradesval = lossifsled*maxavgbuyratio
            plratio = (tp1-lowavgbuy)/(lowavgbuy-stoploss)
            totalval += tradesval

            tradessled = [listedt[enti], listedt[i], buy1, lowavgbuy, tp1,
                          stoploss, 'stopped out', lossifsled, maxavgbuyratio, plratio, tradesval, totalval]
            csv.writer(filet, delimiter=',').writerow(tradessled)
            print("total val: " + str(totalval))

            sltp = 1
            # file.write(str(stoploss))
            #file.write(", stopped out")
            break

        else:
            '''if df['lows'].iloc[i] <= buy2:
                avgbuyratio = 100
                avgbuy = (buy2+buy1)/2
                if avgbuy in avgbuylist:
                    print("buy already done5")
                else:
                    print("selling sand from buy 1")

                    avgbuylist.append(avgbuy)
                    avgbuylistratio.append(avgbuyratio)'''

            '''if df['lows'].iloc[i] > buy3 and df['lows'].iloc[i] <= buy2:

                avgbuyratio = 
                avgbuy = (buy2+buy1)/2

                if avgbuy in avgbuylist:
                    print("buy already done2")
                else:
                    # execute buy order 2
                    print("selling crv from buy 2")

                    avgbuylist.append(avgbuy)
                    avgbuylistratio.append(avgbuyratio)
                    #tp1 = avgbuy+diffreal'''

            '''elif df['lows'].iloc[i] > buy4 and df['lows'].iloc[i] <= buy3:
                # execute buy order 3
                avgbuyratio = 70
                avgbuy = (buy3+buy2+buy1)/3
                if avgbuy in avgbuylist:
                    print("buy already done3")
                else:
                    print("selling crv from buy 3")

                    avgbuylist.append(avgbuy)
                    avgbuylistratio.append(avgbuyratio)
                    #tp1 = avgbuy+diffreal

            elif df['lows'].iloc[i] > buy5 and df['lows'].iloc[i] <= buy4:
                avgbuyratio = 80
                avgbuy = (buy4+buy3+buy2+buy1)/4
                if avgbuy in avgbuylist:
                    print("buy already done4")
                else:
                    print("selling crv from buy 4")

                    avgbuylist.append(avgbuy)
                    avgbuylistratio.append(avgbuyratio)
                    #tp1 = avgbuy+diffreal
                execute buy order 4'''

            #tp1 = avgbuy+diffreal
            # execute buy order 5
            '''plratio = (tp1-lowavgbuy)/(lowavgbuy-stoploss)
            if plratio > 1.6:
                print("plratio big"+str(plratio))
                while plratio > 1.6:

                    tp1 = buy1 + factp*(real.iloc[i+1])
                    plratio = (tp1-lowavgbuy)/(lowavgbuy-stoploss)
                    print("plratio reduction"+str(plratio))
                    factp -= 0.02'''
            lowavgbuy = min(avgbuylist)
            maxavgbuyratio = max(avgbuylistratio)
        '''print("list of avgbuy : ")
            print(*avgbuylist, sep=", ")
            print("min is:", str(lowavgbuy))'''
        #tradesnhy = [buy1, "current price", 'not hit yet']
        #csv.writer(file, delimiter=',').writerow(tradesnhy)
        i += 1

    file.close()
    return i
    #condcheck(i, listedt, listedo, df['highs'], listedc, output, klines)


historicbt()
