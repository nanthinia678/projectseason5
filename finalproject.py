# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 05:35:08 2020

@author: ELCOT
"""

import pandas as pd
import webbrowser
import dash
import dash_html_components as html
from dash.dependencies import Input, Output 
import dash_core_components as dcc 
import plotly.graph_objects as go
import plotly.express as px 
from dash.exceptions import PreventUpdate

app = dash.Dash(__name__)
    
def load_data():
    dataset_name="global_terror.csv"
    
    global df
    df=pd.read_csv(dataset_name)
    
    global month_list
    month = {
        "January" :1,
        "February" :2,
        "March": 3,
        "April": 4,
        "May" :5,
        "June" :6,
        "July" :7,
        "August" :8,
        "September" :9,
        "October" :10,
        "November" :11,
        "December" :12
        }
    
    
    month_list=[{"label":key,"value":values} for key,values in month.items()]
    global date_list
    date_list=[x for x in range(1,32)]
    
    global region_list
    region_list = [{"label": str(i), "value": str(i)}  for i in sorted( df['region_txt'].unique().tolist() ) ]
  
    global country_list
    country_list = df.groupby("region_txt")["country_txt"].unique().apply(list).to_dict()
    print(country_list)
  
    global state_list
    state_list = df.groupby("country_txt")["provstate"].unique().apply(list).to_dict()

    global city_list
    city_list  = df.groupby("provstate")["city"].unique().apply(list).to_dict()

  
    global attack_type_list
    attack_type_list=[{"label":str(i),"value":str(i)} for i in df['attacktype1_txt'].unique().tolist()]
    
    global year_list
    year_list=sorted(df['iyear'].unique().tolist())
    
    global year_dict
    year_dict={str(year): str(year) for year in year_list}
            
    global chart_dropdown_values
    chart_dropdown_values = {"Terrorist Organisation":'gname', 
                             "Target Nationality":'natlty1_txt', 
                             "Target Type":'targtype1_txt', 
                             "Type of Attack":'attacktype1_txt', 
                             "Weapon Type":'weaptype1_txt', 
                             "Region":'region_txt', 
                             "Country Attacked":'country_txt'
                          }
                              
    chart_dropdown_values = [{"label":keys, "value":value} for keys, value in chart_dropdown_values.items()]
      


def open_browser():
  # Open the default web browser
  webbrowser.open_new('http://127.0.0.1:8050/')

def create_app_ui():
  # Create the UI of the Webpage here
  main_layout = html.Div(
       style={
          'margin':'-10px -10px',
          'padding':'0px',
          'background-image':'linear-gradient(rgba(0, 0, 0, 0.4),rgba(0, 0, 0, 0.7)),url(https://www.vision.org/sites/default/files/img/vision_sr_what-is-terrorism_1920x1080.jpg)',
          'background-size': 'cover',
          'opacity':'0.9'
          },children=[
      html.Img(src='/assets/title.png',
                 style={'width':'2000px','hight':'150px'}),
    
      dcc.Tabs(id="Tabs", value="Map",children=[
          dcc.Tab(label="Map tool" ,id="Map tool",value="Map",
                  style={
                          'textAlign':'center',
                          'color':'blue',
                          'font-family':'Times New Roman'
                          
                          },children=[
              dcc.Tabs(id = "subtabs", value = "WorldMap",
                       style={
                          'color':'blue',
                          'font-family':'Times New Roman',
                          'textAlign':'center'
                          },children = [
                  dcc.Tab(label="World Map tool", id="World", value="WorldMap",
                          style={
                          'textAlign':'center',
                          'color':'blue',
                          'font-family':'Times New Roman',
                          }),
                  dcc.Tab(label="India Map tool", id="India", value="IndiaMap",
                          style={
                          'textAlign':'center',
                          'color':'blue',
                          'font-family':'Times New Roman',
                          })
                ], colors={
                            "border": "blue",
                            "primary": "silver",
                            "background": "cornsilk"
                        }),
                    html.Br(),
                    html.H2('Search through dropdown list', id='dropdown-title',style={'color':'white','text-align':'center'}),html.Br(),
                        dcc.Dropdown(
                        id='month',
                        options=month_list,multi=True,
                        placeholder='Select Month',
                        style={
                          'textAlign':'center',
                          'color':'green',
                          'font-family':'Times New Roman',
                          'width':'45vw',
                    'display':'inline-block',
                    'margin':'5px 24px'
                          }),
                    
                  dcc.Dropdown(
                        id='date',multi=True,
                        placeholder='Select Date',
                        style={
                          'textAlign':'center',
                          'color':'green',
                          'font-family':'Times New Roman',
                          'width':'45vw',
                    'display':'inline-block',
                    'margin':'5px 24px'
                          }),
                    
                  dcc.Dropdown(
                        id='region',multi=True,
                        options=region_list,
                        placeholder='Select region',
                        style={
                          'textAlign':'center',
                          'color':'green',
                          'font-family':'Times New Roman',
                          'width':'45vw',
                    'display':'inline-block',
                    'margin':'5px 24px'
                          }),
                    
                  dcc.Dropdown(
                        id='country',multi=True,
                        options=[{'label':'All','value':'All'}],
                        placeholder='Select country',
                        style={
                          'textAlign':'center',
                          'color':'green',
                          'font-family':'Times New Roman',
                          'width':'45vw',
                    'display':'inline-block',
                    'margin':'5px 24px'
                          }),
                    
                  dcc.Dropdown(
                        id='state',multi=True,
                        options=[{'label':'All','value':'All'}],
                        placeholder='Select State or province',
                        style={
                          'textAlign':'center',
                          'color':'green',
                          'font-family':'Times New Roman',
                          'width':'45vw',
                    'display':'inline-block',
                    'margin':'5px 24px'
                          }),
                  dcc.Dropdown(
                        id='city',multi=True,
                        options=[{'label':'All','value':'All'}],
                        placeholder='Select city',
                        style={
                          'textAlign':'center',
                          'color':'green',
                          'font-family':'Times New Roman',
                          'width':'45vw',
                    'display':'inline-block',
                    'margin':'5px 24px'
                          }),
                  html.Br(),
                   
                  dcc.Dropdown(
                        id='attacktype',multi=True,
                        options=attack_type_list,
                        placeholder='Select Attack Type',
                        style={
                          'textAlign':'center',
                          'color':'green',
                          'font-family':'Times New Roman',
                           'width':'45vw',
                           'margin':'5px 24px',
                           'display':'inline-block'
                    
                          }),
                    
             html.H2('Use the year slider for searching in map with the particular range period', id='year_title1',
                     style={'text-align':'center','color':'skyblue',
                            'textAlign':'center',
                          
                          'font-family':'Times New Roman',
                         }),
                    
                  dcc.RangeSlider(id='year_slider',
                               min=min(year_list),
                               max=max(year_list),
                               value=[min(year_list),max(year_list)],
                               marks=year_dict,step=None,
                               ),                 
                 html.Br()
                
              ]),
          dcc.Tab(label = "Chart Tool", id="chart tool", value="Chart",
                  style={
                          'textAlign':'center',
                          'color':'blue',
                          'font-family':'Times New Roman',
                          },children=[
              dcc.Tabs(id = "subtabs2", value = "WorldChart",children = [
                  dcc.Tab(label="World Chart tool", id="WorldC",style={
                          'textAlign':'center',
                          'color':'blue',
                          'font-family':'Times New Roman',
                          }, value="WorldChart"),
                  dcc.Tab(label="India Chart tool", id="IndiaC",
                          style={
                          'textAlign':'center',
                          'color':'blue',
                          'font-family':'Times New Roman',
                          },value="IndiaChart")],
                  colors={
                            "border": "blue",
                            "primary": "silver",
                            "background": "cornsilk"
                        }),
              html.Br(),html.Br(),html.Br(),                
              html.H1('Select The Dropdown List',id='filter',style={'color':'white',
                             'display':'inline-block',
                             'margin-left':'400px',
                             }),
                
              dcc.Dropdown(id="Chart_Dropdown", options = chart_dropdown_values, 
                                   placeholder="Select option", value = "region_txt",
                                   style={
                          'textAlign':'center',
                          'color':'green',
                          'font-family':'Times New Roman',
                          'width':'25vw',
                             'display':'inline-block',
                             'margin-left':'10px',
                             
                          }), 
                      html.Br(),
                      html.Br(),
                      html.Hr(),
                     
                      dcc.Input(id="search", placeholder="Search Filter",
                                style={
                            'color':'green',
                          'font-family':'Times New Roman',
                          'font-size':'20px',
                            ' width':'40vw',
                            'padding':'15px',
                            'border':'none',
                            'border-radius':'10px',
                            'margin-left':'900px',
                            'text-align':'center',
                            'margin-right':'500px'
                          }),
                      html.Hr(),
                      html.Br(),
                      html.H2('Use the year slider for searching in map with the particular range period', id='year_title',
                     style={'text-align':'center','color':'skyblue'}),
                          html.Br(),
                      dcc.RangeSlider(
                        id='cyear_slider',
                        min=min(year_list),
                        max=max(year_list),
                        value=[min(year_list),max(year_list)],
                        marks=year_dict,
                        step=None
                          ),
                      html.Br()
                      ]),
                  
                  ]),
          
      html.Div(id = "graph_object", children ="Graph will be shown here",
      style={
          'textAlign':'center',
          'font-family':'Comic Sans MS',
          'padding-top':'20px',
          'font-size':'30px',
          'color':'white'
          })
    ])
        
  return main_layout

@app.callback(
        dash.dependencies.Output('graph_object','children'),
        [
             dash.dependencies.Input("Tabs","value"),
             dash.dependencies.Input('month','value'),
             dash.dependencies.Input('date','value'),
             dash.dependencies.Input('region','value'),
             dash.dependencies.Input('country','value'),
             dash.dependencies.Input('state','value'),
             dash.dependencies.Input('city','value'),
             dash.dependencies.Input('attacktype','value'),
             dash.dependencies.Input('year_slider','value'),
             dash.dependencies.Input('cyear_slider','value'),
             
             dash.dependencies.Input("Chart_Dropdown","value"),
             dash.dependencies.Input("search","value"),
             dash.dependencies.Input("subtabs2","value")
                
         ])

def update_graph_ui(Tabs,month_value,date_value,region_value,country_value,state_value,city_value,
                    attack_value,year_value,chart_year_selector,chart_dp_value,search,subtabs2):
    fig=None
    
    if Tabs=="Map":       
        print("Data Type of month value= ",str(type(month_value)))
        print("Data of month value= ",month_value)
        
        print("Data Type of Day value= ",str(type(date_value)))
        print("Data of Day value= ",date_value)
        
        print("Data Type of region value= ",str(type(region_value)))
        print("Data of region value= ",region_value)
        
        print("Data Type of country value= ",str(type(country_value)))
        print("Data of country value= ",country_value)
        
        print("Data Type of state value= ",str(type(state_value)))
        print("Data of state value= ",state_value)
        
        print("Data Type of city value= ",str(type(city_value)))
        print("Data of city value= ",city_value)
        
        print("Data Type of attack type value= ",str(type(attack_value)))
        print("Data of attack type value= ",attack_value)
    
        print("Data Type of year value= ",str(type(year_value)))
        print("Data of year value= ",year_value)
        
        year_range=range(year_value[0],year_value[1]+1)
        new_df=df[df["iyear"].isin(year_range)]
        
        if month_value==[] or month_value is None:
            pass
        else:
            if date_value==[] or date_value is None:
                new_df=new_df[new_df["imonth"].isin(month_value)]
                
            else:
                new_df=new_df[(new_df["imonth"].isin(month_value))
                          &   (new_df["iday"].isin(date_value))  ]
        
    
        if region_value==[] or region_value is None:
            pass
        else:
            if country_value==[] or country_value is None:
                new_df=new_df[new_df["region_txt"].isin(region_value)]
            else:
                if state_value==[] or state_value is None:
                     new_df=new_df[(new_df["region_txt"].isin(region_value))&
                                   (new_df["country_txt"].isin(country_value))]
                else:
                    if city_value==[] or city_value is None:
                        new_df=new_df[(new_df["region_txt"].isin(region_value))&
                            (new_df["country_txt"].isin(country_value)) & 
                            (new_df["provstate"].isin(state_value))]
                    else:
                        new_df=new_df[(new_df["region_txt"].isin(region_value))&
                            (new_df["country_txt"].isin(country_value)) & 
                            (new_df["provstate"].isin(state_value)) &
                            (new_df["city"].isin(city_value))]
                        
                            
        if attack_value==[] or attack_value is None:
            pass
        else:
            new_df=new_df[new_df["attacktype1_txt"].isin(attack_value)]
        mapFigure=go.Figure()    
        if new_df.shape[0]:
            pass
        else:
            new_df=pd.DataFrame(columns=['iyear','imonth','iday','country_txt',
                                         'region_txt',
                                              'provstate','city','latitude','longitude',
                                              'attacktype1_txt','nkill'])
            new_df.loc[0]=[0,0,0,None,None,None,None,None,None,None,None]                   
        mapFigure = px.scatter_mapbox(new_df,
          lat="latitude", 
          lon="longitude",
          color="attacktype1_txt",
          hover_name="city", 
          hover_data=["region_txt", "country_txt", "provstate","city", "attacktype1_txt","nkill","iyear","imonth", "iday"],
          zoom=1
          )                       
        mapFigure.update_layout(mapbox_style="carto-positron",
          autosize=True,
          margin=dict(l=0, r=0, t=25, b=20),
          )
          
        fig = mapFigure

    elif Tabs=="Chart":
        fig = None
        
        year_range_c = range(chart_year_selector[0], chart_year_selector[1]+1)
            
        chart_df = df[df["iyear"].isin(year_range_c)]
            
        if subtabs2 == "WorldChart":
            pass
        elif subtabs2== "IndiaChart":
            chart_df=chart_df[(chart_df["region_txt"]=="South Asia")&(chart_df["country_txt"]=="India")]
            
        if chart_dp_value is not None:
            if search is not None: 
               chart_df = chart_df.groupby("iyear")[chart_dp_value].value_counts().reset_index(name = "count")
               chart_df  = chart_df[chart_df[chart_dp_value].str.contains(search, case = False)]
            else:
               chart_df = chart_df.groupby("iyear")[chart_dp_value].value_counts().reset_index(name="count")
                
        if chart_df.shape[0]:
           pass
        else: 
           chart_df = pd.DataFrame(columns = ['iyear', 'count', chart_dp_value])
           chart_df.loc[0] = [0, 0,"No data"]
                           
        fig = px.area(chart_df, x= "iyear", y ="count", color = chart_dp_value)
      
    return dcc.Graph(figure = fig)

@app.callback(
  Output("date", "options"),
                [Input("month", "value")])
def update_date(month):
    option = []
    if month:
        option= [{"label":m, "value":m} for m in date_list]
    return option

@app.callback([Output("region", "value"),
               Output("region", "disabled"),
               Output("country", "value"),
               Output("country", "disabled")],
              [Input("subtabs", "value")])
def update_r(tab):
    region = None
    disabled_r = False
    country = None
    disabled_c = False
    if tab == "WorldMap":
        pass
    elif tab=="IndiaMap":
        region = ["South Asia"]
        disabled_r = True
        country = ["India"]
        disabled_c = True
    return region, disabled_r, country, disabled_c

@app.callback(
    Output('country', 'options'),
    [Input('region', 'value')])
def set_country_options(region_value):
    option = []
    # Making the country Dropdown data
    if region_value is  None:
        raise PreventUpdate
    else:
        for var in region_value:
            if var in country_list.keys():
                option.extend(country_list[var])
    return [{'label':m , 'value':m} for m in option]


@app.callback(
    Output('state', 'options'),
    [Input('country', 'value')])
def set_state_options(country_value):
  # Making the state Dropdown data
    option = []
    if country_value is None :
        raise PreventUpdate
    else:
        for var in country_value:
            if var in state_list.keys():
                option.extend(state_list[var])
    return [{'label':m , 'value':m} for m in option]
@app.callback(
    Output('city', 'options'),
    [Input('state', 'value')])
def set_city_options(state_value):
  # Making the city Dropdown data
    option = []
    if state_value is None:
        raise PreventUpdate
    else:
        for var in state_value:
            if var in city_list.keys():
                option.extend(city_list[var])
    return [{'label':m , 'value':m} for m in option]
 
def main():
    
      load_data()
      open_browser()
      layout=html.Div()

      global app
      app.layout = create_app_ui()
      # go to https://www.favicon.cc/ and download the ico file and store in assets directory 
      app.title="Terrorism Analysis with Insights"
      app.run_server() # debug=True
    
      print("This would be executed only after the script is closed")
      df = None
      app = None
      
if __name__ == '__main__':
    main()