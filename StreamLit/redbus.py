import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector as db

st.set_page_config(page_title="Redbus Data", layout='wide')

with st.sidebar:
    st.write("# RedBus Details")

    menu = option_menu(
                
                menu_title = "Select Any",
                options = ["States", "Bus Selection"],
                styles = {
                    "nav-link-selected": {"background-color": "lightred"}
                }
    )

con = db.connect(
    host = "localhost",
    user = "NewUser",
    password = "root",
    database = "redbus_data"
)
curr = con.cursor()

def get_data_from_db(query):
    curr.execute(query)
    data = curr.fetchall()
    column_names = [desc[0] for desc in curr.description]
    return pd.DataFrame(data, columns=column_names)


if menu == 'States':
    st.header("States")
    query = "SELECT DISTINCT States FROM redbus_data.bus_routes"
    df = get_data_from_db(query)
    for state in df['States']:
        st.write(state)


elif menu == 'Bus Selection':
    st.header("Bus Routes")

    

    c1, c2, c3 = st.columns(3)


    with c1:
        route_query = "SELECT DISTINCT Routes_Name FROM redbus_data.bus_routes"
        route_df = get_data_from_db(route_query)
        select_routes = st.selectbox("Select the Route", route_df['Routes_Name'])

    with c2:
        # Bus Types
        select_type = st.selectbox("Select the Type", ['Sleeper', 'Seater', 'All'])

    with c3:
        # Bus fare
        select_fare = st.selectbox("Select the Fare",['0-500','500-1000','1000+'])


    c4, c5 = st.columns(2)

    with c4:
        # Bus rating
        select_rating = st.selectbox("Rating",['0-3','3-4','4-5', 'All'])

    with c5:
        # Bus AC Types
        ac_type = st.radio("A/C Type", ['A/C', 'NON A/C', 'All'])


    sql_query = f" SELECT * FROM redbus_data.bus_routes WHERE Routes_Name = '{select_routes}' "

    # Bus Types
    if select_type != 'All':
        if select_type == 'Sleeper':
            sql_query += " AND Bus_Type LIKE '%Sleeper%' "
        elif select_type == 'Seater':
            sql_query += " AND (Bus_Type LIKE '%Seater%' OR Bus_Type LIKE '%PUSH BACK%') "

    # Bus fare
    if select_fare == '0-500':
        sql_query += " AND Price BETWEEN 0 AND 500 "
    elif select_fare == '500-1000':
        sql_query += " AND Price BETWEEN 500 AND 1000 "
    elif select_fare == '1000+':
        sql_query += " AND Price > 1000 "

    # Bus rating
    if select_rating != 'All':
        if select_rating == '0-3':
            sql_query += " AND Star_Rating BETWEEN 0 AND 3 "
        elif select_rating == '3-4':
            sql_query += " AND Star_Rating BETWEEN 3 AND 4 "
        elif select_rating == '4-5':
            sql_query += " AND Star_Rating BETWEEN 4 AND 5 "

    # Bus AC Types
    if ac_type != 'All':
        if ac_type == 'A/C':
            sql_query += """ AND (Bus_Type LIKE '%A/C%' OR Bus_Type LIKE '%A.C%') 
                             AND Bus_Type NOT LIKE '%Non%' 
                             AND Bus_Type NOT LIKE '%NON%' """
            
        elif ac_type == 'NON A/C':
            sql_query += """ AND (Bus_Type LIKE '%Non A/C%' 
                                  OR Bus_Type LIKE '%NON A/C%' 
                                  OR Bus_Type LIKE '%NON-AC%') """

    

    # Execute the final query and get the data
    filtered_data = get_data_from_db(sql_query)

    st.write(filtered_data[['Routes_Name', 'Bus_Name', 'Bus_Type', 'Price', 'Star_Rating', 'Seat_Availability','Duration']])

