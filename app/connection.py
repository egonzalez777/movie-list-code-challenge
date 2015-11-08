# -*- coding: utf-8 -*-
import os

from ConfigParser import RawConfigParser
from pymongo import MongoClient

BASE_DIR = os.path.dirname(__file__)
CONFIG_PATH = os.path.join(BASE_DIR, 'local.cfg')

# Setup config parser
config = RawConfigParser()
config.read(CONFIG_PATH)

# Create a Pymongo client instance
host = config.get('mongo', 'host')
port = config.get('mongo', 'port')
client = MongoClient(host, int(port))

# Pymongo DB connection
db = client.rackspace
