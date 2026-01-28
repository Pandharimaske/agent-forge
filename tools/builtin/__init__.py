from tools.base import Tool
from tools.builtin.read_file import ReadFileTool
from tools.builtin.write_file import WriteFileTool
from tools.builtin.edit_file import EditTool


__all__ = [
    'ReadFileTool' , 
    'WriteFileTool' , 
    'EditTool' ,
]

def get_all_builtin_tools() -> list[Tool]:
    return [
        ReadFileTool,
        WriteFileTool,
        EditTool,
    ]