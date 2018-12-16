import json
from jsbeautifier import beautify
from pygments import highlight, lexers, formatters


def client_required(func: callable) -> callable:
    """ Enforces the selection of a client """

    def _client_required(*args, **kwargs):
        self = args[0]

        if not self.selected_client:
            self.print_error('Please select a client first!')
            return

        return func(*args, **kwargs)

    return _client_required


def get_prompt(shell_instance) -> str:
    """ Returns the current prompt string """

    prompt = shell_instance.t.bold_cyan('>> ')

    if shell_instance.selected_client:
        client_id = shell_instance.t.bold_red(shell_instance.selected_client.cid)
        prompt = shell_instance.t.cyan(f"[Client #{client_id}]") + ' ' + prompt

    return prompt


def js_beautify(code: str, colors=True) -> str:
    """ Returns a colored JS-beautified string (if possible) """

    beautified = beautify(code)

    try:
        json.loads(code)
    except json.JSONDecodeError:
        return beautified

    if not colors:
        return beautified

    return highlight(
        beautified,
        lexers.JsonLexer(),
        formatters.TerminalFormatter()
    )
