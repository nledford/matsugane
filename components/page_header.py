from dash import html


def page_header(btn: tuple[html.Button]):
    return html.Div(
        className='flex flex-row items-center justify-between pb-5',
        children=[
            html.Div(children=[
                html.H1(children='Last.fm Stats', className='text-2xl font-bold'),
            ]),
            html.Div(children=btn)
        ])
