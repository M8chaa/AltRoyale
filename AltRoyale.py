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

    # Fetch first row to get header columns
    headers = serviceInstance.spreadsheets().values().get(spreadsheetId=sheetID, range=f"planDataSheet!A1:AB1").execute().get('values', [])[0]
    data = values[1:]  # Fetch rows excluding header row
    df = pd.DataFrame(data, columns=headers)
    return df

st.set_page_config(page_title="알뜰로얄", page_icon=":crown:", layout="wide")
# Get sheet

# Example headers: url	MVNO	요금제명	월 요금	월 데이터	일 데이터	데이터 속도	통화(분)	문자(건)	통신사	망종류	할인정보	통신사 약정	번호이동 수수료	일반 유심 배송	NFC 유심 배송	eSim	지원	미지원	이벤트	카드 할인	월 요금 (숫자)	월 데이터 (숫자)	일 데이터 (숫자)	데이터 속도 (숫자)	통화(분) (숫자)	문자(건) (숫자)	점수
# Example data: https://www.moyoplan.com/plans/16030	프리티	음성기본데이터3G	3,850원	3GB	제공안함	제공안함	무제한	무제한	SKT	3G	12개월 이후 14,300원	없음	없음	유료(2,200원)	유료(4,400원)	지원 안 함	모바일 핫스팟: 3GB 제공, 해외 로밍: 신청은 통신사에 문의	소액 결제, 인터넷 결합, 데이터 쉐어링	제공안함	제공안함	3850	3	0	0	100000	100000	196156

# Bring first 20 rows of data in the beginning of app
df = getSheetData(2, 21)



st.title("알뜰로얄: 요금제 비교 사이트")
st.markdown("""
    알뜰로얄에 오신 것을 환영합니다. 알뜰 요금제를 비교하고 최적의 요금제를 찾아보세요
""")


sorted_df = df.sort_values(by="점수", ascending=False)
sorted_df['순위'] = range(1, len(sorted_df) + 1)
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
    st.text(f"순위: {row['순위']}")
    if row['월 데이터'] != "제공안함":
        st.text(f"월 데이터: {row['월 데이터']}")
    if row['일 데이터'] != "제공안함":
        st.text(f"일 데이터: {row['일 데이터']}")
    st.text(f"월 요금: {row['월 요금']}")
    if row['데이터 속도'] != "제공안함":
        st.text(f"데이터 속도: {row['데이터 속도']}")
    st.text(f"전화: {row['전화']} 분")
    st.text(f"문자: {row['문자']} 건")
    st.markdown('<style>.css-1aumxhk {border: 1px solid #ccc; border-radius: 5px; padding: 10px;}</style>', unsafe_allow_html=True)