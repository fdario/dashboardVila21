# Import packages
from dash import Dash, html, dash_table, dcc, html, callback, Input, Output
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import os
from threading import Timer
import webbrowser

# Incorporate data
df = pd.read_csv('csv-folder/DV21.csv')

# Initialize the app
app = Dash(external_stylesheets=[dbc.themes.MINTY])
load_figure_template('MINTY')

HEADER = {
    "textAlign": "center",
    "font-family": "sans-serif",
    "position": "sticky",
    "top": "0",
    "padding": "3vh",
    "margin": "0",
    "z-index": "10",
    "background-color": "#e9ecef",
    
}

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "1rem 0.8rem",
    "background-color": "#e9ecef",
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "display": "flex",
    "flex-direction": "column"
}

# Colors to use in the plots and dashboards 
# colors = {
#     'background': '#424241',
#     'text': 'white'
# }


# Plot types and examples
fig1 = px.sunburst(df, path=['CLIENTE', 'TAREFA'], values='CODIGO', title='Tarefas por cada cliente')
fig2 = px.pie(df, values='CODIGO', names='TAREFA', title='Quantidade Tarefas p/ código')
fig3 = px.histogram(df, x='TAREFA', title='Quantidade de Tarefas')

# Layout of the plots (Can be changed in 'colors')
# fig1.update_layout(
#     plot_bgcolor=colors['background'],
#     paper_bgcolor=colors['background'],
#     font_color=colors['text']
# )

# App layout
app.layout = [     
    html.Div(
        id="conteudo",
        children=[
         html.Div(
             html.H1(
                 children='Dashboard'
                 ),
             style = HEADER
             ),
         html.Div(
             id="menu-lateral",
             children=[
                 html.Img(
                     id='logo',
                     src='assets/logoVila21.png',
                     style={
                         "height": "12vh",
                         "margin": "0 2rem"
                         }
                     ),
                 html.Hr(),
                 html.Div([
                     html.Div(
                         id='filtrar_tarefa',
                         children=
                         [
                             html.H2(
                                 children='Selecione apenas 2 tarefas para comparação:',
                                 style={
                                     'textAlign': 'center',
                                     'font-family': 'sans-serif',
                                     'text-decoration': 'underline',
                                     'font-size': '1.4em'
                                     }
                                 ),
                             dcc.Dropdown(
                                 df['TAREFA'].drop_duplicates(),
                                 multi=True,
                                 placeholder='Filtro por tarefas',
                                 id='tarefa_cliente',
                                 style={
                                     'textAlign': 'center',
                                     'font-family': 'sans-serif',
                                     'color': 'black',
                                     'font-size': '0.875em'
                                     },
                                 optionHeight=80
                                 ),
                             ]
                         ),
                     ]
                          ),
                 html.Hr(),
                 html.Div([
                     html.H2(
                         id='Tarefa', 
                         className='',
                         children='Selecione o condomínio para visualizar as tarefas:',
                         style={
                             'textAlign': 'center',
                             'font-family': 'sans-serif',
                             'text-decoration': 'underline',
                             'font-size': '1.4em'
                             }
                         ),
                     dcc.Dropdown(
                         df['CLIENTE'],
                         placeholder='Escolha',
                         id='nome_condominio',
                         style={
                             'textAlign': 'center',
                             'font-family': 'sans-serif',
                             'color': 'black',
                             'justify-content': 'center',
                             'font-size': '0.875em'
                             },
                         optionHeight=60
                         )
                     ]
                          )
                 ], style=SIDEBAR_STYLE
             ),
         html.Br(),
         html.Div(
             id='filtro_tarefa',
             style={
                 'textAlign': 'center',
                 'font-family': 'sans-serif',
                 }       
             ),         
         html.Br(),
         html.Div(
             id='nomeCondominio',
             style={
                 'justify-content': 'center'
                 }       
             ),
         #html.Hr(),
         html.Div([
             html.Div([
                html.Div(
                    dcc.Graph(
                        figure = fig2, 
                        style={
                            'width': '100%'
                            }
                        ),
                    style={
                        'width': '100%',
                        'display': 'flex',
                        'justify-content': 'center'
                        }
                    ),
                html.Div(
                    dcc.Graph(
                        figure = fig3, 
                        style={
                            'width': '100%'
                            }
                        ),
                    style={ 
                        'width': '100%',
                        'display': 'flex',
                        'justify-content': 'center'              
                        }
                    ),
                ]
                    ),
            html.Br(),
            html.Div(
                [
                    dcc.Graph(
                        figure=fig1
                        )
                    ],
                    style={
                        'width': '100%',
                        'display': 'flex',
                        'justify-content': 'center'
                        }
                ),
            html.Br(),
            ]
                )
         ], style=CONTENT_STYLE
             )
    , 
    ]
        
@callback(
    Output('nomeCondominio', 'children'),
    Input('nome_condominio', 'value')
    )

def update_figure(nome_condominio):
        if nome_condominio != None and nome_condominio != '':
            localizacao = df[df['CLIENTE'] == nome_condominio]
            localizacao.to_csv('csv-folder/saida_cliente.csv', index=False)
            df2 = pd.read_csv('csv-folder/saida_cliente.csv')
            data = df2.to_dict('records')
            tab_espec = dash_table.DataTable(
                data=data,
                style_header={
                    'backgroundColor': '#adadad',
                    'color': 'white'
                    },
                style_data={
                    'backgroundColor': '#e9ecef',
                    'color': 'black',
                    'max-width': '250px'
                    },
                )
            fig4 = px.sunburst(df2, path=['CLIENTE', 'TAREFA'], values='CODIGO', title=f'Tarefas do {nome_condominio}')
            show_tab_espec = dcc.Loading(
                children=[
                    dcc.Graph(figure=fig4)             
                    ], type='circle') 
            
            return html.H4(children=f'Registros do condominio {nome_condominio}'), tab_espec, html.Br(),show_tab_espec, html.Br()
        
@callback (   
    Output('filtro_tarefa', 'children'),
    Input('tarefa_cliente', 'value')
)
def multi_tarefas (tarefas):
    if tarefas != None and tarefas != [] and tarefas != '':
        if(len(tarefas)) < 2:
            return f'Selecione mais uma tarefa'
        else:                
            tarefa_selecionada = df[df['TAREFA'] == tarefas[0]]
            tarefa_2_selecionada = df[df['TAREFA'] == tarefas[1]]
            tarefa_selecionada.to_csv('csv-folder/tarefa_selecionada.csv', index=False) 
            tarefa_2_selecionada.to_csv('csv-folder/tarefa_2_selecionada.csv', index=False)
            df_ts = pd.read_csv('csv-folder/tarefa_selecionada.csv')
            df_t2s = pd.read_csv('csv-folder/tarefa_2_selecionada.csv')
            df3 = pd.concat([df_ts, df_t2s])
            
            fig5 = px.pie(df3, values='CODIGO', names='TAREFA', title='Quantidade Tarefas')
            show_tab_tar_esp = dcc.Loading(
                children=[
                    dcc.Graph(figure=fig5)
                    ],
                type='circle')
            return show_tab_tar_esp, html.Br()

def open_browser():
    if not os.environ.get("WERKZEUG_RUN_MAIN"):
        webbrowser.open_new('http://127.0.0.1:8050/')

if __name__ == "__main__":
    Timer(1, open_browser).start()
    app.run_server(debug=True, port=8050)