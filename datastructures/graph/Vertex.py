class Vertex:
    
    def __init__(self, data, idx = None):
        self.data = data
        self.idx = idx
        
    def get_data(self):
        return self.data

    def get_index(self):
        return self.idx

    """
    def __hash__(self):
        return 
    implement with self.index if needed
    """

    def has_index(self):
        return self.idx is not None

    def has_hash(self):
        return self.idx is not None

    def __hash__(self):
        assert self.has_index()
        return self.idx

    def __str__(self):
        return 'vertex :'+str(self.idx)




