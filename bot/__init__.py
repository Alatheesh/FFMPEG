import importlib
import pkgutil

from bot import handlers


def load_handlers():
    """
    Automatically import every module inside bot/handlers/
    """

    for _, module_name, _ in pkgutil.iter_modules(handlers.__path__):
        importlib.import_module(f"bot.handlers.{module_name}")
