# Copyright 2017, Google LLC All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import random, string, os, re

import logging
from logging.handlers import RotatingFileHandler

APP_ROOT = os.path.dirname(os.path.abspath(__file__)) 

class Utility(object):
  def __init__(self):
    pass
     
  def logData(self, data):   
    """
      Description: 
       This function log information to the logfile within the log folder.
      Args: 
       data: data write to logfile
      Returns:
       None
    """
    log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')
    logFile = os.path.join(APP_ROOT, "log", "logfile")
    fileHandler = RotatingFileHandler(logFile, mode='a', maxBytes=5*1024*1024, 
                                 backupCount=2, encoding=None, delay=0)
    fileHandler.setFormatter(log_formatter)
    fileHandler.setLevel(logging.INFO)

    app_log = logging.getLogger('applogger')
    app_log.setLevel(logging.INFO)

    app_log.addHandler(fileHandler)
    app_log.info(data)  
