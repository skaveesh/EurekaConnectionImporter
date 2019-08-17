import yaml
import uuid
import collections
import urllib.request as urllib
import xmltodict

SOURCE_FILES_PATH = '/home/vwasaka/Documents/AsbruConnections/py/'
DESTINATION_FILES_PATH = '/home/vwasaka/Documents/AsbruConnections/py/out/'

MAIN_FILE = 'main.txt'
ENV_FOLDER_FILE = 'env_folder.txt'
SERVICE_FILE = 'service.txt'
SERVICE_FOLDER_FILE = 'service_folder.txt'

OUT_FILE = 'import_connections.yml'

main_file_reader = open(SOURCE_FILES_PATH + MAIN_FILE)


def get_uuid():
    return str(uuid.uuid4())


def effify(non_f_str: str):
    return eval(f'f"""{non_f_str}"""')


def make_hash():
    return collections.defaultdict(make_hash)


#
# my_dict = yaml.load(open(SOURCE_FILES_PATH + MAIN_FILE), yaml.FullLoader)
#
# new_children = {'children': {get_uuid(): 1, get_uuid(): 1}}
#
# my_dict["__PAC__EXPORTED__"] = new_children
#
# print(yaml.dump(my_dict))


# with open(SOURCE_FILES_PATH + '/' + MAIN_FILE) as myfile:
#     data = myfile.read()
#     children = newu
#     print(effify(data))


def homepage():
    file = urllib.urlopen('http://localhost:8761/eureka/apps')
    data = file.read()
    file.close()

    # data =
    return xmltodict.parse(data, dict_constructor=dict)


for k, v in homepage()['applications'].items():
    if k == 'application':
        for a in v:
            for ins in a['instance']:
                print(ins['hostName'], 'as', ins['app'], 'in', ins['ipAddr'], 'with', ins['port']['#text'])
