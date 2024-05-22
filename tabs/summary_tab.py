from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import plotly.express as px

def layout(app, data):
    @app.callback(
        Output('summary-stats', 'children'),
        [Input('summary-stats', 'id')]
    )
    def generate_summary_stats(_):
        viewership_values = [record['Viewership'] for record in data]
        total_viewership = sum(viewership_values)
        average_viewership = total_viewership / len(data)
        maximum_viewership = max(viewership_values)
        minimum_viewership = min(viewership_values)

        # Calculate counts for each continent
        continent_counts = {}
        for record in data:
            continent_counts[record['Continent']] = continent_counts.get(record['Continent'], 0) + record['Viewership']

        # Determine the continent with the highest viewership
        continent_with_highest_viewership = max(continent_counts, key=continent_counts.get)

        # Create a pie chart for viewership of the most popular sport
        most_popular_sport = ''
        most_popular_sport_viewership = 0
        sport_counts = {}
        for record in data:
            sport_counts[record['Sport']] = sport_counts.get(record['Sport'], 0) + record['Viewership']
        if sport_counts:
            most_popular_sport = max(sport_counts, key=sport_counts.get)
            most_popular_sport_viewership = sport_counts[most_popular_sport]

        # Create indicator for continent with highest viewership
        continent_viewership_fig = go.Figure(go.Indicator(
            mode="number",
            value=continent_counts[continent_with_highest_viewership],
            title={'text': f"Viewership of Most Popular Continent ({continent_with_highest_viewership})"}
        ))

        # Create a gauge chart for viewership of the most popular sport
        most_popular_sport_fig = go.Figure(go.Indicator(
            mode="number",
            value=most_popular_sport_viewership,
            title={'text': f"Viewership of Most Popular Sport ({most_popular_sport})"}
        ))

        # Total Viewership
        total_viewership_fig = go.Figure(go.Indicator(
            mode="number",
            value=total_viewership,
            title={'text': "Total Viewership"}
        ))

        # Average Viewership
        average_viewership_fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=average_viewership,
            title={'text': "Average Viewership"},
            gauge={
                'axis': {'range': [0, maximum_viewership]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, average_viewership], 'color': "lightblue"},
                    {'range': [average_viewership, maximum_viewership], 'color': "lightgray"}
                ],
            }
        ))

        # Maximum Viewership
        maximum_viewership_fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=maximum_viewership,
            title={'text': "Maximum Viewership"},
            gauge={
                'axis': {'range': [0, maximum_viewership]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, average_viewership], 'color': "lightblue"},
                    {'range': [average_viewership, maximum_viewership], 'color': "lightgray"}
                ],
            }
        ))

        # Minimum Viewership
        minimum_viewership_fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=minimum_viewership,
            title={'text': "Minimum Viewership"},
            gauge={
                'axis': {'range': [0, maximum_viewership]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, average_viewership], 'color': "lightblue"},
                    {'range': [average_viewership, maximum_viewership], 'color': "lightgray"}
                ],
            }
        ))

        return html.Div(style={'display': 'grid', 'grid-template-columns': 'repeat(3, 1fr)', 'row-gap': '1px', 'column-gap': '1px'}, children=[
            dcc.Graph(figure=continent_viewership_fig),
            dcc.Graph(figure=total_viewership_fig),
            dcc.Graph(figure=most_popular_sport_fig),
            dcc.Graph(figure=average_viewership_fig),
            dcc.Graph(figure=maximum_viewership_fig),
            dcc.Graph(figure=minimum_viewership_fig)
        ])

    return html.Div([
        html.Div(id='summary-stats')
    ])
