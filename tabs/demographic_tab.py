from dash import dcc, html, Input, Output
import plotly.express as px

def layout(app, data):
    countries = sorted(set(record['Country'] for record in data))
    continents = sorted(set(record['Continent'] for record in data))
    age_groups = {
        "18-25": "18-25",
        "26-35": "26-35",
        "36-45": "36-45",
        "46-55": "46-55",
        "56-65": "56-65",
        "66-70": "66-70"
    }

    @app.callback(
        Output('continent-demographic-dropdown', 'value'),
        [Input('country-demographic-dropdown', 'value')],
        prevent_initial_call=True
    )
    def update_continent_based_on_country(selected_country):
        if selected_country is None:
            return None
        
        for record in data:
            if record['Country'] == selected_country:
                return record['Continent']
        return None

    @app.callback(
        [Output('country-demographic-output', 'children'),
         Output('continent-demographic-output', 'children')],
        [Input('demographic-dropdown', 'value'),
         Input('country-demographic-dropdown', 'value'),
         Input('continent-demographic-dropdown', 'value')]
    )
    def update_demographic_output(selected_demographic, selected_country, selected_continent):
        filtered_data_country = data.copy()
        filtered_data_continent = data.copy()
        
        # Apply country filter
        if selected_country:
            filtered_data_country = [record for record in filtered_data_country if record['Country'] == selected_country]
        
        # Apply continent filter
        if selected_continent:
            filtered_data_continent = [record for record in filtered_data_continent if record['Continent'] == selected_continent]
        
        if selected_demographic == 'Age':
            # Group ages and sum viewership
            age_group_counts_country = {age_group: sum(record['Viewership'] for record in filtered_data_country if age_group == record['Age']) for age_group in age_groups.values()}
            age_group_counts_sorted_country = {k: age_group_counts_country[k] for k in sorted(age_group_counts_country.keys())}
            age_fig_country = px.bar(x=list(age_group_counts_sorted_country.keys()), y=list(age_group_counts_sorted_country.values()), title='Viewership Distribution by Age Group (Country)')
            age_fig_country.update_layout(title_x=0.5, xaxis_title='Age Group', yaxis_title='Viewership')
            
            age_group_counts_continent = {age_group: sum(record['Viewership'] for record in filtered_data_continent if age_group == record['Age']) for age_group in age_groups.values()}
            age_group_counts_sorted_continent = {k: age_group_counts_continent[k] for k in sorted(age_group_counts_continent.keys())}
            age_fig_continent = px.pie(names=list(age_group_counts_sorted_continent.keys()), values=list(age_group_counts_sorted_continent.values()), title='Viewership Distribution by Age Group (Continent)')
            
            return dcc.Graph(figure=age_fig_country), dcc.Graph(figure=age_fig_continent)
        elif selected_demographic == 'Gender':
            # Count gender distribution
            gender_counts_country = {gender: sum(record['Viewership'] for record in filtered_data_country if record['Gender'] == gender) for gender in ['Male', 'Female']}
            gender_fig_country = px.bar(x=list(gender_counts_country.keys()), y=list(gender_counts_country.values()), title='Viewership Distribution by Gender (Country)')
            gender_fig_country.update_layout(title_x=0.5, xaxis_title='Gender', yaxis_title='Viewership')
            
            gender_counts_continent = {gender: sum(record['Viewership'] for record in filtered_data_continent if record['Gender'] == gender) for gender in ['Male', 'Female']}
            gender_fig_continent = px.pie(names=list(gender_counts_continent.keys()), values=list(gender_counts_continent.values()), title='Viewership Distribution by Gender (Continent)')
            
            return dcc.Graph(figure=gender_fig_country), dcc.Graph(figure=gender_fig_continent)
        else:
            return None, None

    return html.Div([
        html.Div([
            html.Label('Select Demographic:'),
            dcc.Dropdown(
                id='demographic-dropdown',
                options=[{'label': 'Age Group', 'value': 'Age'}, {'label': 'Gender', 'value': 'Gender'}],
                value='Age',
                style={'width': '100%', 'font-size': '14px'}
            ),
        ], style={'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),
        html.Div([
            html.Div([
                html.Label('Select Country:'),
                dcc.Dropdown(
                    id='country-demographic-dropdown',
                    options=[{'label': country, 'value': country} for country in countries],
                    value=None,
                    style={'width': '100%', 'font-size': '14px'}
                ),
                html.Div(id='country-demographic-output', style={'width': '100%', 'display': 'inline-block'})
            ], style={'flex': '1', 'display': 'inline-block', 'margin-right': '20px'}),
            html.Div([
                html.Label('Select Continent:'),
                dcc.Dropdown(
                    id='continent-demographic-dropdown',
                    options=[{'label': continent, 'value': continent} for continent in continents],
                    value=None,
                    style={'width': '100%', 'font-size': '14px'}
                ),
                html.Div(id='continent-demographic-output', style={'width': '100%', 'display': 'inline-block'})
            ], style={'flex': '1', 'display': 'inline-block'})
        ], style={'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'})
    ], style={'width': '100%', 'display': 'flex', 'flex-direction': 'column', 'align-items': 'center', 'justify-content': 'center'})
