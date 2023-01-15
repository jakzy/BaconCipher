from html.parser import HTMLParser
from bacon_binary_hide import english_dict

html_str = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
<html><head><meta name="qrichtext" content="1" /><meta charset="utf-8" /><style type="text/css">
p, li { white-space: pre-wrap; }
hr { height: 1px; border-width: 0; }
</style></head><body style=" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;">
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">aAAAA<span style=" font-weight:700;">aa</span><span style=" font-weight:700; font-style:italic;">aaa</span><span style=" font-style:italic;">a</span><span style=" font-style:italic; text-decoration: underline;">a</span><span style=" text-decoration: underline;">aaaa</span><span style=" text-decoration: underline; color:#0000ff;">aa</span><span style=" color:#0000ff;">aaaaaa</span></p></body></html>
"""

#english_dict_reversed = {y: x for x, y in english_dict.items()}

true_val = 'A'
false_val = 'B'

def make_chunk(tags):
    res  = true_val if not tags["reg"] else false_val
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

    def handle_data(self, data):
        if len(self.current_letter_tags) != 0:
            current_chunk = make_chunk(self.current_letter_tags)
            self.result_chunks.append(current_chunk)

        self.current_letter_tags = dict(self.def_format)
        self.current_value = {data.lower(): self.current_letter_tags}
        if data.isupper():
            self.current_letter_tags['reg'] = True

    def handle_endtag(self, tag):
        print(tag)
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
        res_string = ""
        for chunk in self.result_chunks:
            #res_string += english_dict_reversed[chunk]
            res_string += chunk
        return res_string



if __name__ == "__main__":

    import sys

    parser = MyHTMLParser()

    parser.feed(html_str)

    print(parser.get_result())
