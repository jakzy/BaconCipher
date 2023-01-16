import json
import re

from reveal_no_red import prepare_html, MyHTMLParser

true_val = 'A'
false_val = 'B'
third_val = 'C'

english_dict = [{"a": "AAAAA",
                 "b": "AAAAB",
                 "c": "AAABA",
                 "d": "AAABB",
                 "e": "AABAA",
                 "f": "AABAB",
                 "g": "AABBA",
                 "h": "AABBB",
                 "i": "ABAAA",
                 "j": "ABAAB",
                 "k": "ABABA",
                 "l": "ABABB",
                 "m": "ABBAA",
                 "n": "ABBAB",
                 "o": "ABBBA",
                 "p": "ABBBB",
                 "q": "BAAAA",
                 "r": "BAAAB",
                 "s": "BAABA",
                 "t": "BAABB",
                 "u": "BABAA",
                 "v": "BABAB",
                 "w": "BABBA",
                 "x": "BABBB",
                 "y": "BBAAA",
                 "z": "BBAAB",
                 " ": "BBBBB"},

                {"a": "AAA",
                 "b": "AAB",
                 "c": "AAC",
                 "d": "ABA",
                 "e": "ABB",
                 "f": "ABC",
                 "g": "ACA",
                 "h": "ACB",
                 "i": "ACC",
                 "j": "BAA",
                 "k": "BAB",
                 "l": "BAC",
                 "m": "BBA",
                 "n": "BBB",
                 "o": "BBC",
                 "p": "BCA",
                 "q": "BCB",
                 "r": "BCC",
                 "s": "CAA",
                 "t": "CAB",
                 "u": "CAC",
                 "v": "CBA",
                 "w": "CBB",
                 "x": "CBC",
                 "y": "CCA",
                 "z": "CCB",
                 " ": "CCC"}

                ]


def letter_to_bool(letter: str):
    return letter == false_val


def count_letters(entered_str):
    return sum([char.isalpha() for char in entered_str])


class HamLetter:
    letter: str
    result: str
    def_format: dict = {"reg": None,
                        "underline": None,
                        "bold": None,
                        "ital": None,
                        "color": None}

    def __init__(self, ltr, fmt=None):
        self.letter = ltr
        self.letter_format = dict(self.def_format)
        if fmt:
            self.set_format(fmt)

    def __repr__(self):
        return f"{self.letter} : {self.letter_format}"

    def set_format(self, ciph: str):
        format_values = []
        for letter in ciph:
            format_values.append(letter_to_bool(letter))

        self.letter_format.update(zip(self.letter_format, format_values))


def ham_array_to_string(ham_letter_array):
    res_string = ''
    for letter in ham_letter_array:
        if isinstance(letter, HamLetter):
            cur_letter = letter.letter
            if letter.letter_format["reg"]:
                cur_letter = cur_letter.upper()
            else:
                cur_letter = cur_letter.lower()
            if letter.letter_format["underline"]:
                cur_letter = f"<u>{cur_letter}</u>"
            if letter.letter_format["bold"]:
                cur_letter = f"<b>{cur_letter}</b>"
            if letter.letter_format["ital"]:
                cur_letter = f"<i>{cur_letter}</i>"
            if letter.letter_format["color"]:
                cur_letter = f"<font color=blue>{cur_letter}</font>"
        else:
            cur_letter = letter.lower()
        res_string += cur_letter
    return res_string


class BaconEncryptor:
    template = {"reg": None,
                "underline": None,
                "bold": None,
                "ital": None,
                "color": None}

    def __init__(self, alph_dict=None, remove_redundancy=False, alph_file_path=None, mode=2):
        self.result = ""
        self.mode = mode
        if alph_dict is not None:
            self.alph = alph_dict.copy()
        elif alph_file_path is not None:
            self.get_alph_from_json(alph_file_path)
        else:
            self.alph = english_dict[mode - 2]

        if remove_redundancy:
            self.process = self.hide_message_no_redundant
            self.reveal_message_binary = self.reveal_message_no_redundant
        else:
            self.process = self.hide_message_simple
            self.reveal_message_binary = self.reveal_message_simple

        self.alph_reversed = {y: x for x, y in self.alph.items()}

    def __repr__(self):
        return self.result

    def letter_in_alph(self, letter):
        return letter in self.alph.keys()

    def process(self, message: str, container: str):
        pass

    def setmode(self, mode=2):
        self.mode = mode

    def getmode(self):
        return self.mode

    def hide_message_no_redundant(self, message: str, container: str):
        """
        Gets message to hide and container, returns container with hidden message in it
        :param message:
        :param container:
        :return:
        """
        if len(message) == 0:
            self.result = container
            return container
        if count_letters(container) < len(message):
            self.result = "container too short, try another one"
            return "container too short, try another one"

        ham_letter_array = []
        ltr_count = 0
        msg_ = ''.join(filter(lambda seq: self.letter_in_alph(seq), message.lower()))
        result = ''

        for i in range(len(container)):

            if container[i].isalpha():
                ham_letter_array.append(HamLetter(container[i], self.alph[msg_[ltr_count]]))
                ltr_count += 1
                if ltr_count == len(msg_):
                    result += container[i + 1:]
                    ham_letter_array.append(container[i + 1:])
                    break
            else:
                result += container[i]
                ham_letter_array.append(container[i])
        self.result = ham_array_to_string(ham_letter_array)
        return self.result

    def hide_message_simple(self, message: str, container):
        if len(message) == 0:
            self.result = container
            return container
        if count_letters(container) < len(message) * (5 if self.mode == 2 else 3):
            self.result = "container too short, try another one"
            return "container too short, try another one"

        ltr_count = 0
        msg_ = ''.join(filter(lambda seq: self.letter_in_alph(seq), message))
        curr_code = self.alph[msg_[0]]
        result = ''

        for i in range(len(container)):
            if container[i].isalpha():
                if curr_code[0] == true_val:
                    result += container[i].upper()
                elif curr_code[0] == false_val:
                    result += container[i].lower()
                elif curr_code[0] == third_val:
                    result += f"<b>{container[i]}</b>"
                if len(curr_code) > 1:
                    curr_code = curr_code[1:]
                else:
                    ltr_count += 1
                    if ltr_count < len(msg_):
                        curr_code = self.alph[msg_[ltr_count]]
                    else:
                        result += container[i + 1:]

                        break
            else:
                result += container[i]
        self.result = result
        return result

    def reveal_message_simple(self, container) -> str:
        prepared_html_container = prepare_html(container)
        cleared_container = ''.join(filter(str.isalpha, prepared_html_container))
        n = 5
        chunks = [cleared_container[i:i + n] for i in range(0, len(cleared_container), n)]
        chunks = [''.join([true_val if x.isupper() else false_val for x in chunk]) for chunk in chunks]
        msg_ = ''.join([self.alph_reversed.get(chunk) if self.alph_reversed.get(chunk) else '' for chunk in chunks])
        return msg_

    def reveal_message_no_redundant(self, container):
        prepared_html_str = prepare_html(container)
        parser = MyHTMLParser()
        parser.init_dict(self.alph)
        parser.feed(prepared_html_str)
        msg_ = parser.get_result()
        return msg_

    def reveal_message_binary(self, container):
        pass

    def filter_mode3(self, str):
        if (str.isalpha()) or (str == '*'):
            return True
        else:
            return False

    def reveal_message_mode3(self, container) -> str:
        prepared_html_container = prepare_html(container)
        prepared_html_container = re.sub('<i>|</i>|<u>|</u>|<font color=blue>|</font>|<b> </b>', '', prepared_html_container)
        prepared_html_container = re.sub('<b>[a-zA-Z]</b>', '*', prepared_html_container)
        cleared_container = ''.join(filter(self.filter_mode3, prepared_html_container))
        n = 3
        chunks = [cleared_container[i:i + n] for i in range(0, len(cleared_container), n)]
        print(chunks)
        chunks = [''.join([third_val if x == '*' else true_val if x.isupper() else false_val for x in chunk]) for chunk
                  in chunks]
        print(chunks)
        msg_ = ''.join([self.alph_reversed.get(chunk) if self.alph_reversed.get(chunk) else '' for chunk in chunks])
        return msg_



    def get_alph_from_json(self, file_name):
        with open(file_name, 'r') as alph_file:
            alph_data = json.load(alph_file)
            self.alph = alph_data


if __name__ == "__main__":
    mr_bacon = BaconEncryptor(alph_dict=english_dict[0], remove_redundancy=True)

    cont_text = 'abcd'
    # cont_text = 'Привет, как дела?'
    msg = 'qwRr'

    # mr_bacon.get_alph_from_json("C:\\Users\\wensd\\PycharmProjects\\pythonProject3\\test_alph.json")
    # res = mr_bacon.process(msg, cont_text)
    # print(mr_bacon)

    res = mr_bacon.process(msg, cont_text)
    # res_res = mr_bacon.reveal_message_simple(res)

    print(res)
    print(mr_bacon)

# kk = {"reg": None,
#      "underline": None,
#      "bold": None,
#      "ital": None,
#      "color": None}

# vals = [1, 2, 3, 4, 5]
#
# for val in kk.items():
#    print(val)
#
# kk.update(zip(kk, vals))
#
# for val in kk.items():
#    print(val)
#
