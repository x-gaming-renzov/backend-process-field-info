from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Annotated, Sequence
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class PotentialSameFieldInfo(BaseModel):
    field_orignal_name : str
    field_description : str
    field_data_type : str

class PotentialSameFieldInfoList(BaseModel):
    field_new_name : List[List[PotentialSameFieldInfo]]

class ProcessFieldNamesState(BaseModel):
    user_id : str
    user_session_id : str
    data_file_name : str
    out_data_file_name : str
    data_info_file_name : str
    data_info : Dict[str, Any] = None
    new_field_names_with_potential_same_field_info_list : List[PotentialSameFieldInfoList] = None