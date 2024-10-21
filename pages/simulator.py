import streamlit as st
import pandas as pd
from haversine import haversine

st.title("SK케미칼 임가공 최적화🚚")
df = pd.DataFrame.from_dict({'출발지':['모아', 'KS TECH'],
                            '목적지':['부산항', '울산항'],
                            'cnt':[10, 20],
                            '출발지의_lat_long':[(38.5665, 126.9780),(37.5665, 136.9780)],
                            '목적지의_lat_long':[(36.5665, 126.9780),(37.5665, 116.9780)]})

destination = st.selectbox(
    "목적지를 선택하세요.",
    # ("공장에서 임가공업체", "임가공 업체에서 내수 거래처", "임가공 업체에서 수출"),
    (df['목적지'].value_counts().index.to_list())
)

d_lat_long = df[df['목적지']==destination]['목적지의_lat_long'].values[0]

moa = df.iloc[0]['출발지의_lat_long']
ks = df.iloc[1]['출발지의_lat_long']
a = haversine(moa, d_lat_long, unit = 'km')
b = haversine(ks, d_lat_long, unit = 'km')

st.write("MOA에서 임가공 할 경우 총 이동 거리는 {}km입니다.".format(a))
st.write("KS TECH에서 임가공 할 경우 총 이동 거리는 {}km입니다.".format(b))
winner = min(a, b)
st.write("따라서 {}로 이동시킬 것을 추천합니다.".format(winner))
