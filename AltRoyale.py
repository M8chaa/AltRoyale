import streamlit as st
import pandas as pd

st.set_page_config(page_title="알뜰로얄", page_icon=":crown:", layout="wide")

st.title("알뜰로얄: 요금제 비교 사이트")
st.markdown("""
    알뜰로얄에 오신 것을 환영합니다. 알뜰 요금제를 비교하고 최적의 요금제를 찾아보세요
""")

df = pd.DataFrame({
    '요금제명': ['Plan A', 'Plan B', 'Plan C', 'Plan D', 'Plan E', 'Plan F', 'Plan G', 'Plan H', 'Plan I', 'Plan J'],
    '순위': [8.5, 9.2, 7.8, 8.0, 9.5, 7.2, 8.8, 9.0, 7.5, 8.3],
    '월 데이터 (GB)': [20, 30, 15, 25, 35, 10, 30, 40, 20, 15],
    '월 요금': [30, 40, 25, 35, 45, 20, 40, 50, 30, 25],
    '데이터 속도 (Mbps)': [50, 60, 40, 55, 65, 30, 60, 70, 50, 45],
    '전화': [150, 200, 250, 180, 120, 280, 220, 160, 300, 140],
    '문자': [250, 180, 220, 280, 150, 200, 120, 160, 140, 300]
})

sorted_df = df.sort_values(by="순위", ascending=True)

st.subheader("Leaderboard")
st.markdown('<style>.leaderboard {border-collapse: collapse; width: 100%;} .leaderboard th, .leaderboard td {border: 1px solid #ddd; padding: 8px; text-align: left;} .leaderboard th {background-color: #f2f2f2;}</style>', unsafe_allow_html=True)
st.markdown('<table class="leaderboard"><tr><th>Rank</th><th>Plan Name</th><th>Monthly Data (GB)</th><th>Monthly Fee</th><th>Data Speed (Mbps)</th><th>Call Minutes</th><th>SMS</th></tr></table>', unsafe_allow_html=True)

for n_row, row in sorted_df.iterrows():
    st.markdown(f'<table class="leaderboard"><tr><td>{row["순위"]}</td><td>{row["요금제명"]}</td><td>{row["월 데이터 (GB)"]}</td><td>{row["월 요금"]}₩</td><td>{row["데이터 속도 (Mbps)"]}</td><td>{row["전화"]} mins</td><td>{row["문자"]} messages</td></tr></table>', unsafe_allow_html=True)
