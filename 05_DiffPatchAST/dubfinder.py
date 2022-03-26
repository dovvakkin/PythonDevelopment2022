import ast
import sys
import difflib
import inspect
import argparse
import textwrap
import importlib


CORRECT_ARGV_LEN = 3
EMPTY_IDENTIFIER = '_'
INNER_CLASS_MARKER = '__'
ATTRS_TO_RESET_TO_EMPTY = ('name', 'id', 'arg', 'attr')


def dynamic_import(module):
    return importlib.import_module(module)


def reset_attr_to_empty(node, attr):
    try:
        getattr(node, attr)
        setattr(node, attr, EMPTY_IDENTIFIER)
    except AttributeError as e:
        pass


def remove_identifiers(func_source):
    func_ast = ast.parse(func_source)

    for node in ast.walk(func_ast):
        for attr in ATTRS_TO_RESET_TO_EMPTY:
            reset_attr_to_empty(node, attr)

    return ast.unparse(func_ast)


def get_member_function_sources(obj, prefix=[]):
    getmember_output = inspect.getmembers(obj)

    for name, member in getmember_output:
        if inspect.isclass(member):
            if name.startswith(INNER_CLASS_MARKER):
                continue

            for source in get_member_function_sources(member, [*prefix + [name]]):
                yield source
            continue

        # there is no way to analyze nested functions with inspect module
        if inspect.isfunction(member) or inspect.ismethod(member):
            source = textwrap.dedent(inspect.getsource(member))
            source = remove_identifiers(source)

            yield '.'.join([*prefix + [name]]), source

            continue


def get_module_functions(module_name):
    module = dynamic_import(module_name)

    return {name: source for name, source in \
            get_member_function_sources(module, [module_name])}


def yield_similar_pairs(name_to_source1, name_to_source2):
    for name1 in name_to_source1:
        for name2 in name_to_source2:
            if name1 == name2:
                continue

            if difflib.SequenceMatcher(None, name_to_source1[name1], name_to_source2[name2]).ratio() > 0.95:
                yield name1, name2


def parse_args():
    if len(sys.argv) == CORRECT_ARGV_LEN:
        return sys.argv[1:]

    print("Incorrect number of arguments", file=sys.stderr)
    exit(1)



def main():
    module1, module2 = parse_args()
    name_to_source1 = get_module_functions(module1)
    name_to_source2 = get_module_functions(module2)

    # output is lexicographically sorted due to dict key order
    for name1, name2 in yield_similar_pairs(name_to_source1, name_to_source2):
        print('{} {}'.format(name1, name2))


if __name__ == '__main__':
    main()
