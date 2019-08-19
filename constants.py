import datetime
import uuidgen
import ruamel.yaml

config_dict = {}
CONFIG_FILE_NAME = 'config.yml'

with open(CONFIG_FILE_NAME) as stream:
    try:
        config_dict = ruamel.yaml.safe_load(stream)
    except ruamel.yaml.YAMLError as exc:
        print(exc)

EUREKA_ENDPOINT = config_dict['eureka-endpoint']
PRD_PEM_FILE_LOCATION = config_dict['prod-pem-file-location']
NON_PRD_PEM_FILE_LOCATION = config_dict['non-prod-pem-file-location']
DESTINATION_FILES_PATH = config_dict['output-directory']
STARTING_PORT = int(config_dict['starting-port'])
PORT_GAP = int(config_dict['port-gap'])

ENV_GUID = uuidgen.get_uuid()
PROD = 'PROD'
USER = 'pcs_user'
SSH_CMD = 'ssh -i {} -L {}:localhost:{} ' + USER + '@{}'
OUT_FILE = '_connections_' + datetime.datetime.now().isoformat() + '.yml'
PAC_EXPORTED = '__PAC__EXPORTED__'
INSTANCE = 'instance'
APPLICATION = 'application'
APPLICATIONS = 'applications'
CHILDREN = 'children'
HOST_NAME = 'hostName'
NAME = 'name'
IS_GROUP = '_is_group'
GENERIC_CMD = 'Generic Command'
IP = 'ip'
IP_ADDRESS = 'ipAddr'
METHOD = 'method'
PORT = 'port'
TEXT = '#text'
WRITE = 'w'
QUESTION_PROD_OR_NOT = 'Is this for Production Environment (Press 1 for yes, 0 for no) : '
QUESTION_ENV_NAME = 'Enter Environment Name : '
MESSAGE_SUCCESSFUL = 'Successfully exported to '
