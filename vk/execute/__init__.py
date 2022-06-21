from enum import Enum
from . import get_members
from . import update_widget


def minify(code):
    return "".join(i.strip() for i in code.splitlines())


class ExecuteCode(Enum):
    get_members = minify(get_members.code)
    update_widget = update_widget.code
