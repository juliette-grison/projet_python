#================= Import des librairies ================#
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import plotly.express as px
import dash
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc

#================= Préparation des données ================#
df = pd.read_csv("./supermarket_sales.csv")

df = df[['Invoice ID', 'Branch', 'City', 'Customer type', 'Gender', 'Product line',
       'Unit price', 'Quantity', 'Tax 5%', 'Total', 'Date', 'Time', 'Payment',
       'cogs', 'gross margin percentage', 'gross income', 'Rating']]

df['Date'] = pd.to_datetime(df['Date'])

#================= Création des indicateurs & graphiques ================#

# 1. Montant total des achats : Somme du montant total des achats (Total)

# Calcul du montant total des achats
def total_achats(data): 
    montant_total = data['Total'].sum()
    return [montant_total, montant_total]

# Création de l'indicateur
def plot_total_achats(data, background="#FFF4B8"):
    montant_total = total_achats(data)  

    indicateur = go.Figure(
        go.Indicator(
            mode="number",
            value=montant_total[0],  
            title={
                "text": "💰 Total Purchase Amount",
                "font": {"family": "Georgia, serif", "size": 18, "color": "black"}},
                number={
                "font": {"size": 54, "color": "black"}
            }
        )
    ).update_layout(
        width=250, height=200,
        margin=dict(l=0, r=20, t=20, b=0),
        paper_bgcolor=background
    )
    
    return indicateur


# 2. Évaluation moyenne : Moyenne des évaluations (Rating)

# Calcul de l'évaluation moyenne
def indicateur_evaluation(data): 
    evaluation_moyenne = data['Rating'].mean()
    return [evaluation_moyenne, evaluation_moyenne]

# Création de l'indicateur
def plot_evaluation(data, background="#FFF4B8"):
    evaluation_moyenne = indicateur_evaluation(data)  

    indicateur = go.Figure(
        go.Indicator(
            mode="number",
            value=evaluation_moyenne[0],  
            title={
                "text": "⭐️ Average Rating",
                "font": {"family": "Georgia, serif", "size": 18, "color": "black"}},
                number={
                "font": {"size": 54, "color": "black"}
                }
        )
    ).update_layout(
        width=250, height=200,
        margin=dict(l=0, r=20, t=20, b=0),
        paper_bgcolor=background
    )

    return indicateur


# 3. Graphique evolution du montant total des achats par semaine par ville

def plot_evolution_achats(data, background="#DFF5D9"):

    city_colors = {
    "Mandalay": "#FFCD00",  
    "Naypyitaw": "#43B02A",  
    "Yangon": "#EE2737"  
    }

    df_plot = data.groupby([pd.Grouper(key='Date', freq='W'), 'City']).apply(total_achats)[:-1]

    df_plot_values = df_plot.apply(lambda x: x[0]) 

    chiffre_evolution = px.line(
        x=df_plot_values.index.get_level_values(0),  
        y=df_plot_values.values,  
        color=df_plot_values.index.get_level_values(1),
        title="📈 Weekly Purchase Amount by City",
        labels={"x": "Week", "y": "Total Amount ($)", "color": "City"},
        markers=True,
        color_discrete_map=city_colors
    ).update_layout(
        width=625, height=300,
        margin=dict(t=60, b=0),
        plot_bgcolor='#DFF5D9',   
        paper_bgcolor=background,
        title=dict(
            text="📈 Weekly Purchase Amount by City",
            font=dict(family="Georgia, serif", size=18, color="black"),  
            x=0.5,  
            xanchor="center"  
        )
    )

    return chiffre_evolution

# 4. Diagramme en barres du nombre total d'achats par sexe et par ville

def plot_commandes_par_sexe_ville(data, background="#FFD6DA"):
    
    gender_colors = {
    "Male": "#1A3D6D",  
    "Female": "#FF6F61"  
    }

    df_plot = data.groupby(['City', 'Gender'])['Invoice ID'].count().reset_index(name="Number of Orders")

    fig = px.bar(
        df_plot,
        x="City",
        y="Number of Orders",
        color="Gender",
        title="🧑‍🤝‍🧑 Number of Orders by City and Gender",
        labels={"Number of Orders": "Number of Orders", "Gender": "Gender", "City": "City"},
        barmode="group",  
        color_discrete_map=gender_colors
    ).update_layout(
        width=500, height=300,
        margin=dict(t=60, b=60),
        plot_bgcolor="#FFD6DA",
        paper_bgcolor=background,
        title=dict(
            text="🧑‍🤝‍🧑 Number of Orders by City and Gender",
            font=dict(family="Georgia, serif", size=18, color="black"),  
            x=0.5,  
            xanchor="center"  
        )
    )

    return fig

# 5. Diagramme circulaire montrant la répartition de la catégorie de produit (Product line) par sexe et par ville

def plot_repartition_produit_sexe_ville(data, background="#FFD6DA"):

    category_colors = {
    "Fashion accessories": "#9B4D96",  
    "Food and beverages": "#FFB84D",   
    "Electronic accessories": "#A9A9A9",  
    "Sports and travel": "#00B5E2",    
    "Home and lifestyle": "#A7D8A1", 
    "Health and beauty": "#F7B7B7"   
    }

    df_plot = data.groupby(['Product line']).size().reset_index(name="Nombre d'Achats")

    fig = px.pie(
        df_plot,
        names="Product line",
        values="Nombre d'Achats",
        color="Product line",
        title="🛍️ Product Line Distribution",
        hole=0.4,  
        color_discrete_map=category_colors
    ).update_layout(
        width=500, height=300,
        margin=dict(t=60, b=60),
        paper_bgcolor=background,
        title=dict(
            text="🛍️ Product Line Distribution",
            font=dict(family="Georgia, serif", size=18, color="black"),  
            x=0.5,  
            xanchor="center"  
            )
    )

    return fig

#================= Création de l'application Dash ================#

# Visuels utilisés
fig1 = plot_total_achats(df)
fig2 = plot_evaluation(df)
fig3 = plot_evolution_achats(df)
fig4 = plot_commandes_par_sexe_ville(df)
fig5 = plot_repartition_produit_sexe_ville(df)

# Application
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = dbc.Container([
    # Ligne d’en-tête principale
dbc.Row([
    # Titre avec drapeau
    dbc.Col(
        html.Div([
            html.Img(
                src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/Flag_of_Myanmar.svg/2560px-Flag_of_Myanmar.svg.png",
                style={
                    "height": "40px",
                    "margin-right": "10px"
                }
            ),
            html.H1("Myanmar Supermarkets", style={
                "font-family": "Georgia, serif",
                "font-weight": "bold",
                "font-size": "36px",
                "color": "#2E2E2E",
                "margin": "0"
            }),
        ], style={"display": "flex", "align-items": "center"}),
        width=6
    ),

    # Filtre genre
    dbc.Col(
        dcc.Dropdown(
            id='dropdown-gender',  
            options=[{'label': gender, 'value': gender} for gender in df["Gender"].dropna().unique()],
            multi=True,
            searchable=True,
            placeholder='Select a gender',
            style={
                "font-family": "Georgia, serif",
                "background-color": "#FAF3E0",
                "border-radius": "8px",
                "box-shadow": "0 2px 4px rgba(0,0,0,0.1)"
            }
        ),
        width=3,
        style={"padding-left": "10px", "padding-right": "10px"}
    ),

    # Filtre ville
    dbc.Col(
        dcc.Dropdown(
            id='dropdown-city',  
            options=[{'label': city, 'value': city} for city in df["City"].dropna().unique()],
            multi=True,
            searchable=True,
            placeholder='Select a city',
            style={
                "font-family": "Georgia, serif",
                "background-color": "#FAF3E0",
                "border-radius": "8px",
                "box-shadow": "0 2px 4px rgba(0,0,0,0.1)"
            }
        ),
        width=3,
        style={"padding-left": "10px", "padding-right": "10px"}
    )
], style={
    "padding": "15px 20px",
    "margin-bottom": "10px",
    "background-color": "#FFFBE6",  
    "border-radius": "10px",
    "box-shadow": "0 2px 8px rgba(0, 0, 0, 0.1)"
}),

# Ligne du sous-titre
dbc.Row([
    dbc.Col(
        html.Div(
            "Dashboard created by Juliette Grison, as part of the Advanced Python course taught by Dr. Abdoul Razac Sane in the Applied Econometrics Master's program (IAE Nantes, 2024-2025)",
            style={
                "font-family": "Georgia, serif",
                "font-size": "15px",
                "color": "#777",
                "font-style": "italic",
                "text-align": "center",
                "padding": "8px",
                "line-height": "1.5"
            }
        )
    )
], style={
    "margin-bottom": "10px",
    "background-color": "#FDFDFD",
    "border-radius": "8px",
    "box-shadow": "0 2px 4px rgba(0,0,0,0.05)"
}),

    # Contenu principal

    # Indicateurs
    dbc.Row([
    dbc.Col(
        html.Div(
            dcc.Graph(id='fig1', figure={}),
            style={"border": "2px solid black", "border-radius": "10px", "padding": "5px", "margin": "5px", "background-color": "#FFF4B8", "box-shadow": "0 4px 8px rgba(0, 0, 0, 0.5)", "position": "relative"}
        ),
        style={"display": "flex", "align-items": "center", "justify-content": "center"}
    ),
    dbc.Col(
        html.Div(
            dcc.Graph(id='fig2', figure={}),
            style={"border": "2px solid black", "border-radius": "10px", "padding": "5px", "margin": "5px", "background-color": "#FFF4B8", "box-shadow": "0 4px 8px rgba(0, 0, 0, 0.5)", "position": "relative"}
        ),
        style={"display": "flex", "align-items": "center", "justify-content": "center"}
    ),
], style={"background-color": "#FFCD00"}),

# Graphique 
dbc.Row([
    dbc.Col(
        html.Div(
            dcc.Graph(id='fig3', figure={}),
            style={"border": "2px solid black", "border-radius": "10px", "padding": "5px", "margin": "5px", "background-color": "#DFF5D9", "box-shadow": "0 4px 8px rgba(0, 0, 0, 0.5)", "position": "relative"}
        ),
        width=12,
        style={"display": "flex", "align-items": "center", "justify-content": "center"}
    ),
], style={"background-color": "#43B02A"}),

# Diagrammes
dbc.Row([
    dbc.Col(
        html.Div(
            dcc.Graph(id='fig4', figure={}),
            style={"border": "2px solid black", "border-radius": "10px", "padding": "5px", "margin": "5px", "background-color": "#FFD6DA", "box-shadow": "0 4px 8px rgba(0, 0, 0, 0.5)", "position": "relative"}
        ),
        style={"display": "flex", "align-items": "center", "justify-content": "center"}
    ),
    dbc.Col(
        html.Div(
            dcc.Graph(id='fig5', figure={}),
            style={"border": "2px solid black", "border-radius": "10px", "padding": "5px", "margin": "5px", "background-color": "#FFD6DA", "box-shadow": "0 4px 8px rgba(0, 0, 0, 0.5)", "position": "relative"}
        ),
        style={"display": "flex", "align-items": "center", "justify-content": "center"}
    ),
], style={"background-color": "#EE2737"})

], fluid=True)

#================= Callback pour mettre à jour les graphiques et le tableau ================#

# Mise à jour en fonction de la sélection du dropdown
@app.callback(
    Output('fig1', 'figure'),
    Output('fig2', 'figure'),
    Output('fig3', 'figure'),
    Output('fig4', 'figure'),
    Output('fig5', 'figure'),  
    Input('dropdown-gender', 'value'),
    Input('dropdown-city', 'value')
)

def update_charts(selected_genders, selected_cities):
    filtered_df = df  
    
    # Filtre par genre si une sélection est faite
    if selected_genders:
        filtered_df = filtered_df[filtered_df["Gender"].isin(selected_genders)]

    # Filtre par ville si une sélection est faite
    if selected_cities:
        filtered_df = filtered_df[filtered_df["City"].isin(selected_cities)]

    # Génération des nouveaux graphiques
    return (
        plot_total_achats(filtered_df),
        plot_evaluation(filtered_df),
        plot_evolution_achats(filtered_df),
        plot_commandes_par_sexe_ville(filtered_df),
        plot_repartition_produit_sexe_ville(filtered_df)
    )

if __name__ == '__main__':
    app.run(debug=True, port=8050) 