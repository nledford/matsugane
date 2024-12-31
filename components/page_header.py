from dash import html


def page_header(btn: tuple[html.Button]):
    return html.Div(
        className='sticky top-0 left-0 right-0 bg-neutral-900/75 backdrop-blur border-b border-neutral-700/75 z-50',
        children=[
            html.Div(
                className='container mx-auto h-14 flex flex-row items-center justify-between z-50',
                children=[
                    html.Div(children=[
                        html.H1(children='Last.fm Stats', className='text-2xl font-bold'),
                    ]),
                    html.Div(children=btn)
                ])
        ])
