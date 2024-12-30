from dash import dash_table

from music.tracks import UniversalTracks


def played_tracks_table(universal_tracks: UniversalTracks) -> dash_table:
    return dash_table.DataTable(
        data=universal_tracks.tracks_dataframe.to_dict('records'),
        style_header={
            'backgroundColor': 'rgb(30, 30, 30)',
            'color': 'white'
        },
        style_data={
            'backgroundColor': 'rgb(50, 50, 50)',
            'color': 'white'
        },
        page_size=10
    )
