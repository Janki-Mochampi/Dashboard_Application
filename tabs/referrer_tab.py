from dash import dcc, html, Input, Output
import plotly.express as px

def layout(app, data):
    countries = sorted(set(record['Country'] for record in data))
    continents = sorted(set(record['Continent'] for record in data))

    @app.callback(
        Output('continent-referrer-dropdown', 'options'),
        [Input('country-referrer-dropdown', 'value')]
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
        Output('continent-referrer-dropdown', 'value'),
        [Input('country-referrer-dropdown', 'value')]
    )
    def update_continent_value(selected_country):
        if selected_country is None:
            return None

        for record in data:
            if record['Country'] == selected_country:
                return record['Continent']

    @app.callback(
        [Output('country-visualization-output-referrer', 'children'),
         Output('country-additional-visualization-output-referrer', 'children')],
        [Input('country-referrer-dropdown', 'value')]
    )
    def update_country_visualization(selected_country):
        if selected_country is None:
            return None, None

        if selected_country == 'All Countries':
            filtered_data = data
            title_suffix = 'for All Countries'
        else:
            filtered_data = [record for record in data if record['Country'] == selected_country]
            title_suffix = f'in {selected_country}'

        # Pie chart for viewership distribution by referrer
        pie_fig = px.pie(filtered_data, values='Viewership', names='Referrer', title=f'Viewership Distribution by Referrer {title_suffix}')
        pie_fig.update_layout(title_x=0.5)

        # Bar chart for viewership distribution by referrer in the selected country
        referrer_counts = {referrer: sum(record['Viewership'] for record in filtered_data if record['Referrer'] == referrer) for referrer in set(record['Referrer'] for record in filtered_data)}
        bar_fig = px.bar(x=list(referrer_counts.keys()), y=list(referrer_counts.values()), title=f'Viewership by Referrer {title_suffix}')
        bar_fig.update_layout(title_x=0.5, xaxis_title='Referrer', yaxis_title='Viewership')

        # Fix the template to avoid the marker pattern shape issue
        bar_fig.update_layout(template='plotly')

        return dcc.Graph(figure=pie_fig), dcc.Graph(figure=bar_fig)

    @app.callback(
        [Output('continent-visualization-output-referrer', 'children'),
         Output('continent-additional-visualization-output-referrer', 'children')],
        [Input('continent-referrer-dropdown', 'value')]
    )
    def update_continent_visualization(selected_continent):
        if selected_continent is None:
            return None, None

        if selected_continent == 'All Continents':
            filtered_data = data
            title_suffix = 'for All Continents'
        else:
            filtered_data = [record for record in data if record['Continent'] == selected_continent]
            title_suffix = f'in {selected_continent}'

        # Pie chart for viewership distribution by referrer
        pie_fig = px.pie(filtered_data, values='Viewership', names='Referrer', title=f'Viewership Distribution by Referrer {title_suffix}')
        pie_fig.update_layout(title_x=0.5)

        # Bar chart for viewership distribution by referrer in the selected continent
        referrer_counts = {referrer: sum(record['Viewership'] for record in filtered_data if record['Referrer'] == referrer) for referrer in set(record['Referrer'] for record in filtered_data)}
        bar_fig = px.bar(x=list(referrer_counts.keys()), y=list(referrer_counts.values()), title=f'Viewership by Referrer {title_suffix}')
        bar_fig.update_layout(title_x=0.5, xaxis_title='Referrer', yaxis_title='Viewership')

        # Fix the template to avoid the marker pattern shape issue
        bar_fig.update_layout(template='plotly')

        return dcc.Graph(figure=pie_fig), dcc.Graph(figure=bar_fig)

    return html.Div([
        html.Div([
            html.Label('Select Country:'),
            dcc.Dropdown(
                id='country-referrer-dropdown',
                options=[{'label': country, 'value': country} for country in countries + ['All Countries']],
                value=None,
                style={'width': '300px', 'font-size': '14px'}
            ),
            html.Div(id='country-visualization-output-referrer', style={'width': '48%', 'display': 'inline-block'}),
            html.Div(id='country-additional-visualization-output-referrer', style={'width': '48%', 'display': 'inline-block'})
        ], style={'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),
        html.Div([
            html.Label('Select Continent:'),
            dcc.Dropdown(
                id='continent-referrer-dropdown',
                options=[{'label': continent, 'value': continent} for continent in continents + ['All Continents']],
                value=None,
                style={'width': '300px', 'font-size': '14px'}
            ),
            html.Div(id='continent-visualization-output-referrer', style={'width': '48%', 'display': 'inline-block'}),
            html.Div(id='continent-additional-visualization-output-referrer', style={'width': '48%', 'display': 'inline-block'})
        ], style={'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'})
    ], style={'width': '100%', 'display': 'flex', 'flex-direction': 'column', 'align-items': 'center', 'justify-content': 'center'})
