import plotly.plotly as py
import plotly.graph_objs as go 
from datetime import datetime
import pandas as pd
import plotly
plotly.tools.set_credentials_file(username='MiltonMartz', api_key='QUbjoGhTG410vsbrQFwy')
    
def GetPlot(isin, name):
    path = 'D:/data/csv/funds/Portfolio/'
    df = pd.read_csv(path + isin + '.csv', sep='\t' )
    df.date = [datetime.strptime(x, '%d/%m/%y').date() for x in df.date]
    trace = go.Scatter(x=list(df.date), y=list(df.value))

    data = [trace]
    layout = dict(
        title= isin + ' : ' + name,
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label='1m', step='month', stepmode='backward'),
                    dict(count=3, label='3m', step='month', stepmode='backward'),
                    dict(count=6, label='6m', step='month', stepmode='backward'),
                    dict(count=9, label='9m', step='month', stepmode='backward'),
                    dict(count=1, label='1y', step='year', stepmode='backward'),
                    dict(step='all')
                ])
            ),
            rangeslider=dict(visible=True),
            type='date'
        )
    )

    fig = dict(data=data, layout=layout)
    return fig


if __name__ == '__main__':


    isin = 'LU0260869739'
    name = 'Franklin US Opps Fund A (acc)'
    GetPlot(isin, name)