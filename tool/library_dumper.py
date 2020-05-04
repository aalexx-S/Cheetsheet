import distutils.sysconfig as sysconfig
import os
import importlib.util
import inspect
import sqlite3
import argparse


class LibraryDumpaer():

    def __init__(self, output):
        self.std_lib = sysconfig.get_python_lib(standard_lib=True)
        self.db_conn = sqlite3.connect(output)
        self.db_conn.execute('''
            CREATE TABLE python_library (
            function TEXT PRIMARY KEY NOT NULL,
            visited INTEGER NOT NULL)''')

    def __del__(self):
        self.db_conn.close()

    def run(self):
        for root, dirs, files in os.walk(self.std_lib):
            if self.is_bad_package(root):
                continue

            for file in files:
                if self.is_internal_module(file):
                    continue
                path = os.path.join(root, file)
                self.load_module(file, path)

    def is_bad_package(self, root):
        last = os.path.basename(root)
        if last.find('python') == -1:
            return True
        return False

    def is_internal_module(self, file):
        if file[-3:] != '.py':
            return True
        if file == '__init__.py':
            return True
        if file.find('test') != -1 or file.find('_') != -1:
            return True
        return False

    def is_internal_function(self, function):
        if function.startswith('_'):
            return True
        return False

    def load_module(self, file, path):
        try:
            spec = importlib.util.spec_from_file_location(file, path)
            root = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(root)
            root_name = root.__name__[:-3]

            # Work around for os.path package.
            # Note we may have many alias issues, so consider fix it later.
            if root_name == 'posixpath':
                root_name = os.path.join('os', 'path')

            functions = inspect.getmembers(root, inspect.isfunction)
            for pair in functions:
                if self.is_internal_function(pair[0]):
                    continue
                function = os.path.join(root_name, pair[0])

                self.db_conn.execute(
                    '''
                    INSERT or REPLACE INTO python_library
                    (function, visited) VALUES (?, ?)
                ''', (function, 0))
                self.db_conn.commit()

        except Exception as e:
            pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", help="Path to the sqlite dump.")

    args = parser.parse_args()
    if args.output is None:
        print(parser.print_help())
        return

    dumper = LibraryDumpaer(args.output)
    dumper.run()


if __name__ == "__main__":
    main()
