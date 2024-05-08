"""
Nicole Carella
CS230-4
Rest Area Data set
Link:

Description:
This program shows you the rest stops in your area. It has easy to read dataframes, a bar chart displaying accommodations in each rest stop,
a line chart showing postmiles for each rest stop, and a map labeling each rest stop clearly. There is also an option to leave a review!
"""
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import pydeck as pdk


# reading original data
def read_data():
    path = "C:/Users/nc012/OneDrive/pythonWork/classwork/introPython/finalapp"
    return pd.read_csv(path + "/" + "Rest_Areas.csv")


# filtering data
df = read_data()
# [DA7]
df = df.drop(["X", "Y", "OBJECTID", "CT_NO", "POSTMILE_P", "POSTMILE_S", "DISTRICT"], axis = 1)
# [DA1]
df = df.drop_duplicates("REST_AREA")
print(df)


# Header
st.title("Rest Areas Near You")
st.caption("Find the best rest area for you!")
st.divider()
# [ST4]
st.sidebar.header("Find Your Rest Stop")


# select county drop down code
counties = []
# [DA4]
county_options = df["COUNTY"].unique()
# [DA2]
county_options.sort()
# [PY4]
for county in county_options:
    if county not in counties:
        counties.append(county)
# [ST1]
selected_county = st.sidebar.selectbox("Select the county you are in.", counties)
st.write(f"You are in {selected_county}")


# route selection code
routes = []
route_df = df[df["COUNTY"] == selected_county]
route_options = route_df["ROUTE"].unique()

for route in route_options:
    if route not in routes:
        routes.append(route)
# [ST2]
selected_route = st.sidebar.radio("What route are you on?", routes)
st.write(f"You are on route {selected_route} in {selected_county}")


# review code
# [ST3]
toggle_review = st.sidebar.checkbox("Leave a review?")

if toggle_review:
    st.sidebar.write("Write review below:")
    st.sidebar.text_area("", "Enter review")


# rest area datafram after selected county
# [PY1]
def county_dataFrame(df, county):
    county_df = df[df["COUNTY"] == county][["REST_AREA", "LOCATION", "ADDRESS", "CITY"]]
    return county_df
county = selected_county
st.divider()

county_table = county_dataFrame(df, county)
# [VIZ1]
st.subheader("Rest Areas in Your County")
st.dataframe(county_table)


# accommodations dataframe
# [PY3]
def options_dataFrame(df, county):
    filtered_df = df[df["COUNTY"] == county]
    rest_df = filtered_df[["REST_AREA", "RESTROOM", "WATER", "PHONE", "HANDICAP", "PET_AREA", "VENDING", "PICNICTAB", "RV_STATION"]]
    rest_df = rest_df.set_index("REST_AREA")
    return rest_df

st.divider()

rest_table = options_dataFrame(df, county)
st.subheader("Rest Area Accommodations")
st.dataframe(rest_table)

# accommodations bar chart
# [VIZ2]
st.bar_chart(data= rest_table, x=None, y=("RESTROOM","WATER","PHONE","HANDICAP"))

st.divider()


# post miles line chart
st.subheader("Postmiles for Rest Areas")

# [PY2]
def miles_rest_areas(mile_df):
    # [DA9]
    mile_df["POSTMILE"] = df["POSTMILE"].astype(float)
    mile_df["REST_AREA"] = df["REST_AREA"]
    # [VIZ3]
    st.line_chart(data=mile_df, x="REST_AREA", y="POSTMILE", color=None)

    # [DA3]
    longest = mile_df["POSTMILE"].max()
    shortest = mile_df["POSTMILE"].min()

    st.write(f"The furthest rest stop is {longest} miles away")
    st.write(f"The closest rest stop is {shortest} miles away")

mile_df = options_dataFrame(df,county)
miles_rest_areas(mile_df)

st.divider()


# map of rest areas
# [VIZ1]
st.subheader("Map of the Rest Areas")
def generate_map(df):
    map_df = df.filter(["REST_AREA", "LATITUDE", "LONGITUDE"])

    view_state = pdk.ViewState(latitude=map_df["LATITUDE"].mean(),
                               longgitude=map_df["LONGITUDE"].mean(),
                               zoom=10)
    layer = pdk.Layer('ScatterplotLayer',
                      data=map_df,
                      get_position='[LONGITUDE,LATITUDE]',
                      get_radius=70,
                      get_color=[100, 100, 100])
    tool_tip = {"html": "Rest Area Name:<br/> <b>{REST_AREA}</b>",
            "style": {"backgroundColor": "orange",
                        "color": "white"}}
    map = pdk.Deck(map_style='mapbox://styles/mapbox/outdoors-v11',
                   initial_view_state=view_state,
                   layers=[layer],
                   tooltip=tool_tip)
    st.pydeck_chart(map)

generate_map(df)


