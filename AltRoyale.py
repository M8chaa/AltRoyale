import streamlit as st
import pandas as pd
from Google import Create_Service
from streamlit_gsheets import GSheetsConnection
import re
import numpy as np

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
    range_name = f"planDataSheet!A{start_row}:AG{end_row}"
    result = sheet.values().get(spreadsheetId=sheetID, range=range_name).execute()
    values = result.get('values', [])

    # Fetch first row to get header columns
    headers = serviceInstance.spreadsheets().values().get(spreadsheetId=sheetID, range=f"planDataSheet!A1:AG1").execute().get('values', [])[0]
    data = values[1:]  # Fetch rows excluding header row
    df = pd.DataFrame(data, columns=headers)
    return df

st.set_page_config(page_title="금순위", page_icon=":crown:", layout="wide")
# Get sheet

# Example headers: url	MVNO	요금제명	월 요금	월 데이터	일 데이터	데이터 속도	통화(분)	문자(건)	통신사	망종류	할인정보	통신사 약정	번호이동 수수료	일반 유심 배송	NFC 유심 배송	eSim	지원	미지원	이벤트	카드 할인	월 요금 (숫자)	월 데이터 (숫자)	일 데이터 (숫자)	데이터 속도 (숫자)	통화(분) (숫자)	문자(건) (숫자)	점수
# Example data: https://www.moyoplan.com/plans/16030	프리티	음성기본데이터3G	3,850원	3GB	제공안함	제공안함	무제한	무제한	SKT	3G	12개월 이후 14,300원	없음	없음	유료(2,200원)	유료(4,400원)	지원 안 함	모바일 핫스팟: 3GB 제공, 해외 로밍: 신청은 통신사에 문의	소액 결제, 인터넷 결합, 데이터 쉐어링	제공안함	제공안함	3850	3	0	0	100000	100000	196156

# Bring first 20 rows of data in the beginning of app
df = getSheetData(2, 53)

# Add columns on df
# Add new columns on df
# df['이벤트 가격'] = ""  # Initialize with empty strings or any default value
# df['할인 기간'] = ""  # Initialize with empty strings or any default value
# df['할인 적용 가격'] = ""  # Initialize with empty strings or any default value
# df['할인 점수'] = ""  # Initialize with empty strings or any default value
# df['순위'] = ""  # Initialize with empty strings or any default value

# Define a dictionary to map the events to their prices
event_price_mapping = {
    "3대 마트 상품권 3만원": 30000,
    "3대 마트 상품권 2만원": 20000,
    "SKY 쿠폰 2만원": 20000,
    "SKY 쿠폰 1만원": 10000,
    "밀리의 서재": 9900,
    "네이버페이 5천원": 5000,
    "매달 네이버페이 포인트 2만5천원": 150000
}

event_discount_period_mapping = {
    "3대 마트 상품권 3만원": 6,
    "3대 마트 상품권 2만원": 6,
    "SKY 쿠폰 2만원": 6,
    "SKY 쿠폰 1만원": 6,
    "밀리의 서재": 1,
    "네이버페이 5천원": 3,
    "매달 네이버페이 포인트 2만5천원": 6
}

# Create a regex pattern that matches any of the keys in event_price_mapping
pattern = '|'.join(map(re.escape, event_price_mapping.keys()))

# Update '이벤트' column based on '이벤트' price mapping
df['이벤트'] = df['이벤트'].apply(lambda x: ', '.join(re.findall(pattern, x)) if x != '제공안함' else x)

# Update '이벤트 가격' column based on '이벤트' column
df['이벤트 가격'] = df['이벤트'].apply(lambda x: sum(event_price_mapping.get(i, 0) for i in x.split(', ')))


# Update '할인 적용 가격' column based on '할인기간' & '이벤트 가격' columns
# On 할인정보 column, extract n from n개월 이후
# def calculate_discount_period(row):
#     discount_period = 1
#     if row['할인정보'] != '제공안함':
#         discount_period = int(re.findall(r'(\d+)개월 이후', row['할인정보'])[0])
#     if row['이벤트'] in event_discount_period_mapping:
#         event_discount_period = event_discount_period_mapping[row['이벤트']]
#         discount_period = max(discount_period, event_discount_period)
#     return discount_period

# # Remove the comma and the won symbol from '월 요금' column
# def convert_to_float(val):
#     try:
#         return float(val)
#     except ValueError:
#         return np.nan

# df['월 요금'] = df['월 요금'].str.replace(',', '').str.replace('원', '').apply(convert_to_float)

# df['할인 기간'] = df.apply(calculate_discount_period, axis=1)

# Convert empty strings to NaN
# df['이벤트 가격'] = df['이벤트 가격'].replace('', np.nan)
# df['할인 기간'] = df['할인 기간'].replace('', np.nan)

# # Now you can convert these columns to float
# df['이벤트 가격'] = df['이벤트 가격'].astype(float)
# df['할인 기간'] = df['할인 기간'].astype(float)

# df['월 요금 (숫자)'] = df['월 요금 (숫자)'].astype(float)
# df['할인 적용 가격'] = df['월 요금 (숫자)'] - (df['이벤트 가격'].astype(float) / df['할인 기간'].astype(float))

# weights
# '월 요금': -1,
# '월 데이터': 2,
# '일 데이터': 1,
# '데이터 속도': 1,
# '통화(분)': 1,
# '문자(건)': 1,

# df['할인 점수'] = df['할인 적용 가격'] * -2 + df['월 데이터 (숫자)'].astype(float) * 2 + df['일 데이터 (숫자)'].astype(float) * 1 + df['데이터 속도 (숫자)'].astype(float) * 10000 + df['통화(분) (숫자)'].astype(float) * 1 + df['문자(건) (숫자)'].astype(float) * 1

# # Update sheet for the new columns
# serviceInstance = googleSheetConnect()
# sheet = serviceInstance.spreadsheets()
# sheetID = "12s6sKkpWkHdsx_2kxFRim3M7-VTEQBmbG4OPgFrG0n0"

# # Select only the new columns
# new_columns = ['이벤트 가격', '할인 기간', '할인 적용 가격', '할인 점수', '순위']
# df_new = df[new_columns]

# data = df_new.values.tolist()
# headers = df_new.columns.tolist()
# data = [headers] + data

# # Clear the existing values in the range
# sheet.values().clear(spreadsheetId=sheetID, range="planDataSheet!AC1:AG").execute()

# # Update the range with new values
# sheet.values().update(spreadsheetId=sheetID, range="planDataSheet!AC1:AG", valueInputOption="USER_ENTERED", body={"values": data}).execute()

# # Assuming you've already set up API credentials and sheetID
# spreadsheet_id = '12s6sKkpWkHdsx_2kxFRim3M7-VTEQBmbG4OPgFrG0n0'  # Please replace this with your actual spreadsheet ID
# service = googleSheetConnect()

# request_body = {
#     "requests": [
#         {
#             "sortRange": {
#                 "range": {
#                     "sheetId": 722062841,  # Replace with the actual sheet ID if needed; use 0 if you're sorting the first sheet and don't have the specific ID
#                     "startRowIndex": 1,
#                     "endRowIndex": 1753,  # Adjust this based on the actual number of rows in your sheet
#                     "startColumnIndex": 0,
#                     "endColumnIndex": 32  # Assuming '할인 점수' is in the AG column, which is the 33rd column
#                 },
#                 "sortSpecs": [
#                     {
#                         "dimensionIndex": 31,  # '할인 점수' column index (AG column is the 33rd column, but indexing starts from 0)
#                         "sortOrder": "DESCENDING"
#                     }
#                 ]
#             }
#         }
#     ]
# }

# response = service.spreadsheets().batchUpdate(
#     spreadsheetId=spreadsheet_id,
#     body=request_body
# ).execute()
# st.write(response)




st.title("금순위: 요금제 비교 사이트")
st.markdown("""
    금순위에 오신 것을 환영합니다. 알뜰 요금제를 비교하고 최적의 요금제를 찾아보세요
""")


sorted_df = df.sort_values(by="순위", ascending=False)
# sorted_df['순위'] = range(1, len(sorted_df) + 1)
text_search = st.text_input("요금제 이름으로 찾으세요", value="")

# Filter the dataframe based on search
m1 = df["요금제명"].str.contains(text_search, case=False, na=False)  # Adjust column name as necessary
df_search = sorted_df[m1]

import streamlit.components.v1 as components

N_cards_per_row = 3
if text_search:
    df_display = df_search.sort_values(by="순위", ascending=False)
else:
    df_display = sorted_df

for n_row, row in df_display.iterrows():
    st.write("---")  # Separator line between cards

    if row['순위'] == 1:
        st.markdown(":first_place_medal: 순위: 1")
    elif row['순위'] == 2:
        st.markdown(":second_place_medal: 순위: 2")
    elif row['순위'] == 3:
        st.markdown(":third_place_medal: 순위: 3")
    else:
        st.text(f"순위: {row['순위']}")
    st.subheader(f"{row['요금제명']}")
    data_text = ""
    if row['월 데이터'] != "제공안함":
        data_text += f"월 {row['월 데이터']} "
    if row['일 데이터'] != "제공안함":
        data_text += f"+ 일 {row['일 데이터']} "
    if row['데이터 속도'] != "제공안함":
        data_text += f"+ 소진 시 {row['데이터 속도']}"
    if data_text:
        st.markdown(f"<div style='margin-top:-15px;'><medium><b>{data_text.strip()}</b></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='margin-top:-5px;'><medium><b>월 요금:</b> {row['월 요금']}</small></div>", unsafe_allow_html=True)
    
    st.markdown(f"<div style='margin-top:-5px;'><small>전화 (분): {row['통화(분)']}</small></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='margin-top:-10px;'><small>문자 (건): {row['문자(건)']}</small></div>", unsafe_allow_html=True)
    if row['이벤트'] != "제공안함":
        st.markdown(f"<div style='margin-top:-10px;'><small>이벤트: {row['이벤트']}</small></div>", unsafe_allow_html=True)
    if row['할인 적용 가격'] != "":
        st.markdown(f"<div style='margin-top:-10px;'><small>할인 적용 가격: 최대 월 {(row['할인 적용 가격'])}원</small></div>", unsafe_allow_html=True)
    st.markdown('<style>.css-1aumxhk {border: 1px solid #ccc; border-radius: 5px; padding: 10px;}</style>', unsafe_allow_html=True)