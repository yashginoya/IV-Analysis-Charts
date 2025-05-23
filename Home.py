import pandas as pd
import numpy as np
import plotly.graph_objects as go
import streamlit as st
import os


def make3DGraph(filePath, graphTitle):
    df = pd.read_csv(filePath)

    iv_columns = [col for col in df.columns if 'IV' in col and 'Unnamed' not in col]
    iv_data = df[iv_columns]
    
    # Generate mesh grid
    x_time = np.arange(len(df))
    y_strike = np.arange(len(iv_columns))
    X, Y = np.meshgrid(x_time, y_strike)
    Z = iv_data.T.values

    surface = go.Surface(z=Z, x=X, y=Y, colorscale='Viridis')
    layout = go.Layout(
        title=graphTitle,
        scene=dict(
            xaxis_title='Time',
            yaxis_title='Strike',
            zaxis_title='IV',
            yaxis=dict(
                tickmode='array',
                tickvals=y_strike,
                ticktext=iv_columns
            )
            # aspectmode='cube'
        ),
        autosize=True,
    )

    fig = go.Figure(data=[surface],layout=layout)

    return fig

def get_file_list(folder_path):
    all_files = []
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for file in filenames:
            all_files.append(file)
    
    all_files = np.array(all_files)
    all_files.sort()
    all_files = all_files.tolist()
    return all_files

def main():

    st.set_page_config(layout="wide")

    folder_path = "Output"
    if 'date_list' not in st.session_state:
        st.session_state.date_list = [] 
    if 'textOption' not in st.session_state:
        st.session_state.textOption = [] 

    all_files = get_file_list(folder_path)
    st.session_state.textOption = all_files.copy()

    st.title("Select Date: ")

    def update_text_option():
        if st.session_state.date_select not in st.session_state.date_list:
            st.session_state.date_list.append(st.session_state.date_select)
    
    st.selectbox("Select a Date to Plot:", options=st.session_state.textOption, key="date_select", placeholder="Select Date", on_change=update_text_option)

    st.write("Enter a Date:")
    col1, col2, col3, col_submit, col_clear, extraCol = st.columns([2, 2, 2, 2, 2 ,16])
    
    with col1:
        day = st.text_input("Day", max_chars=2, placeholder="dd", label_visibility="collapsed")
    with col2:
        month = st.text_input("Month", max_chars=2, placeholder="mm", label_visibility="collapsed")
    with col3:
        year = st.text_input("Year", max_chars=4, placeholder="yyyy", label_visibility="collapsed")

    with col_submit:
        if st.button("Submit"):
            if day and month and year:
                date_str = f"{day.zfill(2)}-{month.zfill(2)}-{year}"
                if date_str + ".csv" in st.session_state.textOption:
                    if date_str + ".csv" in st.session_state.date_list:
                        st.warning(f"The date {date_str} is already selected.")
                    else:
                        st.session_state.date_list.append(date_str + ".csv")
                else:
                    st.error(f"The date {date_str} is Invalid. Please check the format and try again.")
            else:
                st.warning("Please fill all date fields before submitting.")

    with col_clear:
        if st.button("Clear Date"):
            st.session_state.date_list = []
            st.session_state.textOption = all_files.copy()

    cols = st.columns(3)

    if st.session_state.date_list:
        for ind in range(len(st.session_state.date_list)):
            date = st.session_state.date_list[ind]
            curr_3d_graph = make3DGraph(filePath="./Output/" + date, graphTitle=date.split(".")[0])
            cols[ind % 3].plotly_chart(curr_3d_graph, use_container_width=True)

if __name__ == "__main__":
    main()
    