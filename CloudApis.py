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

import argparse, os, logging, json
import base64
import datetime
import time
import jwt
import requests
import uuid
import random, string
import collections
from Utility import *

NUM_RETRIES = 3
BATCH_SIZE = 100

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
PATH_TO_SIMULATION_FILE = os.path.join(APP_ROOT, 'files','pubsub_messages')
PATH_TO_TABLE_SCHEMA_FILE = os.path.join(APP_ROOT, 'files','table_schema')

class CloudApis(Utility):
  def __init__(self):
    """
    Description: 
       This contructor function created a logger object
    Args: 
       None
    Returns:
       None
    """
    super(CloudApis,self).__init__()

  def create_device_registry(self, client, project_id, cloud_region, pubsub_topic_id, registry_id):
    """
    Description: 
       This function reates a registry.
    Args: 
       client: client service object
       project_id: project id
       cloud_region: google cloud region
       registry_id: registry id
    Returns:
       On success: response object
       On failure: None or an exception will be thrown.
    Raises:
       An exception error message if the registry cannot be created.
    """ 
    registry_parent = 'projects/{}/locations/{}'.format(project_id, cloud_region)
    pubsub_topic = 'projects/{}/topics/{}'.format(project_id, pubsub_topic_id)
    body = {
        'eventNotificationConfigs': [{
            'pubsubTopicName': pubsub_topic
        }],
        'id': registry_id
    }

    try:
        response = client.projects().locations().registries().create(parent=registry_parent, body=body).execute(num_retries=NUM_RETRIES)
        return response
    except Exception as e:
        print "Exception: %s, registry not created" % e
        raise

  def delete_device_registry(self, client, project_id, cloud_region, registry_id):
    """
    Description: 
       This function reates a registry.
    Args: 
       client: client service object
       project_id: project id
       cloud_region: google cloud region
       registry_id: registry id
    Returns:
       On success: response object
       On failure: None or an exception will be thrown.
    Raises:
       An exception if the registry cannot be deleted.
    """ 
    registry_name = 'projects/{}/locations/{}/registries/{}'.format(project_id, cloud_region, registry_id)

    try:
        response = client.projects().locations().registries().delete(name=registry_name).execute(num_retries=NUM_RETRIES)
        return response
    except Exception as e:
        print "Exception: %s, registry not deleted" % e
        raise

  def create_device(self,client, project_id, cloud_region, registry_id, device_id, public_key_file):
    """
    Description: 
       This function reates a registry.
    Args: 
       client: client service object
       project_id: project id
       cloud_region: google cloud region
       registry_id: registry id
       device_id: device id
       public_key_file: path to the public key file
    Returns:
       On success: response object
       On failure: None or an exception will be thrown.
    Raises:
       An exception if the registry cannot be created.
    """ 
    registry_name = 'projects/{}/locations/{}/registries/{}'.format(project_id, cloud_region, registry_id)

    with open(public_key_file) as f:
        public_key = f.read()

    # Note: You can have multiple credentials associated with a device.
    device_template = {
        'id': device_id,
        'credentials': [{
            'publicKey': {
                'format': 'RSA_X509_PEM',
                'key': public_key
            }
        }]
    }

    try:
        response = client.projects().locations().registries().devices().create(parent=registry_name, body=device_template).execute(num_retries=NUM_RETRIES)
        return response
    except Exception as e:
       print "Exception: %s, device not created" % e
       raise

  def delete_device(self,client, project_id, cloud_region, registry_id, device_id):
    """
    Description: 
       This function Delete the device.
    Args: 
       client: client service object
       project_id: project id
       cloud_region: google cloud region
       registry_id: registry id
       device_id: device id
    Returns:
       On success: response object
       On failure: None or an exception will be thrown.
    Raises:
       An exception if the device cannot be deleted.
    """ 

    registry_name = 'projects/{}/locations/{}/registries/{}'.format(project_id, cloud_region, registry_id)
    device_name = '{}/devices/{}'.format(registry_name, device_id)

    try:
        response = client.projects().locations().registries().devices().delete(name=device_name).execute(num_retries=NUM_RETRIES)
        return response
    except Exception as e:
        print "Exception: %s, device not deleted" % e
        raise

  def set_config(self,client, project_id, cloud_region, registry_id, device_id, version, config):
    print('Set device configuration')
    device_path = 'projects/{}/locations/{}/registries/{}/devices/{}'.format(
            project_id, cloud_region, registry_id, device_id)

    config_body = {
        'versionToUpdate': version,
        'binaryData': base64.urlsafe_b64encode(
                config.encode('utf-8')).decode('ascii')
    }

    return client.projects(
        ).locations().registries(
        ).devices().modifyCloudToDeviceConfig(
        name=device_path, body=config_body).execute()
   # [END iot_set_device_config]

  # [START iot_get_device_configs]
  def get_config_versions(self, client, project_id, cloud_region, registry_id,
        device_id):
    """Lists versions of a device config in descending order (newest first)."""
    registry_name = 'projects/{}/locations/{}/registries/{}'.format(
        project_id, cloud_region, registry_id)

    device_name = '{}/devices/{}'.format(registry_name, device_id)
    devices = client.projects().locations().registries().devices()
    configs = devices.configVersions().list(
        name=device_name).execute().get(
        'deviceConfigs', [])

    for config in configs:
        print('version: {}\n\tcloudUpdateTime: {}\n\t binaryData: {}'.format(
            config.get('version'),
            config.get('cloudUpdateTime'),
            config.get('binaryData')))
    return configs

  def getDeviceConfig(self,client, project_id, cloud_region, registry_id, device_id):
    """
    Description: 
       This function Delete the device.
    Args: 
       client: client service object
       project_id: project id
       cloud_region: google cloud region
       registry_id: registry id
       device_id: device id
    Returns:
       On success: response object
       On failure: None or an exception will be thrown.
    Raises:
       An exception if the device cannot be deleted.
    """ 

    registry_name = 'projects/{}/locations/{}/registries/{}'.format(project_id, cloud_region, registry_id)
    device_name = '{}/devices/{}'.format(registry_name, device_id)

    try:
        response = client.projects().locations().registries().devices().getConfig(name=device_name,localVersion=1).execute(num_retries=NUM_RETRIES)
        return response
    except Exception as e:
        print "Exception: %s, device not deleted" % e
        raise

  def get_full_subscription_name(self,project_id, subscription_id):
    """
    Description: 
       Returns a fully qualified subscription name
    Args: 
       project_id: project id
       subscription_id: subscription id
    Returns:
       suscription name
    """
    return ('projects/{}/subscriptions/{}').format(project_id, subscription_id)

  def get_full_topic_name(self,project_id, topic_id):
    """
    Description: 
       Returns a fully qualified topic name
    Args: 
       project_id: project id
       topic_id: topic id
    Returns:
       topic name
    """
    return ('projects/{}/topics/{}').format(project_id, topic_id)
 
  def get_full_table_name(self, project_id, dataset_id, table_id):
    """
    Description: 
       Returns a fully qualified table name
    Args: 
       project_id: project id
       dataset_id: dataset id
       table_id: table name
    Returns:
       table name
    """
    return ('{}:{}.{}').format(project_id, dataset_id, table_id)


  def create_topic(self, client, project_id, topic_id):
    """
    Description: 
       Create a new topic
    Args: 
       client: client service object
       project_id: project id
       topic_id: topic id
    Returns:
       On success: response object
       On failure: None or an exception will be thrown.
    Raises:
       An exception if the topic cannot be created.
    """  
    try:
        response = client.projects().topics().create(name=self.get_full_topic_name(project_id, topic_id), body={}).execute(num_retries=NUM_RETRIES)    
        print('Created topic')
        return response
    except Exception as e:
        print "Exception: %s, topic not created" % e
        raise

  def delete_topic(self, client, project_id, topic_id):
    """
    Description: 
       delete a topic
    Args: 
       client: client service object
       project_id: project id
       topic_id: topic id
    Returns:
       On success: response object
       On failure: None or an exception will be thrown.
    Raises:
       An exception if the topic cannot be deleted.
    """  
    try:
        response = client.projects().topics().delete(topic=self.get_full_topic_name(project_id, topic_id)).execute(num_retries=NUM_RETRIES)
        return response
    except Exception as e:
        print "Exception: %s, topic not deleted" % e
        raise

  def create_subscription(self, client, project_id, pubsub_topic, subscription_id):
    """
    Description: 
       create a subscription
    Args: 
       client: client service object
       project_id: project id
       pubsub_topic: topic id
       subscription_id: subscription id
    Returns:
       On success: response object
       On failure: None or an exception will be thrown.
    Raises:
       An exception if the subscription cannot be created.
    """ 
    body = {'topic': self.get_full_topic_name(project_id, pubsub_topic)}
    try:
        response = client.projects().subscriptions().create(name=self.get_full_subscription_name(project_id, subscription_id), body=body).execute(num_retries=NUM_RETRIES)
        return response
    except Exception as e:
       print "Exception: %s, subscription not created" % e
       raise

  def delete_subscription(self, client, project_id, subscription_id):
    """
    Description: 
       delete a subscription
    Args: 
       client: client service object
       project_id: project id
       pubsub_topic: topic id
       subscription_id: subscription id
    Returns:
       On success: response object
       On failure: None or an exception will be thrown.
    Raises:
       An exception if the subscription cannot be deleted.
    """ 
    try:
        response = client.projects().subscriptions().delete(subscription=self.get_full_subscription_name(project_id, subscription_id)).execute(num_retries=NUM_RETRIES)
        return response
    except Exception as e:
        print "Exception: %s, subscription not deleted" % e
        raise

  def pull_messages(self, client, project_name, sub_id, max_num_of_messages):
    """
    Description: 
       Pulls messages from a given subscription
    Args: 
       project_name: project id
       sub_id: subscription id
       max_num_of_messages: maximum number of messages will be pulled on each request
    Returns:
       On success: Pub/Sub message in JSON object
       On failure: None or an exception will be thrown.
    """
    list_of_message_objects = []
    subscription = self.get_full_subscription_name(project_name, sub_id)
    body = {
            'returnImmediately': False,
            'maxMessages': max_num_of_messages
    }
    resp = client.projects().subscriptions().pull(
                subscription=subscription, body=body).execute(
                        num_retries=NUM_RETRIES)

    try:
        receivedMessages = resp.get('receivedMessages')   
        if receivedMessages is not None:
            ack_ids = []
            for receivedMessage in receivedMessages:
                message = receivedMessage.get('message')
                if message:
                        ack_ids.append(receivedMessage.get('ackId'))     
        
            ack_body = {'ackIds': ack_ids}
            client.projects().subscriptions().acknowledge(subscription=subscription, body=ack_body).execute(num_retries=NUM_RETRIES)   
  
        return receivedMessages
    except Exception as e:
        print "Exception: %s, Cannot publish message" % e
        raise
  
  def getSubccriptionConfiguration(self, client, project_name, sub_id, max_num_of_messages):
    """
    Description: 
       Pulls messages from a given subscription
    Args: 
       project_name: project id
       sub_id: subscription id
       max_num_of_messages: maximum number of messages will be pulled on each request
    Returns:
       On success: Pub/Sub message in JSON object
       On failure: None or an exception will be thrown.
    """
    list_of_message_objects = []
    subscription = self.get_full_subscription_name(project_name, sub_id)
    resp = client.projects().subscriptions().get(
                subscription=subscription).execute(
                        num_retries=NUM_RETRIES)

    try: 
        print("device config: ",resp)  
        return resp
    except Exception as e:
        print "Exception: %s, Cannot get configuration" % e
        raise


  def create_jwt(self, project_id, private_key_file, algorithm):
    """
    Description: 
       Return a token
    Args: 
       project_id: project id
       private_key_file: path to private key file
       algorithm: algorithm used to create web token
    Returns:
       On success: web token string
       On failure: None or exception thrown.
    """ 
    token = {
            # The time the token was issued.
            'iat': datetime.datetime.utcnow(),
            # Token expiration time.
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            # The audience field should always be set to the GCP project id.
            'aud': project_id
    }

    # Read the private key file.
    with open(private_key_file, 'r') as f:
        private_key = f.read()
    
    try:
        return jwt.encode(token, private_key, algorithm=algorithm)
    except Exception as e:
        print "Exception: %s, web token string cannot be created" % e
        raise
    
  def publish_message(self, message, message_type, base_url, project_id, cloud_region, registry_id, device_id, jwt_token):
    """
    Description: 
       Publish to the events or state topic based on the flag
    Args:
       message: message to send
       project_id: project id
       private_key_file: path to private key file
       algorithm: algorithm used to create web token
    Returns:
       On success: web token string
       On failure: None or exception thrown.
    """ 
    headers = {
            'authorization': 'Bearer {}'.format(jwt_token),
            'content-type': 'application/json',
            'cache-control': 'no-cache'
    }

    # Publish to the events or state topic based on the flag.
    url_suffix = 'publishEvent' if message_type == 'event' else 'setState'

    publish_url = (
        '{}/projects/{}/locations/{}/registries/{}/devices/{}:{}').format(
            base_url, project_id, cloud_region, registry_id, device_id,
            url_suffix)

    body = None
    if message_type == 'event':
        body = {'binary_data': base64.urlsafe_b64encode(message)}
    else:
        body = {
          'state': {'binary_data': base64.urlsafe_b64encode(message)}
        }   

    try:
        resp = requests.post(publish_url, data=json.dumps(body), headers=headers)
        return resp
    except Exception as e:
        print "Exception: %s, cannot publish message" % e
        raise
  def get_config(self, version, message_type, base_url, project_id, cloud_regionn
,registry_id, device_id, private_key_file, algorithm):
    jwt_token = self.create_jwt(project_id, private_key_file, algorithm)
    headers = {
            'authorization': 'Bearer {}'.format(jwt_token),
            'content-type': 'application/json',
            'cache-control': 'no-cache'
    }

    basepath = '{}/projects/{}/locations/{}/registries/{}/devices/{}/'
    template = basepath + 'config?local_version={}'
    config_url = template.format(
        base_url, project_id, cloud_region, registry_id, device_id, version)

    resp = requests.get(config_url, headers=headers)

    if (resp.status_code != 200):
        print('Error getting config: {}, retrying'.format(resp.status_code))
        raise AssertionError('Not OK response: {}'.format(resp.status_code))

    return resp


  def get_table_schema(self):
     """
     Description: 
       return content of the table schema file
     Args:
       None
     Returns:
       On success: content of the table schema file
     """ 
     with open(PATH_TO_TABLE_SCHEMA_FILE, 'r') as f:
       content = f.read()
     
     try:
        return content
     except Exception as e:
        print "Exception: %s, cannot publish message" % e
        raise

  def publish_message_to_subpub(self, project_id, registry_id, device_id, message_type, base_url, cloud_region, algorithm, private_key_file, message_data_type, file_data):
     """
     Description: 
       return content of the file
     Args:
       project_id: project id
       registry_id: registry id
       device_id: device id 
       message_type: message type event or setState
       base_url: url to the google cloud iot to make a rest call 
       cloud_region: google cloud region
       algorithm: algorithm used to create web token
       private_key_file: path to private key file 
       message_data_type: Three options "data_file", "data_string" or read message a from file limit to 1 message per line. The options string indicating image path, image string 
                          containing image data or reading from the simulation file stored in blobal variable PATH_TO_SIMULATION_FILE.
       file_data: String containing the data or path to the file.
     Returns:
       On success: content of the file
     """
     try:
       if(message_data_type == "data_file"):
         file_path = file_data
         with open(file_path, 'r') as fhdl:
            file_data = fhdl.read()
         if(file_data):
            jwt_token = self.create_jwt(project_id, private_key_file, algorithm)            
            payload = '{}'.format(file_data)
            resp = self.publish_message(payload, message_type, base_url, project_id, cloud_region, registry_id, device_id, jwt_token)        
            if resp != None:
               print('HTTP response: ', resp)
               self.logData("HTTP response: {}".format(resp))
       elif(message_data_type == "data_string"):
         if(file_data):
            jwt_token = self.create_jwt(project_id, private_key_file, algorithm)
            payload = '{}'.format(file_data)
            print("parameters: ", type(file_data), type(payload), message_type, base_url, project_id, cloud_region, registry_id, device_id, jwt_token)
            
            try:
              resp = self.publish_message(payload, message_type, base_url, project_id, cloud_region, registry_id, device_id, jwt_token)        
              if resp != None:
                 print('HTTP response: ', resp)
                 self.logData("HTTP response: {}".format(resp))
            except Exception, e:
              print("send to pubsub error: ", e)

       else:
         with open(PATH_TO_SIMULATION_FILE, 'r') as f:
           for message_line in f:      
             jwt_token = self.create_jwt(project_id, private_key_file, algorithm)            
             payload = '{}/{}-{}'.format(registry_id, device_id, message_line)
             resp = self.publish_message(payload, message_type, base_url, project_id, cloud_region, registry_id, device_id, jwt_token)        
             if resp != None:
                print('HTTP response: ', resp)
                self.logData("HTTP response: {}".format(resp))
             time.sleep(1 if message_type == 'event' else 5)
     except Exception as e:
       print "Exception: %s, cannot publish message to pub/sub" % e
       raise
  def create_dataset(self, bigquery, dataset_id, project=None):
    """
    Description: 
       Create a dataset in a given project
    Args:
       bigquery: bigquery api object
       project: project id
       dataset_id: dataset id
    Returns:
       On success: dataset deleted from bigquery
    """
    try:
        bigquery_client = bigquery.Client(project=project)
        dataset_ref = bigquery_client.dataset(dataset_id)
        response = bigquery_client.create_dataset(bigquery.Dataset(dataset_ref))
        return response
    except Exception as e:
       print "Exception: %s, cannot publish message to pub/sub" % e
       raise

  def delete_dataset(self, bigquery, dataset_id, project=None):
    """
    Description: 
       Delete a dataset in a given project
    Args:
       bigquery: bigquery api object
       project: project id
       dataset_id: dataset id
    Returns:
       On success: dataset deleted from bigquery
       On failure: None or exception thrown
    """ 
    try: 
       bigquery_client = bigquery.Client(project=project)
       dataset_ref = bigquery_client.dataset(dataset_id)
       dataset_ref.delete()
    except Exception as e:
       print "Exception: %s, cannot delete dataset" % e
       raise

  def create_table(self, bigquery, dataset_id, table_id, project=None):
    """
    Description: 
       Creates a simple table in the given dataset.
    Args:
       bigquery: bigquery api object
       project: project id
       dataset_id: dataset id
       table_id: table id
    Returns:
       On success: a successful JSON object
       On failure: None or exception thrown
    """
    try: 
       bigquery_client = bigquery.Client(project=project)
       dataset_ref = bigquery_client.dataset(dataset_id)

       table_ref = dataset_ref.table(table_id)
       table = bigquery.Table(table_ref)

       tbl_schema = self.get_table_schema()
       table.schema = (eval(tbl_schema))
       response = bigquery_client.create_table(table)
       return response
    except Exception as e:
       print "Exception: %s, cannot create table" % e
       raise

  def delete_table(self, bigquery, dataset_id, table_id, project=None):
    """
    Description: 
       Delete a table from bigquery
    Args:
       bigquery: bigquery api object
       project: project id
       dataset_id: dataset id
       table_id: table id
    Returns:
       On success: a successful JSON object
       On failure: None or exception thrown
    """
    try: 
       bigquery_client = bigquery.Client(project=project)
       dataset_ref = bigquery_client.dataset(dataset_id)
       table_ref = dataset_ref.table(table_id)
       response = bigquery_client.delete_table(table_ref)
       return response
    except Exception as e:
       print "Exception: %s, cannot delete table" % e
       raise
  
  def Insert_to_bq(self, bigquery, project_id, dataset, table, messages_json):
    """
    Description: 
       Insert message into bigquery table
    Args:
       bigquery: bigquery api object
       project: project id
       dataset: dataset id
       table: table id
    Returns:
       On success: a successful JSON object
       On failure: None or exception thrown
    """ 
    try:
        rowlist = []
        for item in messages_json:
            item_row = {"json": item}
            rowlist.append(item_row)
        body = {"rows": rowlist}
        
        response = bigquery.tabledata().insertAll(
                projectId=project_id, datasetId=dataset,
                tableId=table, body=body).execute(num_retries=NUM_RETRIES)  
      
        return response
    except Exception as e1:
        print "Exception: %s" % e1
        raise
  
  def write_to_bq(self, pubsub, project_id, sub_name, bigquery, messages_json, dataset, table):
    """
    Description: 
       check to see if json object pass is empty or not. If not call function Insert_to_bq to insert the message into bigquery table
    Args:
       pubsub: pubsub service object
       project: project id
       sub_name: subscription id
       bigquery: bigquery api object
       messages_json: message in json object pull from pubsub
       dataset: dataset id
       table: table id
    Returns:
       On success: a successful JSON object
       On failure: None or exception thrown
    """ 
    if messages_json:
        try:
           response = self.Insert_to_bq(bigquery, project_id, dataset, table, messages_json)
        except Exception as e:
           print "Exception: %s" % e1
           raise
    else:
        return None
