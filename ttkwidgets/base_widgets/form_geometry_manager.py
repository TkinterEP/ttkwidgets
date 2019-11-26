class Form:
    def __init__(self, widget):
        self.__slaves = []
        self.__widget = widget
    
    def form(self):
        pass
    
    def form_configure(self):
        pass
    
    def form_config(self, *args, **kwargs):
        return self.form_configure(*args, **kwargs)
    
    def form_forget(self):
        pass
    
    def form_info(self):
        pass
    
    def form_propagate(self):
        pass
    
    def form_slaves(self):
        pass