from aenum import Enum

import utils


class NodeType(Enum):
    ROOT = 1
    ARTIST = 2
    ALBUM = 3


class TreemapNode:
    def __init__(self, node_type: int, value: str, sort_value: str, plays: int, tracks: int, parent: str,
                 children=None):
        if children is None:
            children = []

        self.node_type = node_type
        self.id = utils.hash_str(str(node_type) + value.lower())
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
