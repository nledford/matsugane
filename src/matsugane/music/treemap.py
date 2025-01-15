from typing import NewType

import pandas as pd
import plotly.graph_objects as go
from aenum import Enum
from attrs import define

from matsugane import utils

NodePlays = NewType("NodePlays", int)
NodeTracks = NewType("NodeTracks", int)


class NodeType(Enum):  # pyright: ignore [reportGeneralTypeIssues]
    ROOT = 1
    ARTIST = 2
    ALBUM = 3
    TRACK = 4


@define
class TreemapNode:
    node_type: NodeType
    id = utils.generate_cuid2()
    parent: str
    value: str
    sort_value: str
    plays: int
    tracks: int
    children: list["TreemapNode"] = []

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
    fig = go.Figure(
        go.Treemap(
            branchvalues="total",
            labels=df.labels,
            parents=df.parents,
            ids=df.ids,
            values=df["plays"],
            hovertemplate="<br>".join(
                [
                    "%{label}",
                    "%{value} plays",
                    "<extra></extra>",
                ]
            ),
            texttemplate="<br>".join(
                [
                    "%{label}",
                    "%{value} plays",
                ]
            ),
            # root_color="orange",
        )
    )
    fig.update_layout(
        margin=dict(t=0, l=0, r=0, b=0),
        height=789,
    )

    return fig
