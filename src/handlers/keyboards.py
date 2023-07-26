from telegrinder import InlineKeyboard, KeyboardSetYAML


class KeyboardSet(KeyboardSetYAML):
    __config__ = "src/keyboard_set.yaml"

    KEYBOARD_MENU: InlineKeyboard


KeyboardSet.load()
