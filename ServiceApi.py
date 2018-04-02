from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
import argparse, httplib2, logging


SCOPES = ['https://www.googleapis.com/auth/cloud-platform','https://www.googleapis.com/auth/devstorage.full_control','https://www.googleapis.com/auth/datastore', 'https://www.googleapis.com/auth/compute.readonly', 'https://www.googleapis.com/auth/compute', 'https://www.googleapis.com/auth/userinfo.email']
_BASE_CLOUD_IOT_URL = 'https://cloudiot-device.googleapis.com/v1beta1'

class ServiceApi(object):
  def __init__(self):
    pass
  def parse_command_line_args(self):
    """Parse command line arguments."""
    """
    Description: 
       Parse command line arguments
    Args: 
       None
    Returns:
       parse_args object
    """
    parser = argparse.ArgumentParser(description=('Example of Google Cloud IoT Core HTTP device connection.'))
    parser.add_argument('--base_url',default=_BASE_CLOUD_IOT_URL, help=('Base URL for the Cloud IoT Core Device Service API'))
    parser.add_argument('--project_id', required=True, help='GCP cloud project id')
    parser.add_argument('--cloud_region', required=True, help=('Cloud Region'))
    parser.add_argument('--registry_id', required=True, help='Cloud IoT Core registry id')
    parser.add_argument('--device_id', required=True, help='Cloud IoT Core device id')
    parser.add_argument('--private_key_file', required=True, help='Path to private key file.')
    parser.add_argument('--public_key_file', required=True, help='Path to public key file.')
    parser.add_argument('--algorithm', choices=('RS256','ES256','RS256-X509'),required=True, help='The encryption algorithm to use to generate the JWT.')
    parser.add_argument('--num_messages',type=int, default=5, help='Maximum number of messages to publish.')
    parser.add_argument('--message_type',choices=('event', 'state'),default='event', required=False, help=('Indicates whether the message to be published is a telemetry event or a device state message.'))
    parser.add_argument('--credential', required=True, help=('Path to Service Account json file'))
    parser.add_argument('--message_data_type', required=False, help=('Message data type')) 
    parser.add_argument('--message', default='Please use the --message argument to publish the message', required=False, help=('The message to publish')) 
    return parser.parse_args()


  def get_credentials(self):
    """
    Description: 
       Get the Google credentials needed to access our services.
    Args: 
       None
    Returns:
       credentials object
    """
    
    credentials = GoogleCredentials.get_application_default()
    if credentials.create_scoped_required():
            credentials = credentials.create_scoped(SCOPES)
    return credentials


  def create_bigquery_client(self,credentials):
    """
    Description: 
       Build the bigquery service object needed to access our services.
    Args: 
       credentials: credentials object
    Returns:
       service object
    """
    http = httplib2.Http()
    credentials.authorize(http)
    return discovery.build('bigquery', 'v2', http=http)


  def create_pubsub_client(self,credentials):
    """
    Description: 
       Build the pubsub service object needed to access our services.
    Args: 
       credentials: credentials object
    Returns:
       service object for Pub/Sub
    """
    http = httplib2.Http()
    credentials.authorize(http)
    return discovery.build('pubsub', 'v1beta2', http=http)

  def create_cloudiot_client(self,credentials):
    """Build the cloudiot client."""
    """
    Description: 
       Build the cloudiot service object needed to access our services.
    Args: 
       credentials: credentials
    Returns:
       service object cloud iot
    """
    http = httplib2.Http()
    credentials.authorize(http)
    return discovery.build('cloudiot', 'v1', http=http)

  def create_visionapi_client(self,credentials):
    """
    Description: 
       Build the vision service object needed to access our services.
    Args: 
       credentials: credentials object
    Returns:
       service object for vision
    """
    http = httplib2.Http()
    credentials.authorize(http)
    return discovery.build('vision', 'v1', http=http)

  def create_dataflowapi_client(self,credentials):
    """
    Description: 
       Build the dataflow service object needed to access our services.
    Args: 
       credentials: credentials
    Returns:
       service object for dataflow
    """
    http = httplib2.Http()
    credentials.authorize(http)
    return discovery.build('dataflow', 'v1b3', http=http)

  def create_storageapi_client(self,credentials):
    """
    Description: 
       Build the storage service object needed to access our services.
    Args: 
       credentials: credentials
    Returns:
       service object for storage
    """
    http = httplib2.Http()
    credentials.authorize(http)
    return discovery.build('storage', 'v1', http=http)

