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


st.set_page_config(page_title="알뜰로얄", page_icon=":crown:", layout="wide")

st.title("알뜰로얄: 요금제 비교 사이트")
st.markdown("""
    알뜰로얄에 오신 것을 환영합니다. 알뜰 요금제를 비교하고 최적의 요금제를 찾아보세요
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
# st.dataframe(sorted_df)

# Example: Highlighting top 3 plans
# st.dataframe(sorted_df.style.apply(lambda x: ['background: lightgreen' if x.name in sorted_df.head(10).index else '' for i in x], axis=1))

# # Example: Filter by data limit
# data_limit = st.slider("Minimum Data Limit (GB)", min_value=0, max_value=int(df['월 데이터 (GB)'].max()), value=10)
# filtered_df = sorted_df[sorted_df['월 데이터 (GB)'] >= data_limit]
# st.dataframe(filtered_df)
# Implementing search and card display
# Use a text_input to get the keywords to filter the dataframe
text_search = st.text_input("Search plans by name or other criteria", value="")

# Filter the dataframe based on search
m1 = df["요금제명"].str.contains(text_search, case=False, na=False)  # Adjust column name as necessary
df_search = df[m1]

import streamlit.components.v1 as components

N_cards_per_row = 1  # For long cards that span the full width
# Display the results in a card layout if there is a search query
if text_search:
    for n_row, row in df_search.iterrows():
        i = n_row % N_cards_per_row
        if i == 0:
            st.write("---")  # Separator line between rows of cards
            cols = st.columns(N_cards_per_row, gap="large")
        
        with cols[n_row % N_cards_per_row]:
            if n_row == 0:  # Add gold crown emoji and golden border to the first card
                st.markdown('<style>div.stButton > button:first-child {border: 2px solid gold;}</style>', unsafe_allow_html=True)
            
            st.subheader(f"{row['요금제명']}")
            st.text(f"Rank: {row['순위']}")
            st.text(f"Monthly Data (GB): {row['월 데이터 (GB)']}")
            st.text(f"Monthly Fee: {row['월 요금']}₩")
            st.text(f"Data Speed (Mbps): {row['데이터 속도 (Mbps)']}")
            st.text(f"Call Minutes: {row['전화']} mins")
            st.text(f"SMS: {row['문자']} messages")
            st.markdown('<style>.css-1aumxhk {border: 1px solid #ccc; border-radius: 5px; padding: 10px;}</style>', unsafe_allow_html=True)

# If there is no search query, display the entire dataframe
else:
    for n_row, row in sorted_df.iterrows():
        i = n_row % N_cards_per_row
        if i == 0:
            st.write("---")  # Separator line between rows of cards
            cols = st.columns(N_cards_per_row, gap="large")
        
        with cols[n_row % N_cards_per_row]:
            if n_row == 0:  # Add gold crown emoji to the first card
                st.markdown('👑')
            
            st.subheader(f"{row['요금제명']}")
            st.text(f"Rank: {row['순위']}")
            st.text(f"Monthly Data (GB): {row['월 데이터 (GB)']}")
            st.text(f"Monthly Fee: {row['월 요금']}₩")
            st.text(f"Data Speed (Mbps): {row['데이터 속도 (Mbps)']}")
            st.text(f"Call Minutes: {row['전화']} mins")
            st.text(f"SMS: {row['문자']} messages")
            st.markdown('<style>.css-1aumxhk {border: 1px solid #ccc; border-radius: 5px; padding: 10px;}</style>', unsafe_allow_html=True)
