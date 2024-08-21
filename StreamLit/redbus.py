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

curr.execute("SELECT * FROM redbus_data.bus_routes")
data = curr.fetchall()
column_names = [desc[0] for desc in curr.description]
df = pd.DataFrame(data, columns=column_names)

if menu == 'States':
    st.header("States")
    for i in df['States'].unique():
        st.write(i)


elif menu == 'Bus Selection':

    st.header("Bus Routes")
    c1, c2, c3 = st.columns(3)


    with c1:

        select_routes = st.selectbox("Select the Route", df['Routes_Name'].unique())

    with c2:

        select_type = st.selectbox("Select the Type", ['Sleeper', 'Seater', 'All'])

        if select_type == 'Sleeper':
            filtered_data = df[df['Bus_Type'].str.contains('Sleeper', case=False, na=False)]
        elif select_type == 'Seater':
            filtered_data = df[df['Bus_Type'].str.contains('Seater|PUSH BACK', case=False, na=False, regex=True)]
        elif select_type == 'All':
            filtered_data = df

    with c3:

        select_fare = st.selectbox("Select the Fare",['0-500','500-1000','1000+'])

        if select_fare == '0-500':
            filtered_data = filtered_data[ ( filtered_data['Price'] >= 0 ) & ( filtered_data['Price'] <=500 ) ]
        elif select_fare == '500-1000':
            filtered_data = filtered_data[ ( filtered_data['Price'] > 500 ) & ( filtered_data['Price'] <=1000 ) ]
        elif select_fare == '1000+':
            filtered_data = filtered_data[ ( filtered_data['Price'] > 1000 )]


    c4, c5 = st.columns(2)

    with c4:

        select_rating = st.selectbox("Rating",['0-3','3-4','4-5', 'All'])

        if select_rating == '0-3':
            filtered_data = filtered_data[ ( filtered_data['Star_Rating'] >= 0 ) & ( filtered_data['Star_Rating'] <= 3 ) ]
        elif select_rating == '3-4':
            filtered_data = filtered_data[ ( filtered_data['Star_Rating'] > 3 ) & ( filtered_data['Star_Rating'] <= 4 ) ]
        elif select_rating == '4-5':
            filtered_data = filtered_data[ ( filtered_data['Star_Rating'] > 4 ) & ( filtered_data['Star_Rating'] <= 5 ) ]
        elif select_rating == 'All':
            filtered_data = filtered_data

    with c5:

        ac_type = st.radio("A/C Type", ['A/C', 'NON A/C', 'All'])

        if ac_type == 'A/C':
            filtered_data = filtered_data[ filtered_data['Bus_Type'].apply( lambda x:("A/C" in x or "A.C" in x) and not ("Non A/C" in x or "NON A/C" in x) ) ]
        elif ac_type == 'NON A/C':
            filtered_data = filtered_data[ filtered_data['Bus_Type'].apply(lambda x: "Non A/C" in x or "NON A/C" in x or "NON-AC" in x) ]
        elif ac_type == 'All':
            filtered_data = filtered_data


    filtered_data = filtered_data[filtered_data['Routes_Name'] == select_routes]

    st.write(filtered_data[['Routes_Name', 'Bus_Name', 'Bus_Type', 'Price', 'Star_Rating', 'Seat_Availability','Duration']])

