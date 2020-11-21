def strip_list(elements):
    return [element for element in elements if len(element.strip()) > 0]


def arg_to_help(arg):
    return {
        '-p': 'Listen to the translation',
        '-sp': 'Listen to the original text',
    }[arg]