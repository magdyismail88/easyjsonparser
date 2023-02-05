import unittest
from easyjsonparser import (
    EasyJsonParser, 
    EasyJsonParserIO,
    WrongDirOrFilename,
    InvalidJsonFormat
) 


class EasyJsonParserTest(unittest.TestCase):

    def setUp(self):
        self.fixtures_path = '../fixtures'
        self.default = {
            'path': self.fixtures_path,
            'filename': 'config'
        }
        
    # Testing normal file without any errors
    def test_valid_json_file(self):
        configs = EasyJsonParser(**self.default)
        self.assertEqual(
            configs('database.mysql.host'), 'localhost'
        )
        self.assertEqual(
            configs.get('database.mysql.host'), 'localhost'
        )
        
    # Testing by multi args
    def test_access_data_by_multi_args(self):
        configs = EasyJsonParser(**self.default)
        self.assertEqual(
            configs('database', 'mysql', 'host'), 'localhost'
        )
        self.assertEqual(
            configs.get('database', 'mysql', 'host'), 'localhost'
        )
    
    # Testing with delimiter
    def test_valid_add_new_delimiter_and_use_it(self):
        configs = EasyJsonParser(**self.default)
        self.assertEqual(
            configs('database|mysql|host'), None
        )
        configs.add_delimiters('|')
        self.assertEqual(
            configs('database|mysql|host'), 'localhost'
        )
    
    # Testing with different filename
    def test_using_different_filename(self):
        another_json_file = {
            "path": self.fixtures_path,
            "filename": "another-config"
        }
        configs = EasyJsonParser(**another_json_file)
        self.assertEqual(configs('filename'), 'another-config')
        
    def test_using_different_dir(self):
        from os import sep
        another_sub_dir = {
            "path": self.fixtures_path + sep + 'sub',
            "filename": "config"
        }
        configs = EasyJsonParser(**another_sub_dir)
        self.assertEqual(configs('filename'), 'sub-config')
    
    # Testing using different file extension
    def test_not_using_file_with_different_extension(self):
        json_file_with_conf_ext = {
            "path": self.fixtures_path,
            "filename": "config-conf"
        }
        self.assertRaises(
            WrongDirOrFilename,
            EasyJsonParser,
            **json_file_with_conf_ext
        )
    
    # Testing config file without json extension
    def test_using_filename_without_extension(self):
        json_file_with_conf_ext = {
            "path": self.fixtures_path,
            "filename": "config-without-ex"
        }
        self.assertRaises(
            WrongDirOrFilename,
            EasyJsonParser,
            **json_file_with_conf_ext
        )
        
    # Testing using more one delimiter pattern
    def test_invalid_using_multi_different_delemiter(self):
        configs = EasyJsonParser(**self.default)
        self.assertNotEqual(
            configs('database.mysql-host'), 'localhost'
        )
        self.assertNotEqual(
            configs.get('database.mysql,host'), 'localhost'
        )
        
    # Testing enter wrong information
    def test_using_invalid_identifiers(self):
        configs = EasyJsonParser(**self.default)
        self.assertEqual(
            configs('this.key.invalid'), None
        )
        self.assertEqual(
            configs.get('this.key.invalid'), None
        )
    
    # Testing with invalid json file or file has errors
    def test_invalid_json_format_file(self):
        bad_json = {
            'path': '../fixtures',
            'filename': 'example-02.json'
        }
        
        self.assertRaises(
            InvalidJsonFormat,
            EasyJsonParser,
            **bad_json
        )
        
    # Testing if gives file not found
    def test_config_file_not_found(self):
        bad_json = {
            'path': '../../invalid-path',
            'filename': 'invalid.json'
        }
        self.assertRaises(
            WrongDirOrFilename,
            EasyJsonParser,
            **bad_json
        )
        
    def test_file_with_web_service(self):
        json = {
            'path': self.fixtures_path,
            'filename': 'items.json'
        }
        
        items_data = [
            {"id": 1, "name": "Item 1"},
            {"id": 2, "name": "Item 2"},
            {"id": 3, "name": "Item 3"},
            {"id": 4, "name": "Item 4"}
        ]
        
        data = EasyJsonParser(**json)
        items = data('items')
        
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 4)
        self.assertDictEqual(items_data[0], items[0])
        self.assertCountEqual(items, items_data)
        self.assertListEqual(items, items_data)


class EasyJsonParserIOTest(unittest.TestCase):
    # Testing with basic buffer
    def test_valid_json(self):
        json = '''
        {
            "key1": {
                "key11": {
                    "key111": "value111"
                }
            },
            "key2": "value2"
        }
        '''
        
        configs = EasyJsonParserIO(json)
        self.assertEqual(configs('key1.key11.key111'), 'value111')
    
    # Testing invalid json
    def test_invalid_stream(self):
        invalid_json_stream = '''
        {
            "key1": {
                "key11": {
                    "key111": "value111"
                }
            },
            "key2": "value2
        }
        '''
        
        self.assertRaises(
            InvalidJsonFormat,
            EasyJsonParserIO,
            invalid_json_stream
        )


if __name__ == '__main__':
    unittest.main()