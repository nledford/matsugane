from dash import html

from lastfm_stats.music.tracks import UniversalTracks


def played_tracks_table(ut: UniversalTracks) -> html.Div:
    wrapper = html.Div(
        className="relative overflow-hidden w-full overflow-y-auto "
        "border border-neutral-700/30 rounded max-h-80 text-sm"
    )

    header_row = html.Div(
        className="sticky top-0 left-0 right-0 w-full flex flex-row items-center",
        children=[
            cell(text=x, is_header_cell=True, is_time_cell=idx == 3)
            for idx, x in enumerate(ut.tracks_dataframe.columns.values)
        ],
    )

    played_tracks = html.Div(
        children=[
            html.Div(
                className="flex flex-row items-center bg-neutral-800 hover:bg-neutral-700/50 border-b border-neutral-700/30",
                children=[
                    cell(text=x, is_time_cell=idx == 3) for idx, x in enumerate(row)
                ],
            )
            for row in ut.tracks_dataframe.to_dict("split")["data"]
        ]
    )

    wrapper.children = [header_row, played_tracks]

    return wrapper


def cell(text: str, is_header_cell: bool = False, is_time_cell: bool = False):
    return html.Div(
        children=text,
        className=f"{'basis-[13%] text-center' if is_time_cell else 'basis-[29%]'} "
        f"{'font-bold bg-neutral-900/75 backdrop-blur' if is_header_cell else ''} "
        f"px-3 py-2 tabular-nums",
    )
