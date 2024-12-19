from dash import Dash, html, dcc, callback, Input, Output

from music import treemap
from music.tracks import UniversalTracks

# Fetches and stores tracks from last.fm
universal_tracks = UniversalTracks.build(False)

treemap_fig = treemap.build_treemap(universal_tracks.treemap_dataframe)


@callback(
    # stats header
    Output('total-tracks', 'children'),
    Output('avg-plays-per-artist', 'children'),
    # treemap
    Output('lastfm-treemap', 'figure'),
    Input('refresh-button', 'n_clicks'),
)
def refresh_data(clicks):
    universal_tracks.fetch_tracks()

    total_tracks = f'{universal_tracks.total_tracks} track{"" if universal_tracks.total_tracks == 1 else "s"}'
    avg_plays_per_artist = f'{universal_tracks.average_plays_per_artist} avg. play{"" if universal_tracks.average_plays_per_artist == 1.0 else 's'} per artist'

    return (
        total_tracks,
        avg_plays_per_artist,
        treemap.build_treemap(universal_tracks.treemap_dataframe)
    )


external_scripts = [
    {'src': 'https://cdn.tailwindcss.com'}
]

# Initialize the app
app = Dash(__name__,
           external_scripts=external_scripts
           )

stats_header = html.Ul(
    className='flex flex-row items-center gap-1',
    children=[
        html.Li(children=0, id='total-tracks'),
        html.Li(children=0, id='avg-plays-per-artist'),
    ])

app.layout = html.Div(
    className='bg-neutral-900 text-neutral-200',
    children=html.Div(
        className='container mx-auto py-5',
        children=[
            html.H1(children='Last.fm', className='text-2xl font-semibold'),
            html.Button(children='Refresh', id='refresh-button',
                        className='border border-neutral-700 bg-neutral-800 hover:bg-neutral-700/75 rounded py-1 px-2'),
            html.Div(children=stats_header, id='stats-header'),
            # html.Div(children=f'Avg. Plays Per Artist: {universal_tracks.average_plays_per_artist}'),
            # dash_table.DataTable(data=df.to_dict('records'), page_size=10),
            # dcc.Graph(figure=fig, id="treemap", className='border border-neutral-700 my-5')
            dcc.Graph(id='lastfm-treemap', figure=treemap_fig, className='border border-neutral-700 my-5'),
        ]
    )
)

refresh_data(0)

# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=8077)
