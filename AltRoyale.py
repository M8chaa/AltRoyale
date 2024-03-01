import streamlit as st
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

def getSheetData(start_row, end_row):
    serviceInstance = googleSheetConnect()
    sheet = serviceInstance.spreadsheets()
    sheetID = "12s6sKkpWkHdsx_2kxFRim3M7-VTEQBmbG4OPgFrG0n0"
    range_name = f"planDataSheet!A{start_row}:AB{end_row}"
    result = sheet.values().get(spreadsheetId=sheetID, range=range_name).execute()
    values = result.get('values', [])
    headers = values[0]
    data = values[1:]  # Fetch rows excluding header row
    df = pd.DataFrame(data, columns=headers)
    return df


# Get sheet

# Example headers: url	MVNO	요금제명	월 요금	월 데이터	일 데이터	데이터 속도	통화(분)	문자(건)	통신사	망종류	할인정보	통신사 약정	번호이동 수수료	일반 유심 배송	NFC 유심 배송	eSim	지원	미지원	이벤트	카드 할인	월 요금 (숫자)	월 데이터 (숫자)	일 데이터 (숫자)	데이터 속도 (숫자)	통화(분) (숫자)	문자(건) (숫자)	점수
# Example data: https://www.moyoplan.com/plans/16030	프리티	음성기본데이터3G	3,850원	3GB	제공안함	제공안함	무제한	무제한	SKT	3G	12개월 이후 14,300원	없음	없음	유료(2,200원)	유료(4,400원)	지원 안 함	모바일 핫스팟: 3GB 제공, 해외 로밍: 신청은 통신사에 문의	소액 결제, 인터넷 결합, 데이터 쉐어링	제공안함	제공안함	3850	3	0	0	100000	100000	196156

# Bring first 20 rows of data in the beginning of app
df = getSheetData(2, 21)

st.set_page_config(page_title="알뜰로얄", page_icon=":crown:", layout="wide")

st.title("알뜰로얄: 요금제 비교 사이트")
st.markdown("""
    알뜰로얄에 오신 것을 환영합니다. 알뜰 요금제를 비교하고 최적의 요금제를 찾아보세요
""")


# Assuming 'Plan Name' and 'Score' columns exist
# df = getSheetData()
# df = pd.DataFrame({
#     '요금제명': ['Plan A', 'Plan B', 'Plan C', 'Plan D', 'Plan E', 'Plan F', 'Plan G', 'Plan H', 'Plan I', 'Plan J'],
#     '점수': [8.5, 9.2, 7.8, 8.0, 9.5, 7.2, 8.8, 9.0, 7.5, 8.3],
#     '월 데이터 (GB)': [20, 30, 15, 25, 35, 10, 30, 40, 20, 15],
#     '월 요금': [30, 40, 25, 35, 45, 20, 40, 50, 30, 25],
#     '데이터 속도 (Mbps)': [50, 60, 40, 55, 65, 30, 60, 70, 50, 45],
#     '전화': [150, 200, 250, 180, 120, 280, 220, 160, 300, 140],
#     '문자': [250, 180, 220, 280, 150, 200, 120, 160, 140, 300]
# })

sorted_df = df.sort_values(by="점수", ascending=False)
text_search = st.text_input("Search plans by name or other criteria", value="")

# Filter the dataframe based on search
m1 = df["요금제명"].str.contains(text_search, case=False, na=False)  # Adjust column name as necessary
df_search = df[m1]

import streamlit.components.v1 as components

N_cards_per_row = 3
if text_search:
    df_display = df_search.sort_values(by="점수", ascending=False)
else:
    df_display = sorted_df

for n_row, row in df_display.iterrows():
    st.write("---")  # Separator line between cards

    st.subheader(f"{row['요금제명']}")
    st.text(f"Rank: {row['점수']}")
    st.text(f"Monthly Data (GB): {row['월 데이터 (GB)']}")
    st.text(f"Monthly Fee: {row['월 요금']}₩")
    st.text(f"Data Speed (Mbps): {row['데이터 속도 (Mbps)']}")
    st.text(f"Call Minutes: {row['전화']} mins")
    st.text(f"SMS: {row['문자']} messages")
    st.markdown('<style>.css-1aumxhk {border: 1px solid #ccc; border-radius: 5px; padding: 10px;}</style>', unsafe_allow_html=True)