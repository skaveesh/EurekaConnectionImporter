import urllib.request as urllib
import xmltodict


def get_xml_from_eureka(endpoint: str):
    file = urllib.urlopen(endpoint)
    data = file.read()
    file.close()
    return xmltodict.parse(data, dict_constructor=dict)
