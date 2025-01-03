from dash import Dash, html, dcc, callback, Input, Output

from lastfm_stats.components.page_header import page_header
from lastfm_stats.components.played_tracks_table import played_tracks_table
from lastfm_stats.components.stats_header import stats_header
from lastfm_stats.music import treemap
from lastfm_stats.music.tracks import UniversalTracks

# Fetches and stores tracks from last.fm
universal_tracks = UniversalTracks.build()

treemap_fig = treemap.build_treemap(universal_tracks.treemap_dataframe)


@callback(
    # stats header
    Output('stats-header', 'children'),
    # played tracks table
    Output('played_tracks_table', 'children'),
    # treemap
    Output('lastfm-treemap', 'figure'),
    Input('refresh-button', 'n_clicks'),
)
def refresh_data(clicks):
    universal_tracks.fetch_tracks()

    return (
        stats_header(universal_tracks),
        played_tracks_table(universal_tracks),
        treemap.build_treemap(universal_tracks.treemap_dataframe)
    )


# Initialize the app
app = Dash(__name__,
           external_scripts=[
               {'src': 'https://cdn.tailwindcss.com'}
           ],
           title="Last.fm Stats",
           )

refresh_btn = html.Button(children='Refresh', id='refresh-button',
                          className='border border-neutral-700 bg-neutral-800 hover:bg-neutral-700/75 rounded py-1 px-2'),

app.layout = html.Div(
    className='relative bg-neutral-900 text-neutral-200',
    children=[
        page_header(refresh_btn),
        html.Div(
            className='container mx-auto py-5 z-0',
            children=[
                html.Div(children=stats_header(universal_tracks),
                         id='stats-header',
                         className='mb-5'),
                html.Div(children=played_tracks_table(universal_tracks),
                         id='played_tracks_table',
                         className='mb-5 z-0'),
                dcc.Graph(id='lastfm-treemap',
                          figure=treemap_fig,
                          className='border border-neutral-700 my-5'),
            ]
        )
    ]
)


def main():
    refresh_data(0)
    app.run(debug=True, host="0.0.0.0", port=8077)  # pyright: ignore [reportArgumentType]


# Run the app
if __name__ == '__main__':
    main()
