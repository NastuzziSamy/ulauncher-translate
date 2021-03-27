import subprocess
import json

from src.functions import strip_list
from src.items import generate_trans_item


ALLOWED_PARAMS = [
    '-p', '-sp'
]

FORCED_ARGUMENTS = [
    '-no-ansi', '-b', '-j'
]


class TranslateShell:
    def __init__(self, params):
        self.from_lang = 'auto'
        self.to_lang = 'auto'
        self.args = [];
        self._parse_params(params)


    def _parse_params(self, params):
        lang = None

        while len(params):
            param = params[0]

            if param[0] == '-':
                if param in ALLOWED_PARAMS:
                    self.args.append(param)
            elif ':' in param and lang is None:
                lang = param
            else:
                break

            params.pop(0)

        if lang is not None:
            (from_lang, to_lang) = lang.split(':')

            if from_lang:
                self.from_lang = from_lang
            if to_lang:
                self.to_lang = to_lang

        self.query = ' '.join(params)


    def is_dep_missing(self):
        return subprocess.Popen('trans -h', shell=True, stdout=subprocess.PIPE).wait() == 127


    def get_lang_argument(self):
        (from_lang, to_lang) = (
            self.from_lang if self.from_lang != 'auto' else '',
            self.to_lang if self.to_lang != 'auto' else ''
        )

        if not from_lang and not to_lang:
            return ''

        return from_lang + ':' + to_lang


    def get_arguments(self):
        return strip_list([
            'trans',
            *self.args,
            self.get_lang_argument(),
            *FORCED_ARGUMENTS,
            self.query
        ]);


    def has_query(self):
        return len(self.query) > 0


    def execute(self):
        items = []

        result = subprocess.check_output(self.get_arguments(), encoding='utf-8')
        lines = strip_list(result.split('\n'))

        if len(lines) == 0:
            return items

        langs = self.to_lang.split('+')
        for i in range(len(langs)):
            items.append((lines[i], self.query, langs[i]))

        return items