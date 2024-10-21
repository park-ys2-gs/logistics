import streamlit as st
from streamlit_folium import folium_static
import folium
from folium.plugins import MarkerCluster
import pandas as pd
from folium import plugins


st.title("SK케미칼 임가공 최적화🚚")

# 각 장소의 위도, 경도 데이터
df = pd.DataFrame.from_dict({'출발지':['모아', 'KS TECH'],
                            '목적지':['부산항', '울산항'],
                            'cnt':[10, 20],
                            '출발지의_lat_long':[(38.5665, 126.9780),(37.5665, 136.9780)],
                            '목적지의_lat_long':[(36.5665, 126.9780),(37.5665, 116.9780)]})

threshold = st.slider("몇 개 이상의 CNT?", 0, 20, 12)
df = df[df['cnt']>=threshold]

m = folium.Map(location=(38.5665, 126.9780), zoom_start=5)

# 각 장소에 마커 추가
# for name, coord in locations.items():
#     folium.Marker(coord, popup=name).add_to(m)

# 고객사별 경로를 FeatureGroup으로 그룹화하고 LayerControl 추가
for index, row in df.iterrows():
    customer_key = f"고객사 {index}"

    # FeatureGroup 생성 (고객사별로 경로를 그룹화)
    fg = folium.FeatureGroup(name=customer_key)

    # 경로 시작점(우리 회사)에 녹색 마커 추가
    folium.Marker(row["출발지의_lat_long"], popup="임가공 업체", icon=folium.Icon(color='green', icon='play')).add_to(fg)

    # 경로 중간점(임가공 업체)에 파란 마커 추가
    # folium.Marker(row["목적지의_lat_long"], popup="판매처", icon=folium.Icon(color='blue', icon='cog')).add_to(fg)
    folium.Marker(row["목적지의_lat_long"], popup="판매처",
                icon=plugins.BeautifyIcon(icon="arrow-down",icon_shape="circle", border_width=2, number=3, background_color="green"),
                ).add_to(fg)
    
    # if option == "ALL":
    # 우리 회사 -> 임가공 업체 -> 고객사 경로 (파란색 선)
    folium.PolyLine(locations=[row['출발지의_lat_long'], row['목적지의_lat_long']],
                    color='blue', weight=row['cnt'], opacity=1).add_to(fg)

    # 지도에 FeatureGroup 추가
    fg.add_to(m)

# LayerControl 추가
folium.LayerControl(collapsed=False).add_to(m)
folium_static(m)