from dash import dcc, html, Input, Output, State
import plotly.express as px

def layout(app, data):
    countries = sorted(set(record['Country'] for record in data))
    continents = sorted(set(record['Continent'] for record in data))

    @app.callback(
        Output('continent-peak-hour-dropdown', 'options'),
        [Input('country-peak-hour-dropdown', 'value')]
    )
    def update_continent_options(selected_country):
        if selected_country:
            filtered_continents = set(record['Continent'] for record in data if record['Country'] == selected_country)
            return [{'label': continent, 'value': continent} for continent in continents if continent in filtered_continents]
        else:
            return [{'label': continent, 'value': continent} for continent in continents]

    @app.callback(
        [Output('continent-peak-hour-dropdown', 'value')],
        [Input('country-peak-hour-dropdown', 'value')]
    )
    def update_selected_continent(selected_country):
        if selected_country:
            # Find the first continent corresponding to the selected country
            for record in data:
                if record['Country'] == selected_country:
                    return [record['Continent']]
        return [None]

    @app.callback(
        [Output('visualization-output-peak-hour', 'children'),
         Output('additional-visualization-output-peak-hour', 'children')],
        [Input('country-peak-hour-dropdown', 'value'),
         Input('continent-peak-hour-dropdown', 'value')]
    )
    def update_visualization_peak_hour(selected_country, selected_continent):
        filtered_data_country = [record for record in data if (selected_country is None or record['Country'] == selected_country)]
        filtered_data_continent = [record for record in data if (selected_continent is None or record['Continent'] == selected_continent)]

        # Histogram for viewership distribution over peak usage hours (for country)
        hist_fig_country = px.bar(filtered_data_country, x='Peak Usage Hours', y='Viewership', title=f'Viewership Distribution over Peak Usage Hours in {selected_country}')
        hist_fig_country.update_layout(title_x=0.5, xaxis_title='Peak Usage Hours', yaxis_title='Viewership')

        # Histogram for viewership distribution over peak usage hours (for continent)
        hist_fig_continent = px.bar(filtered_data_continent, x='Peak Usage Hours', y='Viewership', title=f'Viewership Distribution over Peak Usage Hours in {selected_continent}')
        hist_fig_continent.update_layout(title_x=0.5, xaxis_title='Peak Usage Hours', yaxis_title='Viewership')

        return dcc.Graph(figure=hist_fig_country), dcc.Graph(figure=hist_fig_continent)

    return html.Div([
        html.Label('Select Country:'),
        dcc.Dropdown(
            id='country-peak-hour-dropdown',
            options=[{'label': country, 'value': country} for country in countries],
            value=None
        ),
        html.Label('Select Continent:'),
        dcc.Dropdown(
            id='continent-peak-hour-dropdown',
            options=[{'label': continent, 'value': continent} for continent in continents],
            value=None
        ),
        html.Div([
            html.Div(id='visualization-output-peak-hour', style={'width': '48%', 'display': 'inline-block'}),
            html.Div(id='additional-visualization-output-peak-hour', style={'width': '48%', 'display': 'inline-block'})
        ])
    ])
