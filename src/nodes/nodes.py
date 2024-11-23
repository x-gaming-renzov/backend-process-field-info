import os, pathlib, json, dotenv
from termcolor import colored
from typing import Literal

from langchain_openai import ChatOpenAI
from langchain_core.messages import ToolMessage
from langchain.tools.retriever import create_retriever_tool

from ..states.states import ProcessFieldNamesState, PotentialSameFieldInfo, PotentialSameFieldInfoList

dotenv.load_dotenv()

model = ChatOpenAI(model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"), streaming=True)
print(colored("ChatOpenAI model initialized", "green"))
"""
def preprocess_for_potential_same_field_info_list(ProcessFieldNamesState: ProcessFieldNamesState) -> ProcessFieldNamesState:
    temp_dir_path = pathlib.Path(os.getcwd()) / f"temp/{ProcessFieldNamesState.user_id}/{ProcessFieldNamesState.user_session_id}"

    with open(temp_dir_path / ProcessFieldNamesState.data_info_file_name, "r") as f:
        data_info = json.load(f)
        ProcessFieldNamesState.data_info = data_info

    field_info_list = data_info["field_info_list"]

    #dict of fields with same new_filed_name
    fields_with_same_new_field_name = {}

    for field_info in field_info_list:
        if field_info["field_new_name"] not in fields_with_same_new_field_name:
            data_type = field_info["field_type"]
            fields_with_same_new_field_name[field_info["field_new_name"]] = {
                data_type: [
                    PotentialSameFieldInfo(field_orignal_name=field_info["field_name"], 
                                        field_description=field_info["field_description"], 
                                        field_data_type=field_info["field_type"]
                                        )
                ]
            }

        else : 
            data_type = field_info["field_type"]
            if data_type not in fields_with_same_new_field_name[field_info["field_new_name"]]:
                fields_with_same_new_field_name[field_info["field_new_name"]][data_type] = [
                    PotentialSameFieldInfo(field_orignal_name=field_info["field_name"], 
                                        field_description=field_info["field_description"], 
                                        field_data_type=field_info["field_type"]
                                        )
                ]
            else:
                fields_with_same_new_field_name[field_info["field_new_name"]][data_type].append(
                    PotentialSameFieldInfo(field_orignal_name=field_info["field_name"], 
                                        field_description=field_info["field_description"], 
                                        field_data_type=field_info["field_type"]
                                        )
                )
    
    for field_name in fields_with_same_new_field_name:
        for data_type in fields_with_same_new_field_name[field_name]:
            if len(fields_with_same_new_field_name[field_name][data_type]) == 1 or len(fields_with_same_new_field_name[field_name][data_type]) == 0:
                del fields_with_same_new_field_name[field_name][data_type]
    
    new_field_names_with_potential_same_field_info_list = []

    for field_name in fields_with_same_new_field_name:
        temp_list = []
        for data_type in fields_with_same_new_field_name[field_name]:
            temp_list.append(fields_with_same_new_field_name[field_name][data_type])
        new_field_names_with_potential_same_field_info_list.append(
            PotentialSameFieldInfoList(field_new_name=field_name, potential_same_field_info_list=temp_list)
        )
    
    ProcessFieldNamesState.new_field_names_with_potential_same_field_info_list = new_field_names_with_potential_same_field_info_list

    return ProcessFieldNamesState

"""
def preprocess_for_potential_same_field_info_list(ProcessFieldNamesState: ProcessFieldNamesState) -> ProcessFieldNamesState:
    temp_dir_path = pathlib.Path(os.getcwd()) / f"temp/{ProcessFieldNamesState.user_id}/{ProcessFieldNamesState.user_session_id}"

    with open(temp_dir_path / ProcessFieldNamesState.data_info_file_name, "r") as f:
        data_info = json.load(f)
        ProcessFieldNamesState.data_info = data_info

    field_info_list = data_info["field_info_list"]

    # dict of fields with same new_field_name
    fields_with_same_new_field_name = {}

    for field_info in field_info_list:
        if field_info["field_new_name"] not in fields_with_same_new_field_name:
            data_type = field_info["field_type"]
            fields_with_same_new_field_name[field_info["field_new_name"]] = {
                data_type: [
                    PotentialSameFieldInfo(field_orignal_name=field_info["field_name"], 
                                           field_description=field_info["field_description"], 
                                           field_data_type=field_info["field_type"])
                ]
            }

        else:
            data_type = field_info["field_type"]
            if data_type not in fields_with_same_new_field_name[field_info["field_new_name"]]:
                fields_with_same_new_field_name[field_info["field_new_name"]][data_type] = [
                    PotentialSameFieldInfo(field_orignal_name=field_info["field_name"], 
                                           field_description=field_info["field_description"], 
                                           field_data_type=field_info["field_type"])
                ]
            else:
                fields_with_same_new_field_name[field_info["field_new_name"]][data_type].append(
                    PotentialSameFieldInfo(field_orignal_name=field_info["field_name"], 
                                           field_description=field_info["field_description"], 
                                           field_data_type=field_info["field_type"])
                )
    
    print(colored("fields_with_same_new_field_name", "green"), fields_with_same_new_field_name)
    # Remove data types with only one or zero entries
    keys_to_delete = []

    for field_name in fields_with_same_new_field_name:
        print(colored("field_name", "green"), field_name)

        data_types_to_remove = []
        for data_type in fields_with_same_new_field_name[field_name]:
            print(colored("data_type", "blue"), data_type)
            print(colored(f"len(fields_with_same_new_field_name[field_name][data_type])", "blue"), len(fields_with_same_new_field_name[field_name][data_type]))

            if len(fields_with_same_new_field_name[field_name][data_type]) <= 1:
                data_types_to_remove.append(data_type)

        print(colored("data_types_to_remove", "red"), data_types_to_remove)
        # Remove data types after iteration
        for data_type in data_types_to_remove:
            del fields_with_same_new_field_name[field_name][data_type]


        # If all data types are removed, mark field_name for deletion
        if not fields_with_same_new_field_name[field_name]:
            print(colored("field_name marked for deletion", "red"), field_name)
            keys_to_delete.append(field_name)

    # Remove field names with no data types
    for field_name in keys_to_delete:
        del fields_with_same_new_field_name[field_name]
    
    # Create PotentialSameFieldInfoList
    new_field_names_with_potential_same_field_info_list = []

    for field_name in fields_with_same_new_field_name:
        temp_list = []
        for data_type in fields_with_same_new_field_name[field_name]:
            temp_list.append(fields_with_same_new_field_name[field_name][data_type])
        new_field_names_with_potential_same_field_info_list.append(
            PotentialSameFieldInfoList(field_new_name=field_name, potential_same_field_info_list=temp_list)
        )
    
    ProcessFieldNamesState.new_field_names_with_potential_same_field_info_list = new_field_names_with_potential_same_field_info_list

    return ProcessFieldNamesState




        