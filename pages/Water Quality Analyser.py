import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings


st.set_page_config(page_title="Your WaterQuality dashboard",layout="wide")

st.title(" :bar_chart: Your WaterQuality dashboard")

df = pd.read_csv("water_data.csv")

col1, col2 = st.columns((2))


# Getting the min and max date 
# startDate = (df["Order Date"]).min()
# endDate = (df["Order Date"]).max()

# with col1:
#     date1 = pd.to_datetime(st.date_input("Start Date", startDate))

# with col2:
#     date2 = pd.to_datetime(st.date_input("End Date", endDate))

# df = df[(df["Order Date"] >= date1) & (df["Order Date"] <= date2)].copy()

st.sidebar.header("Choose your filter: ")
# Select the type
region = st.sidebar.multiselect("Pick your Region", df["Type Water Body"].unique())
if not region:
    df2 = df.copy()
else:
    df2 = df[df["Type Water Body"].isin(region)]

# Create for State
state = st.sidebar.multiselect("Pick the State", df2["State Name"].unique())
if not state:
    df3 = df2.copy()
else:
    df3 = df2[df2["State Name"].isin(state)]

# Create for year
year = st.sidebar.multiselect("Pick the year",df3["Year"].unique())

# Filter the data based on Region, State and City

if not region and not state and not year:
    filtered_df = df
elif not state and not year:
    filtered_df = df[df["Type Water Body"].isin(region)]
elif not region and not year:
    filtered_df = df[df["State Name"].isin(state)]
elif state and year:
    filtered_df = df3[df["State Name"].isin(state) & df3["Year"].isin(year)]
elif region and year:
    filtered_df = df3[df["Type Water Body"].isin(region) & df3["Year"].isin(year)]
elif region and state:
    filtered_df = df3[df["Type Water Body"].isin(region) & df3["State Name"].isin(state)]
elif year:
    filtered_df = df3[df3["Year"].isin(year)]
else:
    filtered_df = df3[df3["Type Water Body"].isin(region) & df3["State Name"].isin(state) & df3["Year"].isin(year)]

category_df = filtered_df.groupby(by = ["State Name"], as_index = False)["Max pH"].sum()

with col1:
    st.subheader("State wise Max pH")
    fig = px.bar(category_df, x = "State Name", y = "Max pH",
                 template = "seaborn")
    st.plotly_chart(fig,use_container_width=True, height = 200)

with col2:
    st.subheader("Water Body wise Max pH")
    fig = px.pie(filtered_df, values = "Max pH", names = "Type Water Body", hole = 0.5)
    fig.update_traces(text = filtered_df["Type Water Body"], textposition = "outside")
    st.plotly_chart(fig,use_container_width=True)

cl1, cl2 = st.columns((2))
with cl1:
    with st.expander("StateWise_ViewData"):
        st.write(category_df.style.background_gradient(cmap="Blues"))
        csv = category_df.to_csv(index = False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name = "Category.csv", mime = "text/csv",
                            help = 'Click here to download the data as a CSV file')

with cl2:
    with st.expander("Waterbody_wise__ViewData"):
        region = filtered_df.groupby(by = "Type Water Body", as_index = False)["Max pH"].sum()
        st.write(region.style.background_gradient(cmap="Oranges"))
        csv = region.to_csv(index = False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name = "Region.csv", mime = "text/csv",
                        help = 'Click here to download the data as a CSV file')
        
# filtered_df["month_year"] = filtered_df["Order Date"].dt.to_period("M")
st.subheader('Time Series Analysis')


linechart = pd.DataFrame(filtered_df.groupby(filtered_df["Year"])["Max pH"].sum()).reset_index()
fig2 = px.line(linechart, x = "Year", y="Max pH", labels = {"Max pH": "Max pH"},height=500, width = 1000,template="gridon")
st.plotly_chart(fig2,use_container_width=True)


# Create a treem based on Region, category, sub-Category
st.subheader("Hierarchical view of Max Temperature using TreeMap")
fig3 = px.treemap(filtered_df, path = ["Type Water Body","State Name","Year"], values = "Max pH",hover_data = ["Max pH"],
                  color = "Year")
fig3.update_layout(width = 800, height = 650)
st.plotly_chart(fig3, use_container_width=True)

chart1, chart2 = st.columns((2))
with chart1:
    st.subheader('Year wise Max temperature')
    fig = px.pie(filtered_df, values = "Max Temperature", names = "Year", template = "plotly_dark")
    fig.update_traces(text = filtered_df["Year"], textposition = "inside")
    st.plotly_chart(fig,use_container_width=True)

with chart2:
    st.subheader('State wise max temperature')
    fig = px.pie(filtered_df, values = "Max Temperature", names = "State Name", template = "gridon")
    fig.update_traces(text = filtered_df["State Name"], textposition = "inside")
    st.plotly_chart(fig,use_container_width=True)

import plotly.figure_factory as ff
st.subheader(":point_right: Year wise State Max Dissolved Oxygen")
with st.expander("Summary_Table"):
    df_sample = df[0:5][["State Name","Type Water Body","Year","Max pH","Max Temperature","Max Dissolved Oxygen"]]
    fig = ff.create_table(df_sample, colorscale = "Cividis")
    st.plotly_chart(fig, use_container_width=True)

    # st.markdown("Year wise Max Dissolved Oxygen Table")
    # sub_category_Year = pd.pivot_table(data = filtered_df, values = "Max Dissolved Oxygen", index = ["Year"],columns = "Year")
    # st.write(sub_category_Year.style.background_gradient(cmap="Blues"))

# Create a scatter plot
data1 = px.scatter(filtered_df, x = "Max Temperature", y = "Max pH")
# data1['Max pH'].update(title="Relationship between Sales and Profits using Scatter Plot.",
#                        titlefont = dict(size=20),xaxis = dict(title="Max pH",titlefont=dict(size=19)),
#                        yaxis = dict(title = "Max BOD", titlefont = dict(size=19)))
st.plotly_chart(data1,use_container_width=True)

with st.expander("View Data"):
    st.write(filtered_df.iloc[:500,1:20:2].style.background_gradient(cmap="Oranges"))

