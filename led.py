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


import argparse, os, logging, json, glob, base64, datetime, time, sys, subprocess, mraa, requests, urllib, uuid, random, string, dateutil.parser, httplib2, collections
from CloudApis import *
from ServiceApi import *
from Utility import *
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
       This function take an image and publish to the google cloud Pub/Sub.
    Args: 
       None
    Returns:
       None
    Raise:
       Throw an exception on failure
   '''   
   try:
     mraa.addSubplatform(mraa.GROVEPI,"0")

     gpio_1 = mraa.Gpio(515)
     gpio_1.dir(mraa.DIR_OUT)
     gpio_1.write(0)

     while True:
       gpio_1.write(1)
       args.message = "led: on"
       cloudApisObj.publish_message_to_subpub(args.project_id, args.registry_id, args.device_id, args.message_type, args.base_url, args.cloud_region, args.algorithm, args.private_key_file, args.message_data_type, args.message)
       time.sleep(2)
       gpio_1.write(0)
       args.message = "led: off"
       cloudApisObj.publish_message_to_subpub(args.project_id, args.registry_id, args.device_id, args.message_type, args.base_url, args.cloud_region, args.algorithm, args.private_key_file, args.message_data_type, args.message)
       time.sleep(2)

   except Exception, e:
       print e

   else:
       utilityObj.logData("Data published")

publish_message()
