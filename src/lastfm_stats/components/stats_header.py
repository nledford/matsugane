from datetime import datetime

from dash import html

from lastfm_stats.music.tracks import UniversalTracks


def last_updated() -> html.Div:
    now = datetime.now().time().strftime('%H:%M:%S')

    return html.Div(
        className='text-xs mb-1.5',
        children=[f'Last Updated: {now}']
    )


def stats_header(ut: UniversalTracks) -> html.Div:
    def tr(children):
        return html.Tr(children=children, className='group')

    def th(text: str):
        return html.Th(children=text, className='px-6 py-2 bg-neutral-900/75 group-hover:bg-neutral-900/50')

    def td(text: str):
        return html.Td(children=text, className='px-6 py-2 group-hover:bg-neutral-700/25')

    sh = html.Div(children=[
        last_updated(),
        html.Table(
            className='w-full overflow-hidden bg-neutral-800 border border-neutral-700/30 rounded tabular-nums text-left',
            children=[
                tr(children=[
                    th('Total Artists'),
                    td(f'{ut.total_artists}'),

                    th('Total Albums'),
                    td(f'{ut.total_albums}'),

                    th('Total Tracks'),
                    td(f'{ut.total_tracks}'),

                    th('Total Plays'),
                    td(f'{ut.total_plays}'),
                ]),
                tr(children=[
                    th('Avg. Plays Per Artist'),
                    td(f'{ut.average_plays_per_artist}'),
                ])
            ])
    ])

    return sh
