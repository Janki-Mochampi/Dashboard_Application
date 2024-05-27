from dash import Dash, dcc, html
import requests
from tabs.location_tab import layout as location_layout
from tabs.demographic_tab import layout as demographic_layout
from tabs.peak_hour_tab import layout as peak_hours_layout
from tabs.referrer_tab import layout as referrer_layout
from tabs.device_tab import layout as device_layout
from tabs.summary_tab import layout as summary_layout

app = Dash(__name__)
server = app.server

def fetch_data():
    url = 'http://127.0.0.1:7000/'
    response = requests.get(url)
    data = response.json()
    return data

data = fetch_data()

# Logo image URL
olympics_logo_url = 'https://upload.wikimedia.org/wikipedia/commons/5/5c/Olympic_rings_without_rims.svg'

app.layout = html.Div([
    html.Div([
        html.Img(src=olympics_logo_url, style={'width': '80px', 'height': '80px'}),
        html.H1("FUNOLYMPIC GAMES 2024", style={'margin-left': '10px', 'font-size': '24px'})
    ], style={'display': 'flex', 'align-items': 'center'}),
    dcc.Tabs([
        dcc.Tab(label='Viewership Distribution by Location', children=location_layout(app, data)),
        dcc.Tab(label='Viewership Distribution by Demographic', children=demographic_layout(app, data)),
        dcc.Tab(label='Viewership Distribution by Peak Usage Hours', children=peak_hours_layout(app, data)),
        dcc.Tab(label='Viewership Distribution by Referrer', children=referrer_layout(app, data)),
        dcc.Tab(label='Viewership Distribution by Device', children=device_layout(app, data)),
        dcc.Tab(label='Summary Distribution', children=summary_layout(app, data)),
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)

