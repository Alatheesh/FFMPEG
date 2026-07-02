import importlib
import pkgutil

from bot import handlers


def load_handlers():
    """
    Automatically import every module inside bot.handlers
    including all subpackages.
    """

    for _, module_name, is_package in pkgutil.walk_packages(
        handlers.__path__,
        handlers.__name__ + "."
    ):

        importlib.import_module(module_name)
