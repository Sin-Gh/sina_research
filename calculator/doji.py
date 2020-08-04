import os
import sys

import tehran_stocks
from tehran_stocks.download import get_all_price, get_stock_groups, update_stock_price, get_stock_ids
from tehran_stocks import Stocks
from tehran_stocks.config import *

import pandas as pd
import requests
import datetime

def dragonfly_calculator(up_body,down_body,low):
    return float(down_body-low)/float(up_body-down_body) if up_body-down_body else float(down_body-low)/(up_body*.1)

def dragonfly_finder(date: text, intensity: int):
    q = f'select * from stock_price where dtyyyymmdd = {date}'
    df = pd.read_sql(q, engine)
    df['date'] = pd.to_datetime(df['dtyyyymmdd'], format='%Y%m%d')
    df['name'] = df.apply(lambda x: Stocks.query.filter_by(code=x.code).first().name, axis=1)
    df.reset_index(inplace = True)
    df.set_index('name', inplace = True)
    df['dragonfly_finder'] = df.apply(lambda x: dragonfly_calculator(max(x['first'],x['close']),min(x['first'],x['close']),x['low']), axis = 1)
    df['tombstone_finder'] = df.apply(lambda x: tombstone_calculator(max(x['first'],x['close']),min(x['first'],x['close']),x['high']), axis = 1)
    return df[(df['dragonfly_finder']>intensity)&(df['tombstone_finder']<10)].sort_values(by = ['dragonfly_finder'], ascending = False)
    
def tombstone_calculator(up_body,down_body,high):
    return float(high-up_body)/float(up_body-down_body) if up_body-down_body else float(high-up_body)/(up_body*.1)

def tombstone_finder(date: text, intensity:int):
    q = f'select * from stock_price where dtyyyymmdd = {date}'
    df = pd.read_sql(q, engine)
    df['date'] = pd.to_datetime(df['dtyyyymmdd'], format='%Y%m%d')
    df['name'] = df.apply(lambda x: Stocks.query.filter_by(code=x.code).first().name, axis=1)
    df.reset_index(inplace = True)
    df.set_index('name', inplace = True)
    df['tombstone_finder'] = df.apply(lambda x: tombstone_calculator(max(x['first'],x['close']),min(x['first'],x['close']),x['high']), axis = 1)
    df['dragonfly_finder'] = df.apply(lambda x: dragonfly_calculator(max(x['first'],x['close']),min(x['first'],x['close']),x['low']), axis = 1)
    return df[(df['tombstone_finder']>intensity)&(df['dragonfly_finder']<10)].sort_values(by = ['tombstone_finder'], ascending = False)

    