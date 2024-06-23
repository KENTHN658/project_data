import configparser
import os
parser = configparser.ConfigParser()
parser.read(os.path.join(os.path.dirname(__file__), '../config/config.conf'))
API_KEY = parser.get('api_keys', 'apikey')

INPUT_PATH = parser.get('file_paths', 'input_path')
OUTPUT_PATH = parser.get('file_paths', 'output_path')

