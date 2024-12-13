from dash import Dash, html, dcc, callback, Input, Output

from music import treemap
from music.tracks import UniversalTracks

# Fetches and stores tracks from last.fm
universal_tracks = UniversalTracks.build()

treemap_fig = treemap.build_treemap(universal_tracks.treemap_dataframe)


@callback(
    Output('lastfm-treemap', 'figure'),
    Input('refresh-button', 'n_clicks'),
)
def refresh_treemap(clicks):
    universal_tracks.fetch_tracks()
    return treemap.build_treemap(universal_tracks.treemap_dataframe)


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
            dcc.Graph(id='lastfm-treemap', figure=treemap_fig, className='border border-neutral-700 my-5'),
        ]
    )
)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
