from typing import NewType, Optional

import pandas as pd
import plotly.graph_objects as go
from aenum import Enum

from lastfm_stats import utils

NodePlays = NewType('NodePlays', int)
NodeTracks = NewType('NodeTracks', int)


class NodeType(Enum):  # pyright: ignore [reportGeneralTypeIssues]
    ROOT = 1
    ARTIST = 2
    ALBUM = 3
    TRACK = 4


class TreemapNode:
    def __init__(self,
                 node_type: int,
                 value: str,
                 sort_value: str,
                 plays: NodePlays,
                 tracks: NodeTracks,
                 parent: str,
                 children: Optional[list['TreemapNode']] = None):
        if children is None:
            children = []

        self.node_type = node_type
        self.id = utils.generate_cuid2()
        self.parent = parent
        self.value = value
        self.sort_value = sort_value
        self.plays = plays
        self.tracks = tracks
        self.children: list[TreemapNode] = children

    def __repr__(self):
        return f'TreemapNode({self.value}, {self.plays}, {self.tracks}, {self.children})'

    @property
    def node_type_label(self):
        match self.node_type:
            case NodeType.ROOT:
                return ""
            case NodeType.ARTIST:
                return "Artist: "
            case NodeType.ALBUM:
                return "Album: "


def build_treemap(df: pd.DataFrame):
    fig = go.Figure(go.Treemap(
        branchvalues='total',
        labels=df.labels,
        parents=df.parents,
        ids=df.ids,
        values=df['plays'],
        hovertemplate='<br>'.join([
            '%{label}',
            '%{value} plays',
            '<extra></extra>',
        ]),
        texttemplate='<br>'.join([
            '%{label}',
            '%{value} plays',
        ]),
        # root_color="orange",
    ))
    fig.update_layout(
        margin=dict(t=0, l=0, r=0, b=0),
        height=789,
    )

    return fig
