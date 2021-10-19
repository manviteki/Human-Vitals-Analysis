# import scraping modules
from selenium import webdriver
import pandas as pd

# open browser
driver = webdriver.Chrome()

# scrape vital signs
driver.get("https://medicalprogress.dev/patient_file2/vit_signs.html")
html = driver.page_source
driver.close()
data = pd.read_html(html)
data = data[0]
data = pd.DataFrame(data)
print(data)


# replace empty bloodpressure values (- / -) with nothing
data = data.replace(to_replace='- / -', value='')
# replace all comments behind numbers with nothing
data[data.columns[1]] = data[data.columns[1]].str.replace(r'[a-zA-Z].*', '', regex=True)

# make two new columns for sys and dias BP
data['Systolic BP'] = ''
data['Diastolic BP'] = ''
# transport BP into two new columns seperated on systolic and diastolic
data['Systolic BP'] = data[data.columns[1]].str.replace(r'[/].*', '', regex=True)
data['Diastolic BP'] = data[data.columns[1]].str.replace(r'.*[/]', '', regex=True)
# drop the bloodpressure column
data.drop(data.columns[1], axis=1, inplace=True)

# mask all temp > 43 and < 35
data["Temperature"] = data["Temperature"].mask(data["Temperature"] > float(40))
data["Temperature"] = data["Temperature"].mask(data["Temperature"] < float(35))

# mask all AF > 50 and < 3
data["Breathing frequency"] = data["Breathing frequency"].mask(data["Breathing frequency"] > float(50))
data["Breathing frequency"] = data["Breathing frequency"].mask(data["Breathing frequency"] < float(5))

# mask Saturatie (%) > 100 and <60
data["Saturation"] = data["Saturation"].mask(data["Saturation"] > float(100))
data["Saturation"] = data["Saturation"].mask(data["Saturation"] < float(60))

import os
##################################OOOOOOOASDASDASDASDAS

import plotly.graph_objs as go

fig_graph_vit_par = go.Figure()
fig_graph_vit_par.add_trace(go.Scatter(x=data["Date"], y=data["Saturation"],
                                       mode='lines+markers',
                                       name='Saturation (%)',
                                       line=dict(color='deepskyblue', width=2),
                                       connectgaps=True, ))
fig_graph_vit_par.add_trace(go.Scatter(x=data["Date"], y=data["Pulse"],
                                       mode='lines+markers',
                                       name='Pulse (bpm)',
                                       line=dict(color='red', width=2),
                                       connectgaps=True, ))
fig_graph_vit_par.add_trace(go.Scatter(x=data["Date"], y=data["Diastolic BP"],
                                       mode='lines+markers',
                                       name='Diastolic BP (mmHg)',
                                       line=dict(color='darkgreen', width=2),
                                       connectgaps=True, ))
fig_graph_vit_par.add_trace(go.Scatter(x=data["Date"], y=data["Systolic BP"],
                                       mode='lines+markers',
                                       name='Systolic BP (mmHg)',
                                       line=dict(color='forestgreen', width=2),
                                       connectgaps=True, ))
fig_graph_vit_par.add_trace(go.Scatter(x=data["Date"], y=data["Breathing frequency"],
                                       mode='lines+markers',
                                       name='AF (/min)',
                                       line=dict(color='steelblue', width=2),
                                       connectgaps=True, ))
fig_graph_vit_par.add_trace(go.Scatter(x=data["Date"], y=data["Temperature"],
                                    mode='lines+markers',
                                    name='Temp. (ᵒC)',
                                    line=dict(color='darkorange', width=2),
                                    connectgaps=True, ))

import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div([
    html.Center(
        html.H1('VITAL SIGNS'),
    ),
    html.Div([
            dcc.Graph(
                id="vit signs",
                figure=fig_graph_vit_par)
                    ]),
])

if __name__ == '__main__':
    app.run_server(debug=True)