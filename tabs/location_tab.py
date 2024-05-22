from dash import dcc, html, Input, Output
import plotly.express as px

def layout(app, data):
    continents = sorted(set(record['Continent'] for record in data))
    countries_by_continent = {continent: sorted(set(record['Country'] for record in data if record['Continent'] == continent)) for continent in continents}

    @app.callback(
        [Output('visualization-output-loc', 'children'),
         Output('additional-visualization-output-loc', 'children')],
        [Input('sport-dropdown', 'value'),
         Input('country-dropdown', 'value')]
    )
    def update_visualization_location(selected_sport, selected_country):
        filtered_data = [record for record in data if (selected_country is None or record['Country'] == selected_country)]
        
        # Choropleth map
        map_fig = px.choropleth(filtered_data, locations='Country', locationmode='country names', color='Viewership', hover_name='Country')
        map_fig.update_layout(title_text='Viewership Distribution by Country', title_x=0.5)
        map_fig.update_geos(showcountries=True)
        
        # Bar chart for viewership by continent
        if selected_sport:
            # Filter data by selected sport
            sport_data = [record for record in filtered_data if record['Sport'] == selected_sport]
            # Recalculate viewership by continent based on filtered data
            continent_viewership = {continent: sum(record['Viewership'] for record in sport_data if record['Continent'] == continent) for continent in continents}
            bar_fig = px.bar(x=list(continent_viewership.keys()), y=list(continent_viewership.values()))
            bar_fig.update_layout(title_text='Viewership by Continent', title_x=0.5, xaxis_title='Continent', yaxis_title='Viewership')
        else:
            # Calculate viewership by continent for all data
            continent_viewership = {continent: sum(record['Viewership'] for record in filtered_data if record['Continent'] == continent) for continent in continents}
            bar_fig = px.bar(x=list(continent_viewership.keys()), y=list(continent_viewership.values()))
            bar_fig.update_layout(title_text='Viewership by Continent', title_x=0.5, xaxis_title='Continent', yaxis_title='Viewership')
        
        return dcc.Graph(figure=map_fig), dcc.Graph(figure=bar_fig)

    return html.Div([
        html.Label('Select Sport:'),
        dcc.Dropdown(
            id='sport-dropdown',
            options=[{'label': sport, 'value': sport} for sport in sorted(set(record['Sport'] for record in data))],
            value=None
        ),
        html.Label('Select Country:'),
        dcc.Dropdown(
            id='country-dropdown',
            options=[{'label': country, 'value': country} for country in sorted(set(record['Country'] for record in data))],
            value=None
        ),
        html.Div([
            html.Div(id='visualization-output-loc', style={'width': '48%', 'display': 'inline-block'}),
            html.Div(id='additional-visualization-output-loc', style={'width': '48%', 'display': 'inline-block'})
        ])
    ])
