
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

app = dash.Dash(__name__)


app.title = "Automobile Statistics Dashboard"

dropdown_options = [{'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}]

year_list = [i for i in range(1980, 2024, 1)]


app.layout =html.Div([html.H1("Automobile Sales Statistics Dashboard",style={'textAlign':'center','color':'#503d36','font-size':24}),
            html.Div([html.Label("Select Statistics:",style={'margin-right': '2em'}), 
            dcc.Dropdown(
                id='dropwdown-statistics',
                options=dropdown_options,
                value='Select Statistics',
                placeholder="Select a report type",
                style={'textAlign':'center','width':'80%','font-size':'20px','padding':'3px'})]),
             
            html.Div(dcc.Dropdown(id='select-year',
                options=[{'label': i, 'value': i} for i in year_list],
                value='select-year',
                placeholder="Select a Year",
                style={'textAlign':'center','width':'80%','font_size':'20px','padding':'3px'})),

            html.Div([html.Div(id='output-container', className='chart-grid', style={'display':'flex'}),])])

@app.callback(Output(component_id='select-year', component_property='disabled'),
            Input(component_id='dropwdown-statistics',component_property='value'))

def update_input_container(selected_statistics):
    if selected_statistics =='Yearly Statistics': 
        return False
    else: 
        return True

@app.callback(Output(component_id='output-container', component_property='children'), 
            [Input(component_id='dropwdown-statistics', component_property='value'), Input(component_id='select-year', component_property='value')])

def update_output_container(selected_statistics, input_year):
    if selected_statistics == 'Recession Period Statistics':
        recession_data = data[data['Recession'] == 1]

        yearly_rec=recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(figure=px.line(yearly_rec, x='Year', y='Automobile_Sales', title="Average Automobile Sales fluctuation over Recession Period"))
    
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()                           
        R_chart2  = dcc.Graph(figure=px.bar(average_sales,x='Vehicle_Type', y='Automobile_Sales', title="Average Number of Vehicles sold by Type"))
    
        exp_rec= recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(figure=px.pie(exp_rec,values='Advertising_Expenditure', names='Vehicle_Type', title="Expenditure share by Vehicle Type during Recessions"))     
    
        unemployment_effect= recession_data.groupby(['Vehicle_Type','unemployment_rate'])['Automobile_Sales'].mean().reset_index()
        R_chart4  = dcc.Graph(figure=px.bar(unemployment_effect,x='unemployment_rate', y='Automobile_Sales', title="Effect of Unemployment Rate on Vehicle Type and Sales"))
    
        return [html.Div(className='chart_item', children=[html.Div(children=R_chart1),html.Div(children=R_chart2)],style={'display':'flex'}), 
            html.Div(className='chart-item', children=[html.Div(children=R_chart3),html.Div(children=R_chart4)],style={'display':'flex'})]            

    elif (input_year and selected_statistics=='Yearly Statistics') :
        yearly_data = data[data['Year'] == input_year]              
                              
        yas= data.groupby('Year')['Automobile_Sales'].mean().reset_index() 
        Y_chart1 = dcc.Graph(figure=px.line(yas, x='Year', y='Automobile_Sales', title="Yearly Automobile Sales"))
    
        Y_chart2 = dcc.Graph(figure=px.line(yearly_data,x='Month', y='Automobile_Sales', title="Total Monthly Automobile sales"))
    
        avr_vdata=yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(figure=px.bar(avr_vdata, x='Vehicle_Type', y='Automobile_Sales', title="Average Vehicles Sold by Vehicle Type in the year {}".format(input_year)))    
    
        exp_data=yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(figure=px.pie(exp_data, values='Advertising_Expenditure', names='Vehicle_Type', title="Total Advertising Expenditure for each vehicle type"))

        return [html.Div(className='chart_item', children=[html.Div(children=Y_chart1),html.Div(children=Y_chart2)],style={'display':'flex'}),
                html.Div(className='chart_item', children=[html.Div(children=Y_chart3),html.Div(children=Y_chart4)],style={'display':'flex'})]
    
    else:
        return None

    if __name__ == '__main__':
        app.run_server(debug=True)


