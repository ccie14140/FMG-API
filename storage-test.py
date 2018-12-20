#/usr/bin/python3

import requests
import json
import pprint
from random import *
import sys
import logging
import logging.handlers
from azure.storage.file import FileService
#
#Azure storage file
file_service = FileService(account_name='fmgapistorage', account_key='9sl5bbrePkuIgc2MCCKOdeilTiaSrMwC+yLTvNxqe1k0NHwIvS9q2wCpnlsLZNtgOJ8WlYqtzFxydIL7KEwtvA==')
file_service.create_share('myshare2')