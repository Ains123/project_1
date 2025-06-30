import dash
from dash import dcc, html, dash_table
import pandas as pd
import plotly.express as px


# Load cleaned data
df = pd.read_csv("data/cleaned_aviation_data.csv")


# Preprocess
df['Event.Date'] = pd.to_datetime(df['Event.Date'], errors='coerce')
df['Latitude'] = pd.to_numeric(df['Latitude'], errors='coerce')
df['Longitude'] = pd.to_numeric(df['Longitude'], errors='coerce')

df['Year'] = df['Event.Date'].dt.year
df['Total.Fatal.Injuries'] = pd.to_numeric(df['Total.Fatal.Injuries'], errors='coerce')

# Layout components
accidents_by_year = df['Year'].value_counts().sort_index()
fig1 = px.line(x=accidents_by_year.index, y=accidents_by_year.values,
               labels={'x': 'Year', 'y': 'Number of Accidents'},
               title='Accidents by Year')

country_counts = df['Country'].value_counts().nlargest(10)
fig2 = px.bar(x=country_counts.index, y=country_counts.values,
              labels={'x': 'Country', 'y': 'Number of Accidents'},
              title='Top 10 Countries with Most Accidents')

phase_counts = df['Broad.phase.of.flight'].value_counts()
fig3 = px.bar(y=phase_counts.index, x=phase_counts.values, orientation='h',
              labels={'x': 'Number of Accidents', 'y': 'Phase of Flight'},
              title='Accidents by Phase of Flight')

# Dash app
app = dash.Dash(__name__)
app.title = "Aviation Accident Dashboard"

app.layout = html.Div([
    html.H1("Aviation Accident Analysis (1962–2023)", style={'textAlign': 'center'}),

    dcc.Graph(figure=fig1),
    dcc.Graph(figure=fig2),
    dcc.Graph(figure=fig3),

    html.H3("Accident Data Table"),
    dash_table.DataTable(
        data=df[['Event.Id', 'Event.Date', 'Location', 'Country', 'Broad.phase.of.flight', 'Total.Fatal.Injuries']].dropna().to_dict('records'),
        columns=[{"name": i, "id": i} for i in ['Event.Id', 'Event.Date', 'Location', 'Country', 'Broad.phase.of.flight', 'Total.Fatal.Injuries']],
        page_size=10,
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left', 'padding': '5px'},
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
