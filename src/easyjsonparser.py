import json, os
from pathlib import Path


"""
Author: Magdy Ismail
Easy Json Parser
easy way to access or 
parsing json content
using json file as a config file
using with web services or apis

--
Example 1 with static files:

config = EasyJsonParser()
db_hostname = config('database.mysql.host')
or
db_hostname = config.get('database.mysql.host')
or
db_hostname = config('database', 'mysql', 'host')

--
Example 2 using with streaming
buf = '''{
    "data": {
        "items": [
            {"id": 1, "name": "Item 1"}
        ]
    }
}'''

jparser = EasyJsonParserIO(buf)
items = parser('data.items')

--
Example 3:
import requests

res = requests.get('http://example.com/api/v1/items')
jparser = EasyJsonParserIO(res.text)
items = jparser('data.items')
"""

class WrongDirOrFilename(Exception):
    pass

class InvalidJsonFormat(Exception):
    pass


class EasyJsonParser:
    
    allowed_delimiters = {'.', ':',}
    
    def __init__(self, **kwargs):
        base_dir = kwargs['path'] if 'path' in kwargs else Path(__file__).resolve().parent.parent
        filename = kwargs['filename'] if 'filename' in kwargs else 'config'
        filename_without_ext = filename.split('.')[0]

        full_path = os.path.join(base_dir, f'{filename_without_ext}.json')
        
        if not os.path.exists(full_path):
            raise WrongDirOrFilename('Wrong directory or filename')

        with open(full_path, 'r') as f:
            try:
                self.file_content = json.loads(f.read())
            except json.decoder.JSONDecodeError:
                raise InvalidJsonFormat('Invalid json format')
    
    def add_delimiters(self, *args):
        self.allowed_delimiters.update(*args)
    
    def _determine_delimiter(self, syntax):
        for symbol in self.allowed_delimiters:
            if len(syntax.split(symbol)) > 1:
                return symbol
        return None

    def __call__(self, *args):
        if(len(args) > 1):
            keys = args
        else:
            determined_delimiter = self._determine_delimiter(args[0]) 
            delimiter = determined_delimiter if determined_delimiter is not None else '.'
            keys = args[0].split(delimiter)

        identifiers = ''
        for key in keys:
            identifiers += f'["{key}"]'
        try:
            return eval(f'{self.file_content}{identifiers}')
        except:
            return None

    def get(self, *args):
        return self(*args)
        
    def __str__(self):
        return f"{self.file_content}"
    
    __repr__ = __str__


class EasyJsonParserIO(EasyJsonParser):
    def __init__(self, buffer):
        try:
            self.file_content = json.loads(buffer)
        except json.decoder.JSONDecodeError:
            raise InvalidJsonFormat('Invalid json format')
            