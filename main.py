from dash import Dash, html, dcc, callback, Input, Output

from components.page_header import page_header
from components.stats_header import stats_header
from music import treemap
from music.tracks import UniversalTracks

# Fetches and stores tracks from last.fm
universal_tracks = UniversalTracks.build()

treemap_fig = treemap.build_treemap(universal_tracks.treemap_dataframe)


@callback(
    # stats header
    Output('stats-header', 'children'),
    # treemap
    Output('lastfm-treemap', 'figure'),
    Input('refresh-button', 'n_clicks'),
)
def refresh_data(clicks):
    universal_tracks.fetch_tracks()

    return (
        stats_header(universal_tracks),
        treemap.build_treemap(universal_tracks.treemap_dataframe)
    )


external_scripts = [
    {'src': 'https://cdn.tailwindcss.com'}
]

# Initialize the app
app = Dash(__name__,
           external_scripts=external_scripts,
           title="Last.fm Stats",
           )

refresh_btn = html.Button(children='Refresh', id='refresh-button',
                          className='border border-neutral-700 bg-neutral-800 hover:bg-neutral-700/75 rounded py-1 px-2'),

app.layout = html.Div(
    className='bg-neutral-900 text-neutral-200',
    children=html.Div(
        className='container mx-auto py-5',
        children=[
            page_header(refresh_btn),
            html.Div(children=stats_header(universal_tracks), id='stats-header'),
            # dash_table.DataTable(data=df.to_dict('records'), page_size=10),
            dcc.Graph(id='lastfm-treemap', figure=treemap_fig, className='border border-neutral-700 my-5'),
        ]
    )
)

refresh_data(0)

# Run the app
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8077)
