import math
import os
import random
import re
import shutil
import string
import tempfile
import unittest
from difflib import SequenceMatcher
from itertools import combinations
from typing import Iterable as type_iter
from typing import Optional
from collections.abc import Iterable as coll_iter
from subprocess import PIPE, Popen
from time import sleep
from typing import Union, List

BASE_DIR = os.path.dirname(os.path.realpath(__file__))


class RandomWords:
    def __init__(self):
        self.words = {}
        file_path = find_file("safe_dictionary.txt")
        if not file_path:
            raise FileNotFoundError(
                "Unable to find the file safe_dictionary.txt in the professor's test"
                " code."
            )

        with open(file_path, "r") as f:

            for word in f.readlines():
                word = word.strip()
                word_len = len(word)

                if word_len not in self.words:
                    self.words[word_len] = []

                self.words[word_len].append(word)

        self.max_word_len = max(self.words.keys())
        self.min_word_len = min(self.words.keys())

    def __to_validate_range(
        self, num_range: Union[int, type_iter[int]], var_name
    ):
        if isinstance(num_range, coll_iter):
            num_range = list(num_range)

            if len(num_range) != 2:
                raise ValueError(
                    f"If {var_name} is an iterable it must contain 2 integers. "
                    f"Instead an iterable length {len(num_range)} was received."
                )

            for len_param in num_range:
                if not isinstance(len_param, int):
                    raise TypeError(
                        f"If {var_name} is an iterable it must contain 2 integers. "
                        f"Instead {type(len_param).__name__} was received."
                    )

            return random.randint(*num_range)

        return num_range

    def __to_valid_word_len(self, word_len: Union[int, type_iter[int]] = -1):
        if isinstance(word_len, coll_iter):
            word_len = list(word_len)

            if len(word_len) != 2:
                raise ValueError(
                    "If word_len is an iterable it must contain 2 integers. "
                    f"Instead an iterable length {len(word_len)} was received."
                )

            for len_param in word_len:
                if not isinstance(len_param, int):
                    raise TypeError(
                        "If word_len is an iterable it must contain 2 integers. "
                        f"Instead {type(len_param).__name__} was received."
                    )

            word_len = [
                max(self.min_word_len, word_len[0]),
                min(self.max_word_len, word_len[1]),
            ]
            word_len = [
                self.min_word_len if word_len[0] <= 0 else word_len[0],
                self.max_word_len if word_len[1] <= 0 else word_len[1],
            ]

            lengths = []
            for temp_len in range(*word_len):
                if temp_len in self.words:
                    lengths.append(temp_len)
            if not lengths:
                raise AttributeError(
                    f"There are no words with the a length between {word_len[0]} -"
                    f" {word_len[1]} in the dictionary."
                )

            word_len = random.choice(lengths)

        elif word_len <= 0:
            word_len = random.choice(list(self.words.keys()))

        elif word_len not in self.words:
            raise AttributeError(
                f"There are no words of length {word_len} in the dictionary."
            )

        return word_len

    def random_word(self, word_len: Union[int, type_iter[int]] = -1) -> str:
        word_len = self.__to_valid_word_len(word_len)

        return random.choice(self.words[word_len])

    def random_sentence(
        self,
        sentence_len: Union[int, type_iter[int]] = 5,
        word_len: Union[int, type_iter[int]] = -1,
    ) -> str:

        sentence_len = self.__to_validate_range(sentence_len, "sentence_len")
        return " ".join(
            [self.random_word(word_len) for _ in range(sentence_len)]
        )

    def random_paragraph(
        self,
        paragraph_len: Union[int, type_iter[int]] = 10,
        sentence_len: Union[int, type_iter[int]] = 10,
        word_len: Union[int, type_iter[int]] = -1,
    ) -> str:
        paragraph_len = self.__to_validate_range(paragraph_len, "paragraph_len")
        return "\n".join(
            [
                self.random_sentence(sentence_len, word_len)
                for _ in range(paragraph_len)
            ]
        )


def find_numbers(text):
    numbers = []

    for segs in text.split():
        str_num = "".join(c for c in segs if (c.isdecimal() or c in "-."))

        if str_num.endswith(".") or str_num.endswith("-"):
            str_num = str_num[:-1]

        if (
            len(str_num) > 0
            and str_num.replace("-", "").replace(".", "").isdecimal()
        ):
            num = float(str_num) if "." in str_num else int(str_num)
            numbers.append(num)

    return numbers


def match_numbers(
    expected_num: Union[float, int],
    search_num: type_iter[Union[float, int]],
    places: Optional[int] = None,
    delta: Optional[Union[float, int]] = None,
):
    if delta is not None and places is not None:
        raise TypeError("specify delta or places not both")

    for num in search_num:

        diff = abs(expected_num - num)

        if (
            num == expected_num
            or delta is not None
            and diff <= delta
            or round(diff, places) == 0
        ):
            return True

    return False


def random_string(n=20, p=None) -> str:
    """
    This will generate a string with a length between n and p. If just n specified the string will be n length

    :param n: min length
    :param p: max length
    :return:
    """
    if p is not None:
        n = random.randint(n, p)

    return "".join(
        random.SystemRandom().choice(string.ascii_letters + string.digits)
        for _ in range(n)
    )


def similar(
    text_1,
    text_2,
    threshold=0.75,
):
    """
    Test if the two text are similar. This uses Ratcliff/Obershelp algorithm to compute the string
    similarity.The strings are considered similar if the algorithm produce a value greater than or equal to the
    threshold.

    :param text_1: A string value to be compared to text 2
    :param text_2: A string value to be compared to text 1
    :param threshold: The ratio of similarity. A higher value means the text must be a closer match for this function to return true.
    :return: True if the text values are similar
    """

    return SequenceMatcher(None, text_1, text_2).ratio() >= threshold


def contains_similar(
    text_1,
    text_2,
    threshold=0.75,
):
    """
    This tests if larger of text_1 or text_2 contains a similar substring of the smallest of the text values. It
    splits the larger text value into sub-strings on white space charactures and then checks if any of those
    sub-strings are similar to the smaller text value using the similar() function.

    **WARNING:** This does not preform well with large text values greater than 100 words. This is not meant to be
    used if white space characters have meaning.

    :param text_1: A string value to be compared to text 2
    :param text_2: A string value to be compared to text 1
    :param threshold: The ratio of similarity. A higher value means the text must be a closer match for this function to return true.
    :return: True if the text values are similar
    """

    norm_text_1 = clean_text(
        text_1,
        remove_non_alpha_num=False,
        normalize_space=True,
        to_lower=False,
        trim=True,
    )

    norm_text_2 = clean_text(
        text_2,
        remove_non_alpha_num=False,
        normalize_space=True,
        to_lower=False,
        trim=True,
    )

    if len(norm_text_1.split()) > len(norm_text_2.split()):
        larger = text_1
        smaller = text_2
    else:
        larger = text_2
        smaller = text_1

    word_list = larger.split()
    length = len(word_list) + 1
    segments = [
        " ".join(word_list[x:y]) for x, y in combinations(range(length), r=2)
    ]

    for segment in segments:
        if similar(segment, smaller, threshold=threshold):
            return True

    return False


def clean_text(
    text: str,
    remove_non_alpha_num: bool = True,
    normalize_space: bool = True,
    to_lower: bool = True,
    trim: bool = True,
):
    if remove_non_alpha_num:
        text = re.sub(r"[^\d\w\s]", "", text)
    if normalize_space:
        text = re.sub(" +", " ", text)
    if to_lower:
        text = text.lower()
    if trim:
        text = text.strip()

    return text


class ScriptComm:
    """
    A context manager that may be used to test a script. This will take care of running the script and provide
    easy methods to communicate with the running script.
    """

    def __init__(self, script_name: str, test_case: unittest.TestCase):
        """
        Initializes the context manager
        :param script_name: The name of the python script to be run. This file must be located in the same directory as this module.
        :param test_case: The test case of the current test.
        """
        self._test_case = test_case
        self._script_name: str = (
            script_name if script_name.endswith(".py") else f"{script_name}.py"
        )
        self._script_path: str = find_file(self._script_name)
        if self._script_path is None:
            self._test_case.fail(f"The file {self._script_name} is missing.")
        self._process: Popen = None

        self._temp_dir = tempfile.mkdtemp()
        self._strout_file_path = os.path.join(self._temp_dir, "strout_file")
        self._strout_fp = open(self._strout_file_path, "w+")
        self._strerr_file_path = os.path.join(self._temp_dir, "strerr_file")
        self._strerr_fp = open(self._strerr_file_path, "w+")

    def write(self, s, check_error=True, append_enter=True) -> None:
        """
        Sends the specified string to the running process's stdin. This is similar to how a human user would type
        keyboard input then pressing [Enter].

        :param s: The string to be inputted into the running process.
        :param check_error: If True this will preform a check to see if the application has ended with a non-zero exit code before writing the input. If the application has exited with a non-zero code the test will fail and the entire standard err will be used as the message for the reason of the test failure. This defaults to True.
        :param append_enter: If true this will append a newline character to the end of the string if it does not already end with a new line character. This is similar to pressing [Enter] after typing in a new line into the console.
        :return: None
        """
        if check_error:
            self.check_error()

        if self._process.poll() == None:
            s = str(s)

            if append_enter and not s.endswith("\n"):
                s += "\n"

            self._process.stdin.write(s)
            self._process.stdin.flush()
        else:
            self._test_case.fail(
                "Your script ended prematurely before the following input could be"
                f' sent to it "{s}"'
            )

    def _validate_start(self):
        if self._process is None:
            return ValueError("The process has not been started yet.")

    def check_error(self, msg="") -> None:
        """
        A check to see if the application has ended with a non-zero exit code. If this occurs the
        test will fail and the entire standard err will be used as the message for the reason of the test failure.

        :return: None
        """
        if self._process.poll() not in (0, None) and os.path.exists(
            self._strerr_file_path
        ):
            with open(self._strerr_file_path, "r") as f:
                self._test_case.fail(
                    f"{msg} An error occurred while executing your script. Below is the"
                    " error output of your"
                    f' application:\n\n{"=" * 30}\n{f.read()}\n{"=" * 30}'
                )

    def read(
        self, last_line: bool = True, check_errors: bool = True, wait: float = 1
    ) -> str:
        """
        This will return the stdout of the file. Similar to how a human would read the console output of a running
        application this will return the console output of the running application as a string.

        :param last_line: If true this will only read the last line written to the str out stream. Otherwise this will read the entire output stream. This defaults to True.
        :param check_errors: If True this will preform a check to see if the application has ended with a non-zero exit code before reading the output. If the application has exited with a non-zero code the test will fail and the entire standard err will be used as the message for the reason of the test failure. This defaults to True.
        :param wait: The time in seconds the application will wait before reading the output. If this value is None or less than zero no wait will occur. This defaults to 1 second.
        :return: A string representing the console output.
        """

        if wait is not None and wait > 0:
            sleep(wait)

        if check_errors:
            self.check_error()

        self._validate_start()

        with open(self._strout_file_path, "r") as f:
            f.seek(0)
            if last_line:
                line = ""
                for line in f:
                    pass
                return line
            else:
                return f.read()

    def read_num(
        self, last_line: bool = True, check_errors: bool = True, wait: float = 1
    ) -> List[Union[float, int]]:
        """
        This will return a list of any numbers found the stdout of the file. Similar to how a human would read the
        console output of a running application and find the numbers in the text, this will return the numbers in the
        console output of the running application as a float or int. The numbers will be segmented based on any white
        space found in the output string.

        :param last_line: Same as the read() method
        :param check_errors: Same as the read() method
        :param wait:  Same as the read() method
        :return: A list of any numbers found in the stdout, in the order they are found.
        """

        raw_output = self.read(last_line, check_errors, wait)

        numbers = find_numbers(raw_output)

        if not numbers:
            self._test_case.fail(
                "Your application is not returning any numerical output. Please make"
                " sure your application is printing a number. Your application is"
                f' printing the following string "{raw_output.strip()}".'
            )

        return numbers

    def contains_number(
        self,
        expected_num: Union[float, int],
        places: int = None,
        delta: Union[float, int] = None,
        last_line: bool = True,
        check_errors: bool = True,
        wait: float = 1,
    ):
        """
        This is used to test if any number in the output of the application is approximately equal to an expected
        number.

        :param expected_num: A number that will be searched for
        :param places: decimal places for approximation.
        :param delta: delta value for approximation.
        :param last_line: Same as the read() method
        :param check_errors: Same as the read() method
        :param wait: Same as the read() method
        :return: True if the output of the application contains at least one number that is almost equal to the specified expected number.
        """

        if delta is not None and places is not None:
            raise TypeError("specify delta or places not both")

        numbers = self.read_num(last_line, check_errors, wait)

        return match_numbers(
            expected_num=expected_num,
            search_num=numbers,
            places=places,
            delta=delta,
        )

    def alive(self):
        """
        Tests if the application is still running.
        :return: True the process is alive
        """
        return self._process.poll() is None

    def __enter__(self):
        self._process: Popen = Popen(
            ["python3", self._script_path],
            universal_newlines=True,
            stdout=self._strout_fp,
            stdin=PIPE,
            stderr=self._strerr_fp,
            encoding="utf-8",
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        try:
            self._strout_fp.close()
            self._strerr_fp.close()
            shutil.rmtree(self._temp_dir)
        finally:
            self._process.stdin.close()
            self._process.terminate()
            self._process.wait(10)
            self.check_error()

            if self._process.poll() is None:
                self._process.kill()
                self._test_case.fail(
                    f"Your script will not properly exit. For some reason or another it"
                    f" is frozen. Please make sure you do not have any redundant"
                    f" input() statements or infinite loops."
                )


def find_file(name, case_insensitive=False):
    root_dir = os.environ.get("GT_PROJECT_ROOT", BASE_DIR)
    check_name = name.casefold() if case_insensitive else name
    skip_dirs = (
        os.path.join(root_dir, "temp_mod"),
        os.path.join(root_dir, "tmp"),
    )
    for root, dirs, files in os.walk(root_dir):
        path = os.path.join(root, name)
        if check_name in (
            f.casefold() if case_insensitive else f for f in files
        ) and not any(skip in path for skip in skip_dirs):
            return os.path.join(root, name)
