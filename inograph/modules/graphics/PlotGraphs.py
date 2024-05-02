import random
import plotly
import plotly.graph_objects as go


def PlotGraphs(graphDicts, title='Untitled', save=None):
    fig = go.Figure()
    multipleGraph = len(graphDicts) >= 1
    for d in graphDicts:
        c = random.choice(plotly.colors.DEFAULT_PLOTLY_COLORS)
        for l in d['Edges'].values():
            descriptionS = {k: v for k, v in l.items() if k != 'ID' and k != 'Vertices' and 'Location' not in k and 'Target' not in k and v}
            descriptionT = {k: v for k, v in l.items() if k != 'ID' and k != 'Vertices' and 'Location' not in k and 'Source' not in k and v}
            fig.add_trace(go.Scattermapbox(
                mode="markers+lines",
                lon=[l["Source"]["Location"][1], l["Target"]["Location"][1]],
                lat=[l["Source"]["Location"][0], l["Target"]["Location"][0]],
                text=[str(descriptionS), str(descriptionT)],
                name=l['ID'],
                marker={'size': 10, "color": "black" if multipleGraph else None},
                line={"color": c if multipleGraph else None}
            ))
    fig.update_layout(legend_title_text=title)
    fig.update_layout(
        margin={'l': 0, 't': 0, 'b': 0, 'r': 0},
        mapbox={'center': {'lon': 10, 'lat': 10}, 'style': "open-street-map", 'zoom': 1})
    fig.show()
    if save: fig.write_html(save)
