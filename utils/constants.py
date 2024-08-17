import configparser
import os
parser = configparser.ConfigParser()
parser.read(os.path.join(os.path.dirname(__file__), '../config/config.conf'))

OUTPUT_PATH = parser.get('file_paths', 'output_path')


