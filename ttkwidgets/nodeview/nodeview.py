import tkinter as tk
from collections import namedtuple
import math
from ttkwidgets.nodeview import NodeVar


Element = namedtuple("Element", ["id", "coords"])
BezierElement = namedtuple("BezierElement", ["id", "nodes"])



class NodeView(tk.Canvas):
    def __init__(self, master=None, **kwargs):
        super(NodeView, self).__init__(master, **kwargs)
        self.nodes = {}
        self.connections = []
        self.first_node_of_connection = None
        self._bezier_id = 0
        self.selected_node = None
        self.bind('<Button-1>', self._select_node)
        self.bind('<B1-Motion>', self._on_node_drag)

    def create_node(self, coords, node_name, node_data=None, node_connections=None,
                    tags=None, state=tk.NORMAL, text_anchor=tk.NW):
        """
        Creates a Node on the NodeView Canvas.
        
        :param coords: 2-tuple x, y of canvas coordinates to put the node at
        :param node_name: Unique name for the node
        :param node_data: dictionary of data to store in the node
        :param node_connections: connections of the created node to other existing nodes of the graph
        :param tags: additional tags to be added to the created node
        :param state: tkinter state of the node
        :param text_anchor: anchor point for the node name text item
        
        :returns: item identifier
        """
        if node_data is None:
            node_data = {}
        if node_connections is None:
            node_connections = []
        if tags is None:
            tags = []
        tags.append(node_name)
        tags.append("nodeitem")
        rectangle_bbox = list(coords) + [coords[0] + 60, coords[1] + 30]
        text_pos = [coords[0] + 8, coords[1] + 1]
        rectangle_id = self.create_rectangle(rectangle_bbox, tags=tags,
                                             state=state)
        text_id = self.create_text(text_pos, state=state, text=node_name, 
                                   anchor=text_anchor)
        self.nodes[node_name] = {"variable": NodeVar(node_name, node_data, node_connections),
                                 "element_ids": [Element(rectangle_id, rectangle_bbox),
                                                 Element(text_id, text_pos)],
                                 "bezier_ids": []}
        return node_name

    def _on_node_drag(self, event, node=None):
        if node is None and self.selected_node is None:
            node = self.identify(event.x, event.y)
        elif node is None:
            node = self.selected_node
            
        for e in self.nodes[node]["element_ids"]:
            eid = e.id
            coords = e.coords.copy()
            coords[0] = coords[0] + event.x
            coords[1] = coords[1] + event.y
            if len(coords) == 4:
                coords[2] = coords[2] + event.x
                coords[3] = coords[3] + event.y
            self.coords(eid, *coords)

    def _create_connection(self, event, node=None):
        if node is None and self.selected_node is None:
            node = self.identify(event.x, event.y)
        elif node is None:
            node = self.selected_node
                
        if self.first_node_of_connection is None:
            self.first_node_of_connection = (node, (event.x, event.y))
        else:
            cp1 = self.first_node_of_connection[1]
            cp4 = (event.x, event.y)
            x_avg = (cp4[0] - cp1[0]) / 2
            cp2 = (x_avg, cp1[1])
            cp3 = (x_avg, cp4[1])
            bezier_id = self.create_bezier([cp1, cp2, cp3, cp4])
            node_a = self.first_node_of_connection[0]
            node_b = node
            self.nodes[node_a]["bezier_ids"].append(BezierElement(bezier_id, [node_a, node_b]))
            self.nodes[node_a]["variable"].connect(self.nodes[node]["variable"])
            self.first_node_of_connection = None

    def _select_node(self, event):
        radius = 15
        x1 = event.x - radius
        x2 = event.x + radius
        y1 = event.y - radius
        y2 = event.y + radius
        node = self.find_overlapping(x1, y1, x2, y2)
        self.selected_node = None
        if node:
            node = node[0]
            tags = list(self.gettags(node))
            if "nodeitem" in tags:
                self.selected_node = tags[0]
        print(self.selected_node)
            

    def create_bezier(self, control_points):
        """
        Creates a bezier curve out of the provided control_points
        :param control_points: list of control points for the bezier
        :returns: item identifier for the bezier curve
        """
        def bernstein(idx, degree):
            m = degree
            binom = math.comb(m, idx)
            return lambda u: binom * u ** idx * (1 - u) ** (m - idx)

        def bezier(cpts, u):
            rv = [0, 0]
            for idx, cp in enumerate(cpts):
                rv[0] += bernstein(idx, len(cpts))(u) * cp[0]
                rv[1] += bernstein(idx, len(cpts))(u) * cp[1]
            return rv

        tag_name = f"bezier{self._bezier_id}"
        self._bezier_id += 1

        # Start x and y coordinates, when t = 0
        x_start = control_points[0][0]
        y_start = control_points[0][1]

        # loops through
        n = 50
        for i in range(n):
            t = i / n
            x, y = bezier(control_points, t)

            self.create_line(x, y, x_start, y_start, tags=[tag_name])
            # updates initial values
            x_start = x
            y_start = y
        return tag_name
    
    def identify(self, x, y):
        """
        Identifies the closest node to the provided coordinates
        
        :param x: x coordinate
        :param y: y coordinate
        :returns: None if no nodes are found, else the closest node item identifier.
        """
        closest = self.find_closest(x, y)
        if "nodeitem" in self.gettags(closest):
            tags = list(self.gettags(closest))
            tags.remove("nodeitem")
            return tags[0]
        else:
            return


if __name__ == '__main__':
    root = tk.Tk()
    gui = NodeView(root, width=500, height=500)
    gui.create_node((5, 5), "test")
    gui.create_node((150, 5), "test2")
    gui.pack()
    root.mainloop()
