import streamlit as st
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from Google import Create_Service
from streamlit_gsheets import GSheetsConnection

def googleSheetConnect():
    CLIENT_SECRETS = st.secrets["GoogleDriveAPISecrets"]
    API_NAME = 'sheets'
    API_VERSION = 'v4'
    SCOPES = ['https://www.googleapis.com/auth/drive']
    serviceInstance = Create_Service(CLIENT_SECRETS, API_NAME, API_VERSION, SCOPES)
    return serviceInstance

def getSheetData():
    serviceInstance = googleSheetConnect()
    sheet = serviceInstance.spreadsheets()
    sheetID = "Sheet3"
    result = sheet.values().get(spreadsheetId=sheetID, range="Sheet3").execute()
    values = result.get('values', [])
    headers = values[0]
    data = values[1:]
    df = pd.DataFrame(data, columns=headers)
    return df


st.set_page_config(page_title="알뜰로얄", page_icon=":mobile_phone_off:", layout="wide")

st.title("알뜰로얄: The Mobile Data Plan Battle Royale")
st.markdown("""
    Welcome to 알뜰로얄, where we rank the best mobile data plans for your needs! Dive in to find the champion in cost-efficiency, speed, and more.
""")


# Assuming 'Plan Name' and 'Score' columns exist
# df = getSheetData()
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
st.dataframe(sorted_df)

# Example: Highlighting top 3 plans
st.dataframe(sorted_df.style.apply(lambda x: ['background: lightgreen' if x.name in sorted_df.head(10).index else '' for i in x], axis=1))

# Example: Filter by data limit
data_limit = st.slider("Minimum Data Limit (GB)", min_value=0, max_value=int(df['월 데이터 (GB)'].max()), value=10)
filtered_df = sorted_df[sorted_df['월 데이터 (GB)'] >= data_limit]
st.dataframe(filtered_df)

# Show more button
if st.button("Show More"):
    # Load 10 more plans
    more_plans = pd.DataFrame({
        '요금제명': ['Plan K', 'Plan L', 'Plan M', 'Plan N', 'Plan O', 'Plan P', 'Plan Q', 'Plan R', 'Plan S', 'Plan T'],
        '순위': [7.0, 8.8, 6.5, 7.2, 9.0, 6.8, 8.5, 9.2, 7.8, 8.0],
        '월 데이터 (GB)': [10, 25, 20, 30, 40, 15, 30, 35, 25, 20],
        '월 요금': [20, 35, 30, 40, 50, 25, 40, 45, 35, 30],
        '데이터 속도 (Mbps)': [40, 55, 50, 60, 70, 45, 60, 65, 55, 50],
        '전화': [120, 180, 160, 200, 220, 140, 200, 250, 180, 160],
        '문자': [200, 280, 250, 180, 160, 300, 180, 220, 280, 250]
    })
    sorted_df = pd.concat([sorted_df, more_plans])
    st.dataframe(sorted_df)

