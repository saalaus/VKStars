from enum import Enum

from . import get_members, update_widget


def minify(code):
    return "".join(i.strip() for i in code.splitlines())



class ExecuteCode(Enum):
    # EXECUTE WITH NOT COMMENTS
    get_members = minify(get_members.code)
    update_widget = minify(update_widget.code)
