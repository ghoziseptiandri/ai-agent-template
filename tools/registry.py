from tools.calculator import calculate
from tools.time_tool import get_current_time
from long_term_memory import save_memory, update_memory, delete_memory

TOOL_FUNCTIONS = {
    "calculate": calculate,
    "get_current_time": get_current_time,
    "save_memory": save_memory,
    "update_memory": update_memory,
    "delete_memory": delete_memory,
}