from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction

from src.functions import strip_list
from src.translate_shell import TranslateShell
from src.items import no_input_item, missing_dep_item, show_used_args, generate_trans_items, no_translation_available

class TranslateExtension(Extension):
    def __init__(self):
        super(TranslateExtension, self).__init__()

        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        query = event.get_argument() or str()

        params = strip_list(query.split(' '))

        parser = TranslateShell(extension.preferences, params)

        if parser.is_dep_missing():
            return RenderResultListAction(missing_dep_item())

        if len(query.strip()) == 0:
            return RenderResultListAction(no_input_item())

        if not parser.has_query():
            return RenderResultListAction(show_used_args(parser))

        translations = parser.execute()

        if not translations:
            return RenderResultListAction(no_translation_available())

        return RenderResultListAction(generate_trans_items(translations))


if __name__ == '__main__':
    TranslateExtension().run()
