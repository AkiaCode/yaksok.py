import codecs, encodings

def yaksok_source(code):
    return r"""from yaksok.yacc import compile_code
from yaksok import bootbakyi
import copy
code = compile_code('''{code}''', file_name=None)
locals_dict = {}
g = copy.deepcopy({k:getattr(bootbakyi, k) for k in dir(bootbakyi)})
locals_dict['____functions'] = g['____functions']
exec(code, g, locals_dict)
""".replace("{code}", code)

def yaksok_decode(input, errors="strict"):
    raw = bytes(input).decode("utf-8")
    hooked = yaksok_source("\n".join(raw.splitlines()[1:]))
    return hooked, len(input)

def search_coding(encoding):
    if encoding != "yaksok":
        return None
    utf8 = encodings.search_function("utf8")
    return codecs.CodecInfo(
        name="yaksok",
        encode=utf8.encode,
        decode=yaksok_decode,
    )

codecs.register(search_coding)