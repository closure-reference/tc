import importlib
import json
from colorama import Fore, Back, Style
import os
import sys
from collections import namedtuple
from argparse import Namespace
from runpy import run_path

from .util import exported
from . import matchers
matchers = exported(matchers)


def get_path(path):
    return os.path.join(sys.path[0], path)


def all_files(folder):
    for name in os.listdir(folder):
        if name.endswith(".py"):
            yield os.path.join(folder, name)


def run_file(file):
    importlib.invalidate_caches()
    if isinstance(file, str):
        file = open(get_path(file))
    run_config(get_config(file))


def get_tests_for_module(module_filename, code_path, test_path):
    module_path = os.path.join(code_path, module_filename)
    module_name = module_filename.replace(".py", "")
    try:
        sys.path.insert(1, os.path.split(module_path)[0])
        module = run_path(module_path)
        return {
            "name": module_name,
            "path": module_path,
            "testables": [*filter(lambda t: os.path.isfile(t["unittest_path"]),
                                  [
                                    {
                                     "name":
                                         name,
                                     "unittest_path":
                                         os.path.join(
                                                      test_path,
                                                      module_name,
                                                      name + ".py"
                                                     )
                                    }
                                   for name in module
                                   if not name.startswith("_")
                                   ])
                         ]
        }
    except Exception as e:
        print(Back.RED + Fore.WHITE
              + f"Error trying to import {module_path}: {e}"
              + Style.RESET_ALL)
        return None



def get_config(file):
    raw_config = json.load(file)

    output = []

    for test_location, code_location in raw_config.items():
        test_path = get_path(test_location)
        code_path = get_path(code_location)

        output.append(list(filter(
                       None,
                       [get_tests_for_module(module_file, code_path, test_path)
                        for module_file in os.listdir(code_path)
                        if module_file.endswith(".py")]
                      )))

    return output


def run_config(config):
    for target in config:
        for module_spec in target:
            test_module(**module_spec)


def test_module(*, name, path, testables):
    module = run_path(path)
    for testable in testables:
        test_testable(module, name, **testable)


def test_testable(module, module_name, *, name, unittest_path):
    subject = module[name]
    tester = run_path(unittest_path)["test"]
    driver = Driver(subject)

    if isinstance(tester, list):
        driver.its_just_data(tester)
    else:
        tester(driver, module)

    print_driver_results(f"{module_name}::{name}",
                         module["__doc__"],
                         driver.tests)


def print_driver_results(name, doc, tests):
    print(Style.BRIGHT + name + Style.RESET_ALL)
    print(doc or Back.MAGENTA + Fore.WHITE + "no docstring!" + Style.RESET_ALL)
    for context, test_results in tests.items():
        indent = (len(context)) * "     "
        if context:
            print(indent + Fore.CYAN + context[-1] + Style.RESET_ALL)
        indent += "     "
        for test_result in test_results:
            print(str_result(test_result, indent))


def align(s, indent):
    return ("\n" + indent).join(s.split("\n"))

def str_result(result, indent):
    title = align(result["title"], indent + "  ")
    if result["expected"] == result["actual"]:
        return indent + Fore.GREEN + "V " + Style.RESET_ALL + title
    else:
        return "\n" \
               + indent + Fore.RED + f"X {title}" \
               + "\n" \
               + indent + Fore.RED + f"   - expected ({result['expected']})" \
               + "\n" \
               + indent + Fore.GREEN + f"   + actual ({result['actual']})" \
               + Style.RESET_ALL \
               + "\n"


def match(subject, test):
    for matcher in matchers.values():
        if matcher["detect"](test):
            return matcher["f"](subject, test)
    return {
        "title": "<failed to load test>",
        "expected": 1,
        "actual": 0
    }


class Driver:
    def __init__(self, subject, context=None):
        if context is None:
            context = []
        self.subject = subject
        self.context = context
        self.tests = {}

    def __call__(self, *args, **kwargs):
        if args:
            [ctx] = args
            self.with_new_context(ctx)
        else:
            self@kwargs

        return self

    def with_new_context(self, new_context):
        self.context.append(new_context)

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        self.context.pop()

    def __matmul__(self, test):
        key = tuple(self.context)
        self.tests[key] = self.tests.get(key, []) + [match(self.subject, test)]
        return self

    def its_just_data(self, its_just_data):
        new_context, tests = its_just_data
        with self(new_context):
            for test in tests:
                if isinstance(test, list):  # subcontext
                    self.its_just_data(test)
                else:  # simple test
                    self @ test

    def __repr__(self):
        return "Driver(" + repr(self.subject) + ", " + repr(self.context) + ")"


__all__ = ["run_file"]
