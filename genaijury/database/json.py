import json
from genaijury.database.base import DatabaseInterface
from typing import List, Dict
import os

class JSONFileInterface(DatabaseInterface):
    def __init__(self, filepath):
        self.filepath = filepath
        self.connect()

    def connect(self):
        # Ensure the file exists
        if not os.path.exists(self.filepath):
            with open(self.filepath, 'w') as file:
                json.dump([], file)

    def create(self, data):
        documents = self._read_file()
        documents.append(data)
        self._write_file(documents)
        return len(documents) - 1  # Assuming index as ID

    def read(self, query):
        documents = self._read_file()
        # Simple query implementation: filter by key-value pairs
        return [doc for doc in documents if all(item in doc.items() for item in query.items())]

    def update(self, query, data):
        documents = self._read_file()
        updated_count = 0
        for doc in documents:
            if all(item in doc.items() for item in query.items()):
                doc.update(data)
                updated_count += 1
        self._write_file(documents)
        return updated_count

    def delete(self, query):
        documents = self._read_file()
        new_documents = [doc for doc in documents if not all(item in doc.items() for item in query.items())]
        self._write_file(new_documents)
        return len(documents) - len(new_documents)

    def _read_file(self) -> List[Dict]:
        with open(self.filepath, 'r') as file:
            return json.load(file)

    def _write_file(self, documents):
        with open(self.filepath, 'w') as file:
            json.dump(documents, file, indent=4)
