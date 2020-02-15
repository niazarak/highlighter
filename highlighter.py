import spacy
import math
from spacy.tokens import Token


def approach_1(h, d):
    """
    POS-based highlighting, the most simple approach 
    """
    for token in d:
        #print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
        #      token.shape_, token.is_alpha, token.is_stop)
        if token.pos_ in {"NOUN", "PROPN", "PRON"} and token.dep_ in {"nsubj", "attr"}:
            h.append("<span class=\"noun\">%s</span>" % token.text)
        elif token.pos_ in {"AUX", "VERB"}:
            h.append("<span class=\"verb\">%s</span>" % token.text)
        else:
            h.append("<span class=\"text\">%s</span>" % token.text)


Token.set_extension('height', default=0)
def height(token, h=1) -> int:
    """
    Assigns height to each node in the dependency graph
    Height value may be used in highlighting
    """
    if not len(list(token.children)):
        token._.height = h
        return h
    token._.height = h
    return max([height(t, h + 1) for t in token.children])


def hsv_to_rgb(h, s, v):
    h60 = h / 60.0
    h60f = math.floor(h60)
    hi = int(h60f) % 6
    f = h60 - h60f
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    r, g, b = 0, 0, 0
    if hi == 0: r, g, b = v, t, p
    elif hi == 1: r, g, b = q, v, p
    elif hi == 2: r, g, b = p, v, t
    elif hi == 3: r, g, b = p, q, v
    elif hi == 4: r, g, b = t, p, v
    elif hi == 5: r, g, b = v, p, q
    r, g, b = int(r * 255), int(g * 255), int(b * 255)
    return r, g, b


def token_to_hue(token):
    if token.pos_ in {"NOUN"}:
        return 190.0
    elif token.pos_ in {"PROPN", "PRON"}:
        return 190.0
    elif token.pos_ in {"AUX", "VERB"}:
        return 325.0
    elif token.pos_ in {"ADP"}:
        return 248.0
    else:
        return 140.0


def approach_2(h, d):
    """
    Height-based highlighting, mostly for debugging
    """
    for sent in d.sents:
        hei = height(sent.root)
        for token in sent:
            color = hex(64 + 192 - int((token._.height) / (hei) * 192))
            formatted_color = color[2:] * 3
            h.append("<span style=\"color: #%s\">%s</span>" % (formatted_color, token))


def approach_3(h, d):
    """
    POS + tree-height based approach
    This was written a year ago and I barely understand what this code does
    """
    for sent in d.sents:
        hei = height(sent.root)
        for token in sent:
            if not token.is_punct:
                value = 0.3 + (1 - (token._.height) / (hei)) * 0.7
                # value = 1.0
                formatted_color = ','.join([str(v) for v in hsv_to_rgb(token_to_hue(token), 0.80, value)])
            else:
                formatted_color = '135,144,138'
            h.append("<span style=\"color: rgb(%s)\">%s</span>" % (formatted_color, token))

nlp = spacy.load('en_core_web_sm')
with open("text.txt") as f:
    text = "".join(f.readlines())
    # doc = nlp(u'Apple is looking at buying U.K. startup for $1 billion')
    doc = nlp(text)

html = []
html.append("<html>")
html.append("<head>")
html.append("<title>Highlighter</title>")
html.append("</head>")
html.append("<body>")
html.append("<style>")
html.append("body{ background-color:#2c292d; font-family: Courier,monospace }")
html.append(".noun{ color:#78dce8 }")
html.append(".verb{ color:#a9dc76 }")
html.append(".text{ color:#fcfcfa }")
html.append("</style>")

html.append("<p>")
html.append("<span class=\"text\">%s</span>" % text)
html.append("</p>")
html.append("<p>")
approach_1(html, doc)
html.append("</p>")
html.append("<p>")
approach_2(html, doc)
html.append("</p>")
html.append("<p>")
approach_3(html, doc)
html.append("</p>")
html.append("</body>")
html.append("</html>")

html = "\n".join(html)
# print(html)


with open("index.html", 'w') as f:
    f.write(html)

