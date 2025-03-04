import streamlit as st
import numpy as np
import datetime
import pandas as pd
import datetime
import time
import math

from streamlit.proto.Checkbox_pb2 import Checkbox

st.sidebar.subheader('必要事項を入力')
cost = st.sidebar.number_input('①税抜原価（円）',  min_value=0, max_value=99999999, step=1)
amount = st.sidebar.number_input('②仕入数量（個）',  min_value=0, max_value=99999999, step=1)
selling = st.sidebar.number_input('③税込売価（円）',  min_value=0, max_value=99999999, step=1)

sellingCost = 0.1

ship_ = st.sidebar.selectbox('④送料区分', ['送料別', '送料無料', 'メール便無料'])
if ship_ == '送料別':
    ship = 0
elif ship_ == '送料無料':
    ship = 550
else:
    ship = 180

if st.sidebar.button('軽減税率対象'):
    tax = 0.08
else:
    tax = 0.10

st.sidebar.write("""* * *""")
salesCost = st.sidebar.info('販売手数料/個：' + str("{:,}".format(selling * sellingCost)) + '円')

varriableCost1 = st.sidebar.number_input('★変動費1/個（円）',  min_value=0, max_value=99999999, step=1)
varriableCost2 = st.sidebar.number_input('★変動費2/個（円）',  min_value=0, max_value=99999999, step=1)
varriableCost3 = st.sidebar.number_input('★変動費3/個（円）',  min_value=0, max_value=99999999, step=1)

if cost != 0 and amount != 0 and selling != 0:
    totalCosts = (cost*amount)*(1+tax)

    for i in range(0, amount + 1):
        sales = selling * i
        costs = cost * i
        ships = ship * i
        salesCosts = (selling * i) * sellingCost
        varriableCosts = (varriableCost1 * i) + (varriableCost2 * i) + (varriableCost3 * i)
        if (sales >= (totalCosts + ships + salesCosts)):
            breakEvenPoint = i
            break
        else:
            breakEvenPoint = '無し'
else:
    breakEvenPoint = 0

st.title('損益分岐点計算')
st.subheader('損益分岐点は ' + str(breakEvenPoint) + ' です')

st.subheader('完売時の合計')
col7, col8, col9 = st.columns(3)
with col7:
    costTotal = st.info('仕入金額：' + str("{:,}".format(cost * amount)) + '円')
with col8:
    sellingTotal = st.info('売上金額：' + str("{:,}".format(selling * amount)) + '円')
with col9:
    profitTotal = st.info('最終損益：' + str("{:,}".format((round(selling - ((cost * (1 + tax)) + (selling * (varriableCost3)) + (varriableCost1) + (varriableCost2) + (ship) + (selling * sellingCost))) * amount))) + '円')

units = []
costs = []
sellings = []
profits = []
profitLoss = []

for i in range(1, amount + 1):
    units.append(i)
    costs_ = (math.floor((cost * (1 + tax)) * amount) + (i * varriableCost1) + (i * varriableCost2) + (i * selling * varriableCost3) + (i * ship) + (i * (selling * sellingCost)))
    costs.append(round(costs_))
    sellings.append(round(i * selling))
    profits.append(i * round(selling - (cost * (1 + tax))))

for i in range(len(costs)):
    tmp = round(sellings[i] - costs[i])
    profitLoss.append(tmp)

dfChart = {
    '販売原価': costs,
    '売上金額': sellings,
}
dfTable = {
    '販売数量': units,
    '販売原価': costs,
    '売上金額': sellings,
    '粗利金額': profits,
    '損益金額': profitLoss,
}
df = pd.DataFrame(dfChart)
df_ = pd.DataFrame(dfTable)

st.subheader('推移グラフ')
st.line_chart(df)
st.subheader('推移一覧表')
st.table(df_.set_index('販売数量'))
