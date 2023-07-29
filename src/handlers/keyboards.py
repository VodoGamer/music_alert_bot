from telegrinder import InlineButton, InlineKeyboard, KeyboardSetYAML
from telegrinder.types import InlineKeyboardMarkup


class KeyboardSet(KeyboardSetYAML):
    __config__ = "src/keyboard_set.yaml"

    KEYBOARD_MENU: InlineKeyboard


def get_correct_or_no_kb(artist_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboard()
    keyboard.add(InlineButton("✅ Правильно", callback_data=f"correct/yes/{artist_id}"))
    keyboard.add(InlineButton("⛔ Неправильно", callback_data=f"correct/no/{artist_id}"))
    return keyboard.get_markup()


KeyboardSet.load()
