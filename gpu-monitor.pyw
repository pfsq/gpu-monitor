#! usr/bin/env python

import gpuwatch
import plotly.plotly as py
import plotly.tools as tls
from plotly.graph_objs import *
import datetime
from time import strftime, sleep

def main():
    # Add traces of temperature, memory and fan usage.
    trace1 = Scatter(x=[],
                     y=[],
                     mode='lines+markers',
                     line=Line(shape='spline', color='lime'),
                     marker=Marker(color='black', line=Line(color='lime', width=2)),
                     stream=Stream(token=stream_ids[0], maxpoints=60))
    trace2 = Scatter(x=[],
                     y=[],
                     yaxis='y2',
                     mode='lines',
                     line=Line(shape='vh', color='cyan'),
                     stream=Stream(token=stream_ids[1], maxpoints=60))
    data = Data([trace1, trace2])
    
    # Add layout object
    layout = Layout(title='GeForce GTX460 GPU real-time monitor',
                    font=Font(color='white'),
                    showlegend=False,
                    xaxis=XAxis(gridcolor='darkgreen'),
                    yaxis=YAxis(title='Temperature (C)', 
                                titlefont=Font(color='lime'),
                                tickfont=Font(color='lime'), 
                                gridcolor='darkgreen'),
                    yaxis2=YAxis(title='Fan speed (%)',
                                 overlaying='y',
                                 side='right',
                                 titlefont=Font(color='cyan'),
                                 tickfont=Font(color='cyan'),
                                 gridcolor='darkgreen'),
                    paper_bgcolor='black',
                    plot_bgcolor='black')

    # Make a figure object
    fig = Figure(data=data, layout=layout)

    # (@) Send fig to Plotly, initialize streaming plot, open new tab
    unique_url = py.plot(fig, filename='streaming/gpu-monitor', auto_open=False)

    # Make 1st instance of the stream link object
    s1 = py.Stream(stream_ids[0])

    # Make 2nd instance of the stream link object
    s2 = py.Stream(stream_ids[1])

    # Open both streams
    s1.open()
    s2.open()

    # Loop
    while True:
        # Current time on x-axis, GPU temperature on y-axis
        x = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        y1 = gpuwatch.Gpu_Temp()
        y2 = gpuwatch.Fan_Speed()

        # Write to Plotly stream!
        s1.write(dict(x=x, y=y1))
        s2.write(dict(x=x, y=y2))

        sleep(10)

if __name__ == "__main__":
    from sys import exit
    stream_ids = ["lj8k5sz7sx", "upxpfny8c1"]
    exit(main())