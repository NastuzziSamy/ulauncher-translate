from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction

ICON_FILE = 'images/icon.png'

def no_input_item():
    return [
        ExtensionResultItem(
            icon=ICON_FILE,
            name='No input',
            on_enter=HideWindowAction()
        )
    ]


def missing_dep_item():
    return [
        ExtensionResultItem(
            icon=ICON_FILE,
            name='Translate-shell is required for this extension to work',
            description="Select to follow install instructions",
            on_enter=OpenUrlAction('https://github.com/soimort/translate-shell#installation')
        )
    ]


def generate_trans_item(translation, lang):
    return ExtensionResultItem(
        icon=ICON_FILE,
        name=translation,
        description=lang + ': ' + translation,
        on_enter=CopyToClipboardAction(translation)
    )