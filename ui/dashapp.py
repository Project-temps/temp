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
