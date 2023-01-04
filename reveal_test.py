from html.parser import HTMLParser
from bacon_binary_hide import english_dict

html_str = "A<i><b>B</b></i><font color=blue>C</font><font color=blue>D</font>"

english_dict_reversed = {y: x for x, y in english_dict.items()}

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
            res_string += english_dict_reversed[chunk]
        return res_string



if __name__ == "__main__":

    import sys

    parser = MyHTMLParser()

    parser.feed(html_str)

    print(parser.get_result())
