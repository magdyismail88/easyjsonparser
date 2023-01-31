### Easy Json Parser

Easy Json Parser easy way to access or parsing json content using json file as a config file using with web services or apis

> ##### **Example 1**

```
configs = EasyJsonParser()
# by default reading from config.json
db_hostname = configs('database.mysql.host')
# or
db_hostname = configs.get('database.mysql.host')
```

> ##### **Example 2**

```
options = {
  'path': 'configs-path-or-another-path',
  'filename': 'config-file-name'
}

configs = EasyJsonParser(**options)
or
configs = EasyJsonParser(path='path-here')
db_hostname = configs('database.mysql.host')
```

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

> ##### Example 4

```
import requests

res = requests.get('http://example.com/api/v1/items')
jparser = EasyJsonParserIO(res.text)
items = jparser('data.items')
```