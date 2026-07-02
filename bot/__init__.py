import importlib


def load_handlers():
    """
    Load the main handlers module.
    """

    importlib.import_module("bot.handlers")
