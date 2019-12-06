import json
import pathlib
import tkinter as tk


class ConfigSerializer:
    def deserialize(self, file_handler):
        """
        Deserializes the contents of the provided file_handler, and returns a dictionary of
        tkinter.Variable instances
        """
        raise NotImplementedError("Method 'deserialize' is not Implemented in class {}".format(self.__class__.__name__))
    
    def serialize(self, file_handler, data):
        """
        Serializes the content of the data dictionary into the provided file_handler.
        """
        raise NotImplementedError("Method 'serialize' is not Implemented in class {}".format(self.__class__.__name__))

    def from_tkvar(self, item):
        """
        Returns the value from a tkinter.Variable instance
        """
        return item.get()

    def to_tkvar(self, item):
        """
        Returns a tkinter.Variable instance based on the python type of the item.
        """
        if isinstance(item, (bool, int)):
            var = tk.IntVar()
            item = int(item)
        elif isinstance(item, float):
            var = tk.DoubleVar()
        elif isinstance(item, str):
            var = tk.StringVar()
        var.set(item)
        return var


class JSONSerializer(ConfigSerializer):
    def deserialize(self, file_handler):
        data = json.load(file_handler)
        rv = {}
        for key, value in data.items():
            rv[key] = self.to_tkvar(value)
        return rv
    
    def serialize(self, file_handler, data):
        dump = {}
        for key, value in data.items():
            dump[key] = self.from_tkvar(value)
        json.dump(dump, file_handler, indent=4)


class Config:
    """
    Singleton to hold config information.
    
    Config can be loaded/saved into various formats, but defaults to JSON.
    """
    __instance = None
    
    class __Config:        
        def __init__(self, path, serializer=None):
            """
            Config holder for tkinter.Variable instances
            
            :param path: str or pathlib.Path object. path to the file that configuration will be loaded/saved to
            :param serializer: ttkwidgets.ConfigSerializer instance to save/load data
            """
            if serializer is None:
                serializer = JSONSerializer
            self.serializer = serializer()
            self._path = path
            self.data = {}
        
        def __getitem__(self, item):
            return self.data[item]
        
        @property
        def path(self):
            return self._path
        
        @path.setter
        def path(self, value):
            if isinstance(value, str):
                self._path = pathlib.Path(value)
            elif isinstance(value, pathlib.Path):
                self._path = value
            else:
                raise TypeError("Config.path attribute must be a string or pathlib.Path instance.")
        
        def load(self):
            with self.path.open('r') as f:
                self.data = self.serializer.deserialize(f)
        
        def save(self):
            with self.path.open('w') as f:
                self.serializer.serialize(f, self.data)

    def __new__(cls, *args, **kwargs):
        if not Config.__instance:
            cls.__instance = Config.__Config(*args, **kwargs)
        return cls.__instance

    def __getattr__(self, name):
        return getattr(self.__instance, name)
    
    def __setattr__(self, name, value):
        return setattr(self.__instance, name, value)
