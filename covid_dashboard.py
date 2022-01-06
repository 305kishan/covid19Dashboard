import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

import warnings
warnings.filterwarnings('ignore')

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 


url = 'https://raw.githubusercontent.com/datasets/covid-19/main/data/time-series-19-covid-combined.csv'
data = pd.read_csv(url)

def data_prepare(x):    
    data_x = data[data['Country/Region'] == x]
    data_x['Date'] = pd.to_datetime(data_x['Date'])
    data_x = data_x.groupby(["Date"]).agg({"Confirmed":'sum',"Recovered":'sum',"Deaths":'sum'})
    data_x["WeekofYear"]=data_x.index.weekofyear
    data_x["Days Since"]=(data_x.index-data_x.index[0])
    data_x["Days Since"]=data_x["Days Since"].dt.days
    data_x["Active"] = data_x["Confirmed"] - data_x["Recovered"] - data_x["Deaths"]
    
    data_x = data_x.reset_index()  
    data_x.loc[0,"NewCases"] = data_x.loc[0,"Confirmed"]
    data_x.loc[0,"NewRecovered"] = data_x.loc[0,"Recovered"]
    data_x.loc[0,"NewDeaths"] = data_x.loc[0,"Deaths"]
 
    for i in range(1,len(data_x)):
        data_x.loc[i,"NewCases"] = data_x.loc[i,"Confirmed"] - data_x.loc[i-1,"Confirmed"]
        data_x.loc[i,"NewRecovered"] = data_x.loc[i,"Recovered"] - data_x.loc[i-1,"Recovered"]
        data_x.loc[i,"NewDeaths"] = data_x.loc[i,"Deaths"] - data_x.loc[i-1,"Deaths"]
        
    return data_x

#PLOT
def NewCases(data_x,x):
    st.write("Number of New Cases as of ",(data_x["Date"].dt.date).iloc[-1], " is ",data_x["NewCases"].iloc[-1])
    fig = px.bar(data_x, x='Date', y='NewCases',color='NewCases', height=500)
    fig.update_layout(title='New Cases in '+x,xaxis_title="Date",yaxis_title="New Cases")
    st.plotly_chart(fig)

def Confirmed(data_x,x):
    st.write("Number of Confirmed Cases as of ",(data_x["Date"].dt.date).iloc[-1], " is ",data_x["Confirmed"].iloc[-1])
    fig = px.bar(data_x, x='Date', y='Confirmed',color='Confirmed', height=500)
    fig.update_layout(title='Confirmed Cases in '+x,xaxis_title="Date",yaxis_title="Confirmed Cases")
    st.plotly_chart(fig)
    
def Recovered(data_x,x):
    st.write("Number of Recovered Cases as of ",(data_x["Date"].dt.date).iloc[-1], " is ",data_x["Recovered"].iloc[-1])
    fig = px.bar(data_x, x='Date', y='Recovered',color='Recovered',template='plotly_white', height=500)
    fig.update_layout(title='Recovered Cases in'+x,xaxis_title="Date",yaxis_title="Recovered Cases")
    st.plotly_chart(fig)
    
def NewRecovered(data_x,x):
    st.write("Number of New Recovered Cases as of ",(data_x["Date"].dt.date).iloc[-1], " is ",data_x["NewRecovered"].iloc[-1])
    fig = px.bar(data_x, x='Date', y='NewRecovered',color='NewRecovered',template='plotly_white', height=500)
    fig.update_layout(title='New Recovered Cases in'+x,xaxis_title="Date",yaxis_title="NewRecovered Cases")
    st.plotly_chart(fig)

def Active(data_x,x):
    st.write("Number of Active Cases as of ",(data_x["Date"].dt.date).iloc[-1], " is ",data_x["Active"].iloc[-1])
    fig = px.bar(data_x, x='Date', y='Active',color='Active',template='plotly_white', height=500)
    fig.update_layout(title='Active Cases in'+x,xaxis_title="Date",yaxis_title="Active Cases")
    st.plotly_chart(fig)

def Deaths(data_x,x):
    st.write("Number of Deaths as of ",(data_x["Date"].dt.date).iloc[-1], " is ",data_x["Deaths"].iloc[-1])
    fig = px.bar(data_x, x='Date', y='Deaths',color='Deaths',template='plotly_white', height=500)
    fig.update_layout(title='Deaths in'+x,xaxis_title="Date",yaxis_title="Deaths")
    st.plotly_chart(fig)
    
def NewDeaths(data_x,x):
    st.write("Number of New Deaths as of ",(data_x["Date"].dt.date).iloc[-1], " is ",data_x["NewDeaths"].iloc[-1])
    fig = px.bar(data_x, x='Date', y='NewDeaths',color='NewDeaths',template='plotly_white', height=500)
    fig.update_layout(title='New Deaths in'+x,xaxis_title="Date",yaxis_title="New Deaths")
    st.plotly_chart(fig)

def Compare(data_x,x):
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=data_x['Date'], y=data_x["Confirmed"],mode='lines+markers',name='Confirmed Cases'))
    fig.add_trace(go.Scatter(x=data_x['Date'], y=data_x["Recovered"],mode='lines+markers',name='Recovered Cases'))
    fig.add_trace(go.Scatter(x=data_x['Date'], y=data_x["Active"],mode='lines+markers',name='Active Cases'))
    fig.add_trace(go.Scatter(x=data_x['Date'], y=data_x["Deaths"],mode='lines+markers',name='Death Cases'))
    fig.update_layout(title="Confirmed vs Recovered vs Active vs Deaths due to CORONA")
    st.plotly_chart(fig)

def Compare2(data_x,x):
    fig=go.Figure(data=go.Pie(labels=['Active','Recovered','Deaths'],
                values=[data_x.iloc[data_x['Date'].idxmax(axis=1)]['Active'],
                        data_x.iloc[data_x['Date'].idxmax(axis=1)]['Recovered'],
                        data_x.iloc[data_x['Date'].idxmax(axis=1)]['Deaths']
                       ]),layout={'template':'presentation'})
    fig.update_layout(title_text="Coronavirus Cases in "+x+" as of "+data_x['Date'].max().strftime("%d-%b'%y"))
    st.plotly_chart(fig)


def sidebarfunction(): #CREATING A BAR NAVIGATION FORM
    st.sidebar.markdown("<hr>", unsafe_allow_html=True)
    link1 = '[covid19Dashboard Repository](https://github.com/305kishan/covid19Dashboard)'
    link2 = '[How it works?](https://github.com/305kishan/covid19DashboardmovieXplore/blob/main/README.md)'
    st.sidebar.markdown(link1, unsafe_allow_html=True)
    st.sidebar.markdown(link2, unsafe_allow_html=True)
    st.sidebar.markdown("<hr>", unsafe_allow_html=True)
    st.sidebar.write("Reach Me Here!")
    link = '[GitHub](https://github.com/305kishan)'
    st.sidebar.markdown(link, unsafe_allow_html=True)
    link = '[Kaggle](https://www.kaggle.com/kishan305)'
    st.sidebar.markdown(link, unsafe_allow_html=True)
    link = '[LinkedIn](https://www.linkedin.com/in/305kishan/)'
    st.sidebar.markdown(link, unsafe_allow_html=True)
    st.sidebar.markdown("<hr>", unsafe_allow_html=True)

def main():
    
    st.title("COVID-19 Dashboard")
    st.markdown("---")
    st.error('For some Countries you might notice some fields are incorrectly showing 0, this is due to db is updated at different time in different countries.')

    x = st.text_input("Enter Country Name. (View COuntries Names in sidebar)",'India')
    y = data_prepare(x)
    z = data['Country/Region'].to_list()
    z = np.unique(z).tolist()
    
    if st.sidebar.button("Show All Countries Names"):
        st.sidebar.write(z)
    sidebarfunction()
    
    Compare(y, x)
    Compare2(y,x)
    
    Confirmed(y, x)
    NewCases(y, x)
    
    Recovered(y, x)
    NewRecovered(y, x)
    
    Active(y, x)
    
    Deaths(y, x)
    NewDeaths(y, x)
    
    
if __name__=="__main__":
    main()
