import pandas as pd
import plotly.graph_objects as go
from dash import Dash, html, dcc, callback, Input, Output

from music.tracks import UniversalTracks
from music.treemap import TreemapNode

universal_tracks = UniversalTracks()
universal_tracks.fetch_tracks()


def build_treemap(treemap_data: TreemapNode):
    print(treemap_data)
    # Building nested dataframe for artists and albums
    df = pd.DataFrame(columns=['ids', 'labels', 'parents', 'plays'])
    for node in sorted(treemap_data.children, key=lambda x: x.sort_value):
        df_artist = {
            'ids': node.id,
            'labels': node.value,
            'parents': node.parent,
            'plays': sum([child.plays for child in node.children]) if node.children else node.plays,
        }
        df.loc[len(df)] = df_artist
        for album in sorted(node.children, key=lambda x: x.sort_value):
            df_album = {
                'ids': album.id,
                'labels': album.value,
                'parents': album.parent,
                'plays': album.plays,
            }
            df.loc[len(df)] = df_album

    # df["Total Plays"] = f'Total Plays | {len(artists)} artists | {len(tracks)} tracks | {sum(plays)} plays'

    fig = go.Figure(go.Treemap(
        branchvalues='total',
        labels=df.labels,
        parents=df.parents,
        ids=df.ids,
        values=df['plays'],
        hovertemplate='<br>'.join([
            '%{label}',
            '%{value} plays',
            '<extra></extra>',
        ]),
        texttemplate='<br>'.join([
            '%{label}',
            '%{value} plays',
        ]),
        root_color="orange",
    ))
    fig.update_layout(
        margin=dict(t=0, l=0, r=0, b=0),
        height=777,
    )

    return fig


default_fig = build_treemap(universal_tracks.treemap_data)


@callback(
    Output('lastfm-treemap', 'figure'),
    Input('refresh-button', 'n_clicks'),
)
def refresh_treemap(clicks):
    universal_tracks.fetch_tracks()
    return build_treemap(universal_tracks.treemap_data)


external_scripts = [
    {'src': 'https://cdn.tailwindcss.com'}
]

# Initialize the app
app = Dash(__name__,
           external_scripts=external_scripts
           )

app.layout = html.Div(
    className='bg-neutral-900 text-neutral-200',
    children=html.Div(
        className='container mx-auto py-5',
        children=[
            html.H1(children='Last.fm', className='text-2xl font-semibold'),
            html.Button(children='Refresh', id='refresh-button',
                        className='border border-neutral-700 bg-neutral-800 hover:bg-neutral-700/75 rounded py-1 px-2'),
            # dash_table.DataTable(data=df.to_dict('records'), page_size=10),
            # dcc.Graph(figure=fig, id="treemap", className='border border-neutral-700 my-5')
            dcc.Graph(id='lastfm-treemap', figure=default_fig, className='border border-neutral-700 my-5'),
        ]
    )
)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
