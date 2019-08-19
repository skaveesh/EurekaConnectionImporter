from constants import *
import ruamel.yaml
import hashdict
import eurekaxmlparse
import collections

environment_dict = {0: DEV, 1: DEV1, 2: DEV2, 3: DEV3, 4: QA, 5: STG, 6: PROD}
eureka_dict = {0: EUREKA_DEV, 1: EUREKA_DEV1, 2: EUREKA_DEV2, 3: EUREKA_DEV3, 4: EUREKA_QA, 5: EUREKA_STG,
               6: EUREKA_PROD}

main_dictionary = hashdict.make_hash()

environment_user_input = int(input(QUESTION_ENV_NUMBER))

try:
    environment_name = environment_dict[environment_user_input]
    eureka_endpoint = eureka_dict[environment_user_input]
except KeyError:
    print(MESSAGE_INPUT_ERROR)
    environment_name = None
    eureka_endpoint = None
    exit(1)

IS_PROD = environment_name == PROD

main_dictionary.update({PAC_EXPORTED: {CHILDREN: {}}})
main_dictionary[PAC_EXPORTED][CHILDREN] = {ENV_GUID: 1}

main_dictionary.update({ENV_GUID: {NAME: environment_name, IS_GROUP: 1, CHILDREN: {}}})

for key, value in eurekaxmlparse.get_xml_from_eureka(eureka_endpoint)[APPLICATIONS].items():
    if key == APPLICATION:
        for application in value:
            service_folder_uuid = uuidgen.get_uuid()
            main_dictionary[ENV_GUID][CHILDREN][service_folder_uuid] = 1
            main_dictionary.update(
                {service_folder_uuid: {NAME: application[NAME], IS_GROUP: 1, CHILDREN: {}}})

            if isinstance(application[INSTANCE], collections.Mapping):
                application[INSTANCE] = [application[INSTANCE]]

            for instance in application[INSTANCE]:
                service_uuid = uuidgen.get_uuid()
                main_dictionary[service_uuid] = {NAME: instance[HOST_NAME], IS_GROUP: 0,
                                                 METHOD: GENERIC_CMD,
                                                 IP: SSH_CMD.format(
                                                     PRD_PEM_FILE_LOCATION if IS_PROD else NON_PRD_PEM_FILE_LOCATION,
                                                     STARTING_PORT, instance[PORT][TEXT], instance[IP_ADDRESS])}
                STARTING_PORT += PORT_GAP
                main_dictionary[service_folder_uuid][CHILDREN][service_uuid] = 1

file_with_path = DESTINATION_FILES_PATH + str.lower(environment_name) + OUT_FILE
yaml = ruamel.yaml.round_trip_dump(dict(main_dictionary), stream=open(file_with_path, WRITE),
                                   width=800)
print(MESSAGE_SUCCESSFUL + file_with_path)
