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

import argparse, os, logging, json, glob, base64, datetime, time, sys, subprocess, mraa, requests, urllib, uuid, random, string, dateutil.parser, httplib2
from CloudApis import *
from ServiceApi import *
from Utility import *
from upm import pyupm_th02 as th02
reload(sys)
sys.setdefaultencoding('utf8')

serviceApiObj = ServiceApi() 
args = serviceApiObj.parse_command_line_args()
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=args.credential  
 
utilityObj = Utility()   
cloudApisObj = CloudApis()

    
def publish_message():
   '''
    Description: 
       This function publish tempurature and humidity data taken from sensors to the google cloud Pub/Sub.
    Args: 
       None
    Returns:
       None
    Raise:
       Throw an exception on failure
   '''   
   try:
       thsensor = th02.TH02()
       while True:
          temp = thsensor.getTemperature()
          humidity = thsensor.getHumidity()
          args.message = "Temperature(C),Humidity: (%d,%d)" % (temp, humidity)
          cloudApisObj.publish_message_to_subpub(args.project_id, args.registry_id, args.device_id, args.message_type, args.base_url, args.cloud_region, args.algorithm, args.private_key_file, args.message_data_type, args.message)
          time.sleep(2)    
   except Exception, e:
       print e
   else:
       print("Temperature and humidity data published")
       utilityObj.logData("Temperature and humidity data published")

publish_message()
