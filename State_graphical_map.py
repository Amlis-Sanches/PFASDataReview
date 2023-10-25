import pandas as pd
import os
import plotly.express as px
import dash
import dash_core_components as doc
import dash_html_components as html
from dash.dependencies import Input, Output

#Check if imorted file exists before reading it. 
filename = "State_Summary.csv"

if not os.path.exists(filename):
    # If it doesn't exist, run another Python script
    os.system("Data_Evaluation.py")

df = pd.read_csv(r'C:\Users\natha\Documents\Coding\PFASDataReview\State_Summary.csv')



app = dash.Dash(__name__)

app.layout = html.Div([
    doc.Graph(id='map', figure=fig)
])

if __name__ == '__main__':
    app.run_server(debug=True)