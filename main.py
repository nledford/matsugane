from dash import Dash, html, dcc, callback, Input, Output

from music import treemap
from music.tracks import UniversalTracks

# Fetches and stores tracks from last.fm
universal_tracks = UniversalTracks.build()

treemap_fig = treemap.build_treemap(universal_tracks.treemap_dataframe)


def stats_header(ut: UniversalTracks) -> html:
    return html.Table(
        className='w-full overflow-hidden bg-neutral-800 border border-neutral-700/30 rounded tabular-nums text-left',
        children=[
            html.Tr(children=[
                html.Th(children='Total Artists', className='px-6 py-3'),
                html.Td(children=ut.total_artists),

                html.Th(children='Total Albums'),
                html.Td(children=ut.total_albums),

                html.Th(children='Total Tracks'),
                html.Td(children=ut.total_tracks),

                html.Th(children='Total Plays'),
                html.Td(children=ut.total_plays),
            ]),
            html.Tr(children=[
                html.Th(children='Avg. Plays Per Artist', className='px-6 py-3'),
                html.Td(children=ut.average_plays_per_artist),
            ])
        ])


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
            html.Div(children=stats_header(universal_tracks), id='stats-header'),
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
    app.run(debug=True, host="0.0.0.0", port=8077)
