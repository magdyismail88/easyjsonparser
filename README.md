### Easy Json Parser

Easy JSON Parser easy way to access or parsing JSON content, using JSON file as a config file, using with web services, APIS

<br>

> ##### **Example 1**

```
configs = EasyJsonParser()
# by default reading from config.json
db_hostname = config('database.mysql.host')
# or
db_hostname = config.get('database.mysql.host')
# or 
db_hostname = config.get('database', 'mysql', 'host')
```
<br>

> ##### **Example 2**

```
options = {
  'path': 'configs-path-or-another-path',
  'filename': 'config-file-name'
}

config = EasyJsonParser(**options)
or
config = EasyJsonParser(path='path-here', filename='config-filename-here')
db_hostname = config('database.mysql.host')
```
<br>

> ##### Example 3

```
buf = '''{
    "data": {
        "items": [
            {"id": 1, "name": "Item 1"}
        ]
    }
}'''

jparser = EasyJsonParserIO(buf)
items = parser('data.items')
```
<br>

> ##### Example 4

```
import requests

res = requests.get('http://example.com/api/v1/items')
jparser = EasyJsonParserIO(res.text)
items = jparser('data.items')
```