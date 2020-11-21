from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction

from src.functions import strip_list
from src.translate_shell import TranslateShell
from src.items import no_input_item, missing_dep_item, show_used_args

class TranslateExtension(Extension):
    def __init__(self):
        super(TranslateExtension, self).__init__()

        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        query = event.get_argument() or str()

        if len(query.strip()) == 0:
            return RenderResultListAction(no_input_item())

        params = strip_list(query.split(' '))

        try:
            parser = TranslateShell(params)

            if not parser.has_request():
                return RenderResultListAction(show_used_args(parser))
        except OSError:
            return RenderResultListAction(missing_dep_item())

        return RenderResultListAction(parser.execute())


if __name__ == '__main__':
    TranslateExtension().run()
