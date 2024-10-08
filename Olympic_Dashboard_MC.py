import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import matplotlib.pyplot as plt

## hui 
st.set_page_config(layout="wide")
st.title("Map - Medals per Year per Country")

col1, col2, col3 = st.columns(3)

data = pd.read_csv('C:/Users/CookeM/OneDrive - NHS/HSMA/Module 7 - GIT/23 - Web apps/h6_7b_web_apps_1-main/exercises/exercise_3/medals_per_country_per_year.csv')
with col1: selected_games_year = st.multiselect("Select Year", options=data["Year"].unique())
with col2: selected_games_Country = st.multiselect("Select Country", options=data["Country"].unique())
with col3: selected_games_NOC = st.multiselect("Select NOC", options=data["NOC"].unique())
min_score, max_score = st.slider("Medal Range", min_value=0, max_value=230, value=(0, 230))


if selected_games_year:
    filtered_data = data[data["Year"].isin(selected_games_year)]
else:
    filtered_data = data

if selected_games_Country:
    filtered_data = filtered_data[filtered_data["Country"].isin(selected_games_Country)]

if selected_games_NOC:
    filtered_data = filtered_data[filtered_data["NOC"].isin(selected_games_NOC)]

if min_score:
    filtered_data = filtered_data[(filtered_data["Total"] >= min_score) & (filtered_data["Total"] <= max_score)]

st.dataframe(filtered_data,
    use_container_width=True,
    column_config={
        "Year": st.column_config.NumberColumn(
            "Year of Game",
            format = "%f" #float
        )
    })

fig, ax = plt.subplots()
for country in filtered_data['Country'].unique():
    country_data = filtered_data[filtered_data['Country'] == country]
    ax.plot(country_data['Year'], country_data['Total'], label=country)

ax.set_xlabel('Year')
ax.set_ylabel('Total')
ax.set_title('Total by Year and Country')
#ax.legend(title='Country')
ax.legend(title='Country', loc='upper center', bbox_to_anchor=(0.5, -0.1), fontsize='small', ncol=10)

# Display the plot in Streamlit
st.pyplot(fig)



st.write("Map shows the total number of medals earned per country in selected year")
geo_data = gpd.read_file('C:/Users/CookeM/OneDrive - NHS/HSMA/Module 7 - GIT/23 - Web apps/h6_7b_web_apps_1-main/exercises/exercise_3/countries_outlines.geojson')

#years = data['Year'].unique()
#selected_year = st.slider('Select Year', min_value=int(years.min()), max_value=int(years.max()), value=int(years.min()))

years = data['Year'].unique()
selected_year = st.selectbox('Select Year', years)

def create_map(year):
    # Filter the data for the selected year
    year_data = data[data['Year'] == selected_year]
    
    # Merge geo_data with year_data
    merged_data = geo_data.merge(year_data, how='left', left_on='name', right_on='Country')
    
    # Create a Folium map
    m = folium.Map(location=[geo_data.geometry.centroid.y.mean(), geo_data.geometry.centroid.x.mean()], zoom_start=1,min_zoom=1)
    
    # Create a Choropleth map
    folium.Choropleth(
        geo_data=merged_data,
        data=merged_data,
        columns=['Country', 'Total'],
        key_on='feature.properties.name',  # Adjust this if your geo_data has a different property name
        fill_color='YlGn',  # You can choose other color scales as well
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Total'
    ).add_to(m)
    
    return m

# Create the map for the selected year
map_for_selected_year = create_map(selected_year)

# Display the map in Streamlit
st_folium(map_for_selected_year, width=700, height=500)
