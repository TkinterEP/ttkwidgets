from copy import copy


class NodeVar:
    def __init__(self, name, data=None, connections=None):
        """
        Node representation for the NodeView widget.

        :param name: name of the Node.
        :param data: dict of data for the node. Default : {}
        :param connections: connections from this node to other nodes. Default : set()
        """
        if connections is None:
            connections = set()
        if data is None:
            data = {}
        self.name = name
        self.connections = set(connections)
        self.data = data

        self.traces = {"read": [],
                       "write": [],
                       "unset": []}

    def __eq__(self, other):
        if isinstance(other, NodeVar):
            return self.name == other.name
        elif isinstance(other, str):
            return self.name == other
        else:
            raise ValueError()
    
    def __hash__(self):
        return hash(self.name)

    def get(self):
        """
        Gets the info about this node.

        :return: Dictionary containing the name, data and connections of this node.
        """
        for _, cb in self.traces["read"]:
            cb()
        return {"name": self.name,
                "data": self.data,
                "connections_name": [n.name for n in self.connections],
                "connections_data": [n.data for n in self.connections]}

    def set(self, name=None, data=None):
        """
        Sets the name and data for this node.

        :param name: New name for the node. Replaces the old one.
        :param data: data dictionary to update this node's data with.
        :return: None
        """
        for _, cb in self.traces["write"]:
            cb()

        if name is not None:
            self.name = name

        if data is not None:
            self.data.update(data)

    def connect(self, node, bidirectional=False):
        """
        Connects this node to another.

        :param node: The node to connect to.
        :param bidirectional: Whether the connection should be bidirectional.
                              Default : False
                              If unidirectional, the connection is made from this node to the target node.
        :return: None
        """
        self.connections.add(node)
        if bidirectional:
            node.connections.add(self)

    def trace_add(self, mode, callback):
        """
        Define a trace callback for the variable.

        Mode is one of "read", "write", "unset", or a list or tuple of
        such strings.
        Callback must be a function which is called when the variable is
        read, written or unset.

        Return the name of the callback.
        """
        if isinstance(mode, str):
            mode = [mode]
        for m in mode:
            self.traces[m].append((callback.__name__, callback))
        return callback.__name__

    def trace_remove(self, mode, cbname):
        """
        Delete the trace callback for a variable.

        Mode is one of "read", "write", "unset" or a list or tuple of
        such strings.  Must be same as were specified in trace_add().
        cbname is the name of the callback returned from trace_add().
        """
        if isinstance(mode, str):
            mode = [mode]

        for m in mode:
            indices = [i for i, cb in enumerate(self.traces[m]) if cb[0] == cbname]
            for nb, i in enumerate(indices):
                self.traces[m].pop(i - nb)

    def trace_info(self):
        """
        Return all trace callback information.
        """
        return copy(self.traces)


class GraphVar:
    def __init__(self, nodes=None):
        """
        Node representation for the NodeView widget.

        :param nodes: nodes list to store in this variable
        """
        if nodes is None:
            nodes = []
            
        self.nodes = nodes

        self.traces = {"read": [],
                       "write": [],
                       "unset": []}

    def __len__(self):
        return len(self.nodes)

    def __getitem__(self, item):
        for _, cb in self.traces["read"]:
            cb()
            
        if isinstance(item, int):
            return self.nodes[item]
        elif isinstance(item, (NodeVar, str)):
            return [n for n in self.nodes if n == item][0]
        else:
            raise KeyError()

    def get(self):
        """
        Gets the info about this graph.

        :return: Dictionary containing the name, data and connections of this node.
        """
        for _, cb in self.traces["read"]:
            cb()
        return self.nodes

    def set(self, index, node):
        """
        Sets the name and data for this node.

        :param index: index of the node to set.
        :param node: NodeVar of the node to replace the one at index index.
        :returns: None
        """
        for _, cb in self.traces["write"]:
            cb()

        self.nodes[index] = node
    
    def add(self, *nodes):
        """
        Adds nodes to the graph
        
        :param nodes: nodes instances to add to the graph
        """
        for _, cb in self.traces["write"]:
            cb()
        nodes = filter(lambda n: n not in self.nodes, nodes)
        self.nodes.extend(nodes)

    def construct_graph(self):
        """
        Constructs the graph as intertwined python dictionaries.
        
        Nodes are keys, and the value is another dict containing 
        the connected nodes, and their connections
        """
        graph = {}
        done_nodes = []
        def __construct_graph(graph, node):
            g = {}
            nonlocal done_nodes
            done_nodes.append(node)
            graph[node] = {__construct_graph(g, n) for n in node.connections}
            return graph
                
        
        for node in self.nodes:
            if node not in done_nodes:
                __construct_graph(graph, node)
        return graph

    def trace_add(self, mode, callback):
        """
        Define a trace callback for the variable.

        Mode is one of "read", "write", "unset", or a list or tuple of
        such strings.
        Callback must be a function which is called when the variable is
        read, written or unset.

        Return the name of the callback.
        """
        if isinstance(mode, str):
            mode = [mode]
        for m in mode:
            self.traces[m].append((callback.__name__, callback))
        return callback.__name__

    def trace_remove(self, mode, cbname):
        """
        Delete the trace callback for a variable.

        Mode is one of "read", "write", "unset" or a list or tuple of
        such strings.  Must be same as were specified in trace_add().
        cbname is the name of the callback returned from trace_add().
        """
        if isinstance(mode, str):
            mode = [mode]

        for m in mode:
            indices = [i for i, cb in enumerate(self.traces[m]) if cb[0] == cbname]
            for nb, i in enumerate(indices):
                self.traces[m].pop(i - nb)

    def trace_info(self):
        """
        Return all trace callback information.
        """
        return copy(self.traces)