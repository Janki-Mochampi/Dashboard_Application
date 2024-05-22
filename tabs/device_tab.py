from dash import dcc, html, Input, Output
import plotly.express as px

def layout(app, data):
    countries = sorted(set(record['Country'] for record in data))
    continents = sorted(set(record['Continent'] for record in data))

    @app.callback(
        Output('continent-dropdown', 'options'),
        [Input('country-device-dropdown', 'value')]
    )
    def update_continent_options(selected_country):
        if selected_country is None:
            continent_options = [{'label': continent, 'value': continent} for continent in continents + ['All Continents']]
        else:
            selected_country_continent = None
            for record in data:
                if record['Country'] == selected_country:
                    selected_country_continent = record['Continent']
                    break
            continent_options = [{'label': continent, 'value': continent} for continent in continents]
            if selected_country_continent not in continents:
                continent_options.append({'label': selected_country_continent, 'value': selected_country_continent})
            continent_options.append({'label': 'All Continents', 'value': 'All Continents'})

        return continent_options

    @app.callback(
        Output('continent-dropdown', 'value'),
        [Input('country-device-dropdown', 'value')]
    )
    def update_continent_value(selected_country):
        if selected_country is None:
            return None

        for record in data:
            if record['Country'] == selected_country:
                return record['Continent']

    def update_visualization(selected_data, title_suffix):
        if selected_data is None:
            return None, None

        if selected_data == 'All Countries' or selected_data == 'All Continents':
            filtered_data = data
        else:
            filtered_data = [record for record in data if record['Country'] == selected_data]

        # Bar chart for viewership distribution by device type
        device_counts = {}
        for record in filtered_data:
            device = record['User Agents']
            device_counts[device] = device_counts.get(device, 0) + record['Viewership']

        bar_fig = px.bar(x=list(device_counts.keys()), y=list(device_counts.values()), title=f'Viewership Distribution by Device Type {title_suffix}')
        bar_fig.update_layout(title_x=0.5, xaxis_title='Device Type', yaxis_title='Viewership')

        # Pie chart for viewership distribution by device type
        pie_fig = px.pie(filtered_data, values='Viewership', names='User Agents', title=f'Proportion of Viewership by Device Type {title_suffix}')
        pie_fig.update_layout(title_x=0.5)

        return dcc.Graph(figure=bar_fig), dcc.Graph(figure=pie_fig)

    @app.callback(
        [Output('country-visualization-output-device', 'children'),
         Output('country-additional-visualization-output-device', 'children')],
        [Input('country-device-dropdown', 'value')]
    )
    def update_country_visualization(selected_country):
        return update_visualization(selected_country, f'for {selected_country}' if selected_country else 'for All Countries')

    @app.callback(
        [Output('continent-visualization-output-device', 'children'),
         Output('continent-additional-visualization-output-device', 'children')],
        [Input('continent-dropdown', 'value')]
    )
    def update_continent_visualization(selected_continent):
        return update_visualization(selected_continent, f'in {selected_continent}' if selected_continent else 'for All Continents')

    return html.Div([
        html.Div([
            html.Label('Select Country:'),
            dcc.Dropdown(
                id='country-device-dropdown',
                options=[{'label': country, 'value': country} for country in countries + ['All Countries']],
                value=None,
                style={'width': '300px', 'font-size': '14px'}
            ),
            html.Div(id='country-visualization-output-device', style={'width': '48%', 'display': 'inline-block'}),
            html.Div(id='country-additional-visualization-output-device', style={'width': '48%', 'display': 'inline-block'})
        ], style={'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),
        html.Div([
            html.Label('Select Continent:'),
            dcc.Dropdown(
                id='continent-dropdown',
                options=[{'label': continent, 'value': continent} for continent in continents + ['All Continents']],
                value=None,
                style={'width': '300px', 'font-size': '14px'}
            ),
            html.Div(id='continent-visualization-output-device', style={'width': '48%', 'display': 'inline-block'}),
            html.Div(id='continent-additional-visualization-output-device', style={'width': '48%', 'display': 'inline-block'})
        ], style={'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'})
    ], style={'width': '100%', 'display': 'flex', 'flex-direction': 'column', 'align-items': 'center', 'justify-content': 'center'})
