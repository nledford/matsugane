from dash import html

from music.tracks import UniversalTracks


def played_tracks_table(ut: UniversalTracks) -> html.Div:
    wrapper = html.Div(className='relative overflow-hidden w-full overflow-y-auto '
                                 'border border-neutral-700/30 rounded h-80'
                       )

    header_row = html.Div(
        className='sticky top-0 left-0 right-0 w-full flex flex-row items-center',
        children=[
            html.Div(children=x,
                     className='bg-neutral-900/75 backdrop-blur basis-1/4 font-bold px-3 py-2')
            for x in ut.tracks_dataframe.columns.values
        ]
    )

    played_tracks = html.Div(children=[
        html.Div(
            className='flex flex-row items-center bg-neutral-800 hover:bg-neutral-700/50 border-b border-neutral-700/30',
            children=[
                html.Div(
                    className='basis-1/4 px-3 py-2',
                    children=x
                )
                for x in row
            ])
        for row in ut.tracks_dataframe.to_dict('split')['data']
    ])

    wrapper.children = [header_row, played_tracks]

    return wrapper
