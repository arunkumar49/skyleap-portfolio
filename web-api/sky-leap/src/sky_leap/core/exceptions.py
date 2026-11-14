

class UnsupportedFileTypeError(Exception):
    
    def __init__(self, filetype: str):
        self.filetype = filetype
        
    def __str__(self):
        return f"Unsupported file type: {self.filetype or 'unknown'}"


class StorageError(Exception):

    def __init__(self, key: str):
        self.key = key

    def __str__(self):
        return f"Could not store object: {self.key}"