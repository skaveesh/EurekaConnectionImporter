import urllib.request as urllib
import xmltodict
from constants import *


def get_xml_from_eureka():
    file = urllib.urlopen(EUREKA_ENDPOINT)
    data = file.read()
    file.close()
    return xmltodict.parse(data, dict_constructor=dict)
