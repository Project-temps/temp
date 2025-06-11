<<<<<<< HEAD
import os
import glob
import pandas as pd
from dash import dcc, html, Input, Output
# from dash_extensions.snippets import send_data_frame
from django_plotly_dash import DjangoDash
import plotly.express as px
from dash import dcc

# adjust this so it points at your repo’s data/processed
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'processed')

# load CSVs and tag by farm
all_files = glob.glob(os.path.join(DATA_DIR, "*.csv"))
dfs = []
for f in all_files:
    farm = os.path.basename(f).split('_')[0]
    df = pd.read_csv(f, parse_dates=[0])
    df.rename(columns={df.columns[0]:'Date'}, inplace=True)
    df['Farm'] = farm
    dfs.append(df)

df_all = pd.concat(dfs, ignore_index=True)
time_col = 'Date'
params = [c for c in df_all.columns if c not in ['Farm', time_col]]

app = DjangoDash("FarmDataDashboard")

app.layout = html.Div([
    html.H2("Farm Data Dashboard", style={'textAlign':'center'}),
    html.Div([
        html.Label("Farms:"),
        dcc.Checklist(
            id='farm-selector',
            options=[{'label':f,'value':f} for f in sorted(df_all.Farm.unique())],
            value=sorted(df_all.Farm.unique()),
            inline=True
        )
    ], style={'padding':'10px'}),

    html.Div([
        html.Label("Parameters:"),
        dcc.Dropdown(
            id='param-selector',
            options=[{'label':p,'value':p} for p in params],
            value=[params[0]],
            multi=True
        )
    ], style={'padding':'10px'}),

    html.Div([
        html.Label("Date range:"),
        dcc.DatePickerRange(
            id='date-range',
            start_date=df_all[time_col].min().date(),
            end_date=df_all[time_col].max().date()
        )
    ], style={'padding':'10px'}),

    dcc.Graph(id='time-series-graph'),

    html.Button("Export CSV", id='export-button'),
    dcc.Download(id='download-data')
])

@app.callback(
    Output('time-series-graph','figure'),
    Input('farm-selector','value'),
    Input('param-selector','value'),
    Input('date-range','start_date'),
    Input('date-range','end_date'),
)
def update_graph(farms, params_sel, start, end):
    if not farms or not params_sel:
        return {}
    dff = df_all[df_all.Farm.isin(farms)]
    dff = dff[(dff.Date>=start)&(dff.Date<=end)]
    fig = px.line(
        dff,
        x='Date',
        y=params_sel,
        color='Farm',
        title="Time Series Comparison"
    )
    return fig

@app.callback(
    Output('download-data','data'),
    Input('export-button','n_clicks'),
    Input('farm-selector','value'),
    Input('param-selector','value'),
    Input('date-range','start_date'),
    Input('date-range','end_date'),
)
def export_data(n, farms, params_sel, start, end):
    if not n:
        return
    dff = df_all[df_all.Farm.isin(farms)]
    dff = dff[(dff.Date>=start)&(dff.Date<=end)]
    cols = ['Farm','Date'] + params_sel
    return dcc.send_data_frame(dff[cols].to_csv, "exported.csv")

=======
# ui/dashapp.py
import pandas as pd
from dash import html, dcc, Input, Output
from django_plotly_dash import DjangoDash
from api.models import Farm, SensorReading
import plotly.express as px

app = DjangoDash("FarmTimeSeries")

def farm_options():
    return [{"label": f.name, "value": f.id} for f in Farm.objects.all()]

def parameter_options():
    params = (
        SensorReading.objects.values_list("parameter", flat=True)
        .distinct()
        .order_by("parameter")
    )
    return [{"label": p, "value": p} for p in params]

def serve_layout():
    return html.Div(
        [
            html.Div(
                [
                    dcc.Dropdown(id="farm-1", placeholder="Farm A"),
                    dcc.Dropdown(id="farm-2", placeholder="Farm B (optional)"),
                ],
                style={"display": "flex", "marginBottom": "1rem"},
            ),
            dcc.Dropdown(id="parameter", placeholder="Parameter"),
            dcc.DatePickerRange(id="range"),
            dcc.Graph(id="time-series-plot"),
            dcc.Store(id="init-data"),   # براى پرکردن آپشن‌ها بعداً
        ],
        style={"padding": "1rem"},
    )

app.layout = serve_layout

# پر کردن آپشن‌ها بعد از اولین رندر
@app.callback(
    Output("farm-1", "options"),
    Output("farm-2", "options"),
    Output("parameter", "options"),
    Input("init-data", "data"),
)
def fill_dropdowns(_):
    return farm_options(), farm_options(), parameter_options()

# کال‌بک رسم چارت همانى که قبلاً نوشتیم
@app.callback(
    Output("time-series-plot", "figure"),
    Input("farm-1", "value"),
    Input("farm-2", "value"),
    Input("parameter", "value"),
    Input("range", "start_date"),
    Input("range", "end_date"),
)
def update_chart(f1, f2, param, start, end):
    if not (f1 and param and start and end):
        return {}
    qs = SensorReading.objects.filter(
        farm_id__in=[f1, f2] if f2 else [f1],
        parameter=param,
        ts__range=[start, end],
    ).values("farm__name", "ts", "value")
    df = pd.DataFrame.from_records(qs)
    if df.empty:
        return {}
    fig = px.line(df, x="ts", y="value", color="farm__name",
                  labels={"value": param, "ts": "Timestamp", "farm__name": "Farm"})
    fig.update_layout(hovermode="x unified")
    return fig
>>>>>>> 7576c1d35bb7910344a6ac3a18c4a6d539cb55fd
