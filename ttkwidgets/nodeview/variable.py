from copy import copy


class NodeVar:
    def __init__(self, name, data=None, connections=None):
        """
        Node representation for the NodeView widget.

        :param name: name of the Node.
        :param data: dict of data for the node. Default : {}
        :param connections: connections from this node to other nodes. Default : []
        """
        if connections is None:
            connections = []
        if data is None:
            data = {}
        self.name = name
        self.connections = connections
        self.data = data

        self.traces = {"read": [],
                       "write": [],
                       "unset": []}

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
        self.connections.append(node)
        if bidirectional:
            node.connections.append(self)

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
