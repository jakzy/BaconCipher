from html.parser import HTMLParser


html_str = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
<html><head><meta name="qrichtext" content="1" /><meta charset="utf-8" /><style type="text/css">
p, li { white-space: pre-wrap; }
hr { height: 1px; border-width: 0; }
</style></head><body style=" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;">
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">a<span style=" color:#0000ff;">a</span><span style=" font-style:italic;">a</span><span style=" font-weight:700;">a</span><span style=" text-decoration: underline;">a</span>aaa</p></body></html>
"""

true_val = 'A'
false_val = 'B'


class SpanHTMLParser(HTMLParser):
    current_attr = {"underline": False,
                    "bold": False,
                    "ital": False,
                    "color": False}

    result_line = ''

    def handle_starttag(self, tag, attrs):
        for attr in attrs:
            for tag in attr[1].split(";"):
                if "underline" in tag:
                    self.current_attr["underline"] = True
                if "weight:700" in tag:
                    self.current_attr["bold"] = True
                if "italic" in tag:
                    self.current_attr["ital"] = True
                if "color" in tag:
                    self.current_attr["color"] = True

    def handle_data(self, data):
        for c in data:
            curr_c = c
            if self.current_attr["underline"]:
                curr_c = f"<u>{curr_c}</u>"
            if self.current_attr["bold"]:
                curr_c = f"<b>{curr_c}</b>"
            if self.current_attr["ital"]:
                curr_c = f"<i>{curr_c}</i>"
            if self.current_attr["color"]:
                curr_c = f"<font color=blue>{curr_c}</font>"

            self.result_line += curr_c

    def handle_endtag(self, tag):
        for key in self.current_attr.keys():
            self.current_attr[key] = False

    def get_result(self):
        return self.result_line


def prepare_html(long_html):
    new_html = ''
    last_line = long_html.split("\n")[-2] if len(long_html.split("\n")[-1]) == 0 else long_html.split("\n")[-1]
    last_line = last_line[last_line.find(">") + 1:]

    parser = SpanHTMLParser()
    parser.feed(last_line)

    new_html = parser.get_result()
    return new_html


def make_chunk(tags):
    res = true_val if not tags["reg"] else false_val
    res += true_val if not tags["underline"] else false_val
    res += true_val if not tags["bold"] else false_val
    res += true_val if not tags["ital"] else false_val
    res += true_val if not tags["color"] else false_val
    return res


class MyHTMLParser(HTMLParser):
    current_letter_tags = {}
    def_format: dict = {"reg": False,
                        "underline": False,
                        "bold": False,
                        "ital": False,
                        "color": False}
    current_value = {}

    result_chunks = []

    dict_reversed = {}

    def init_dict(self, new_dict):
        self.dict_reversed = {y: x for x, y in new_dict.items()}

    def handle_data(self, data):
        if len(self.current_letter_tags) != 0:
            current_chunk = make_chunk(self.current_letter_tags)
            self.result_chunks.append(current_chunk)

        self.current_letter_tags = dict(self.def_format)
        self.current_value = {data.lower(): self.current_letter_tags}
        if data.isupper():
            self.current_letter_tags['reg'] = True

    def handle_endtag(self, tag):
        if tag == "i":
            self.current_letter_tags['ital'] = True
        elif tag == "b":
            self.current_letter_tags['bold'] = True
        elif tag == "font":
            self.current_letter_tags['color'] = True
        elif tag == "u":
            self.current_letter_tags['underline'] = True
        else:
            pass

    def get_result(self):
        res_string = ''
        for chunk in self.result_chunks:
            res_string += self.dict_reversed[chunk]
        self.result_chunks.clear()
        return res_string
