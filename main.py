from constants import *
import ruamel.yaml
import hashdict
import eurekaxmlparse
import collections


main_dictionary = hashdict.make_hash()

IS_PRD = bool(int(input(QUESTION_PROD_OR_NOT)))

ENV_NAME = PROD if IS_PRD else str(input(QUESTION_ENV_NAME))

main_dictionary.update({PAC_EXPORTED: {CHILDREN: {}}})
main_dictionary[PAC_EXPORTED][CHILDREN] = {ENV_GUID: 1}

main_dictionary.update({ENV_GUID: {NAME: ENV_NAME, IS_GROUP: 1, CHILDREN: {}}})

for key, value in eurekaxmlparse.get_xml_from_eureka()[APPLICATIONS].items():
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
                                                     PRD_PEM_FILE_LOCATION if IS_PRD else NON_PRD_PEM_FILE_LOCATION,
                                                     STARTING_PORT, instance[PORT][TEXT], instance[IP_ADDRESS])}
                STARTING_PORT += PORT_GAP
                main_dictionary[service_folder_uuid][CHILDREN][service_uuid] = 1

file_with_path = DESTINATION_FILES_PATH + str.lower(ENV_NAME) + OUT_FILE
yaml = ruamel.yaml.round_trip_dump(dict(main_dictionary), stream=open(file_with_path, WRITE),
                                   width=800)
print(MESSAGE_SUCCESSFUL + file_with_path)
