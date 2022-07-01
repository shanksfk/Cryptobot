# this is for back testingging
from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException
from datetime import datetime

import talib
import numpy
import csv
open('trades.csv', 'w+').close()
client = Client('XX',
                'XXZ')

sltp = 1
EMATP = 14
ATRTP = 7
tradesval = 100


def historicbt():
    klines = client.get_historical_klines(
        "RUNEUSDT", Client.KLINE_INTERVAL_30MINUTE, "1 Oct, 2021", "31 Oct, 2021")

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
    for nu in klines:
        closed = float(nu[4])

        # can put ema.long logic here
        listedc.append(closed)

    # print(output)

    listedh = list()
    for nu in klines:
        highed = float(nu[2])
        listedh.append(highed)
    listedt = list()
    for nu in klines:
        time = float(nu[0]/1000)

        listedt.append(datetime.utcfromtimestamp(
            int(time)).strftime('%Y-%m-%d %H:%M'))
        listedo = list()
    for nu in klines:
        openp = float(nu[1])
        listedo.append(openp)
    listedl = list()
    for nu in klines:
        lowed = float(nu[3])
        listedl.append(lowed)
    i = 20
    arrh = numpy.array(listedh)
    arrl = numpy.array(listedl)
    arrc = numpy.array(listedc)
    arr = numpy.array(listedc)
    output = talib.EMA(arr, timeperiod=20)
    ema50 = talib.EMA(arr, timeperiod=20)
    #ema6 = talib.EMA(arr, timeperiod=6)
    #ema9 = talib.EMA(arr, timeperiod=9)
    real = talib.ATR(arrh, arrl, arrc, timeperiod=ATRTP)

    #tstart = listedt[0]
    #startts = datetime.fromtimestamp('1633860000000')
    '''
    startts = datetime.
    endts = datetime(int(listedt[19]))'''
    print("timestamp start: " + str(listedt[0]))
    print("timestamp end: " + str(listedt[19]))
    condcheck(i, listedt, listedo, listedh, listedc, listedl,
              output, klines, arr, ema50, real, ema50)
    return i, listedt, listedo, listedh, listedc, output, klines
    # probably have to new fx def


RSITime = 14


def condcheck(i, listedt, listedo, listedh, listedc, listedl, output, klines, arr, ema, real, ema50):
    arrh = numpy.array(listedh)
    arrl = numpy.array(listedl)
    arrc = numpy.array(listedc)
    arrt = numpy.array(listedt)
    ema3 = talib.EMA(arrc, timeperiod=3)
    ema6 = talib.EMA(arrc, timeperiod=6)
    ema9 = talib.EMA(arrc, timeperiod=9)

    rsi = talib.RSI(arrc, timeperiod=14)

    while i < (len(listedt)):

        # and ema6[i-3] < ema9[i-3]:
        if (ema3[i] > ema6[i] and ema6[i] > ema9[i]) and (ema3[i-3] < ema6[i-3]) and (ema6[i-6] < ema9[i-6] and ema6[i-9] < ema9[i-9]):
            print("ema 14" + str(ema6[i]))
            print("ema 20" + str(ema9[i]))
            print("ema 14-5" + str(ema6[i-5]))
            print("ema 20-5" + str(ema9[i-5]))
            print("ema 14-14 " + str(ema6[i-14]))
            print("ema 20-14 " + str(ema9[i-14]))

            size_candlenow = listedc[i]-listedo[i]
            size_candleprev = abs(listedc[i-1]-listedo[i-1])
            if size_candlenow > size_candleprev:
                if listedc[i] > output[i]:
                    # if rsi[i] < 75:

                    print("long now "+str(i))
                    print("time: " + str(listedt[i]))
                    '''print("open: " + str(listedo[i]))
                            print("close: " + str(listedc[i]))
                            print("EMA: " + str(float(output[i])))
                            print("next close: " + str(listedc[i+1]))
                            print("crossing high: " + str(listedh[i]))'''
                    i = fibvalue(i, listedt, listedo, listedh,
                                 listedc, output, klines)
                    #print("this is i tp/sl hit: " + str(i))

        else:
            # print("dont on t:" + str(i))
            '''print("open: " + str(listedo[i]))
            print("high: " + str(listedh[i]))
            print("close: " + str(listedc[i]))
            print("EMA: " + "{:.2f}".format(output[i]))
        # print("next close: " + str(listedc[i+1]))'''
        i += 1

    # print(float(listedc[n-13]))
    # pol = float(listedc[n-13])+float(listedc[n])
    # print(pol)
    # if listedc[n] > listedc[n]+listedc[n-13]:
    # print(processed_klines)

    return klines, i, listedc, listedh


def fibvalue(i, listedt, listedo, listedh, listedc, output, klines):

    listedl = list()
    for nu in klines:
        lowed = float(nu[3])
        listedl.append(lowed)

    loww = listedl[i]
    print("curent low"+str(listedl[i]))
    m = i-3
    # p = 0
    print("this is i before tp/sl hit: " + str(i))
    # print(listedl[m])
    while m <= i:
        if listedl[m] <= loww:
           #print("this is:" + str(listedl[m]))
            loww = listedl[m]
            #print("low has changed " + str(loww))

        # else:
           #print("low stay same:" + str(loww) + "  " + str(m))
        m += 1

    print("lowest from last five low: " + str(loww))

    i = buytpsl(i, listedt, listedo, listedh, listedc,
                listedl, output, klines, loww)

    return i


totalval = 0


def buytpsl(i, listedt, listedo, listedh, listedc, listedl, output, klines, loww):
    # setbuy order
    nextclose = listedc[i]
    diff = nextclose-loww
    buy1 = nextclose
    buy2 = buy1-(0.38*diff)
    buy3 = buy1-(0.5*diff)
    buy4 = buy1-(0.68*diff)
    buy5 = buy1-(0.68*diff)
    avgbuy = buy1
    global sltp, tradesval, totalval
    avgbuylist = []

    file = open('trades.csv', 'a', newline='')
    #csv.writer(file, delimiter=',')

    #file.write(str(buy1) + "," )
    # file.write(str(buy1))

    arrh = numpy.array(listedh)
    arrl = numpy.array(listedl)
    arrc = numpy.array(listedc)
    real = talib.ATR(arrh, arrl, arrc, timeperiod=ATRTP)
    lowavgbuy = buy1
    avgbuylistratio = []
    # set sl
    stoploss = loww - real[i]
    # set tp
    diffreal = buy1 - stoploss
    #tp1 = buy1+diffreal
    tp1 = buy1+1.5*diffreal
    # this is for appending  time of buy, buyprice, tp, and sl
    #plratio = (tp1-lowavgbuy)/(lowavgbuy-stoploss)
    factp = 1.75
    #print("plratio" + str(plratio))
    '''while plratio < 1.0:
        tp1 = buy1 + factp*(real[i+1])
        plratio = (tp1-lowavgbuy)/(lowavgbuy-stoploss)
        #print("plratio increment"+str(plratio))
        factp += 0.02'''
    #print("plratio" + str(plratio))

    avgbuyratio = 70
    maxavgbuyratio = 70

    avgbuylist.append(avgbuy)
    avgbuylistratio.append(avgbuyratio)
    print("this is h: "+str(listedh[i+1]))
    print("this tp1: " + str(tp1))
    print("this is sl: " + str(stoploss))
    tp2 = tp1+diff
    # check tp for hit
    print("this is diff " + str(diff))

    #a = len(listedh)
    #liml = a-1
    enti = i
    while i < len(listedh):

        if listedh[i] >= tp1:
            print("time tp hit" + str(listedt[i]))
            profittped = ((tp1-lowavgbuy)/lowavgbuy)+(-0.002)
            tradesval = profittped*maxavgbuyratio
            totalval += tradesval

            plratio = (tp1-lowavgbuy)/(lowavgbuy-stoploss)
            tradestped = [listedt[enti], listedt[i], buy1,
                          lowavgbuy, tp1, stoploss, 'tphit', profittped, maxavgbuyratio, plratio, tradesval, totalval]

            csv.writer(file, delimiter=',').writerow(tradestped)
            print("total val: " + str(totalval))
            # file.write(str(tp1))
            #file.write(", tphit ,")

            sltp = 1

            break
        elif listedl[i] <= stoploss:
            print("stopped out")
            maxavgbuyratio = 100
            lossifsled = ((stoploss-lowavgbuy)/lowavgbuy)+(-0.002)
            tradesval = lossifsled*maxavgbuyratio
            plratio = (tp1-lowavgbuy)/(lowavgbuy-stoploss)
            totalval += tradesval

            tradessled = [listedt[enti], listedt[i], buy1, lowavgbuy, tp1,
                          stoploss, 'stopped out', lossifsled, maxavgbuyratio, plratio, tradesval, totalval]
            csv.writer(file, delimiter=',').writerow(tradessled)
            print("total val: " + str(totalval))

            sltp = 1
            # file.write(str(stoploss))
            #file.write(", stopped out")
            break

        else:

            '''if listedl[i] > buy3 and listedl[i] <= buy2:

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
            if listedl[i] <= buy5:
                avgbuyratio = 100
                avgbuy = (buy5+buy1)/2

                #avgbuy = (buy5+buy4+buy3+buy2+buy1)/5
                if avgbuy in avgbuylist:
                    print("buy already done5")
                else:
                    print("selling crv from buy 5")

                    avgbuylist.append(avgbuy)
                    avgbuylistratio.append(avgbuyratio)
            '''elif listedl[i] > buy4 and listedl[i] <= buy3:
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

            elif listedl[i] > buy5 and listedl[i] <= buy4:
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

                    tp1 = buy1 + factp*(real[i+1])
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
    #condcheck(i, listedt, listedo, listedh, listedc, output, klines)


def backtest():
    print("check here1")
    k = historicbt()

    return True


k = backtest()
