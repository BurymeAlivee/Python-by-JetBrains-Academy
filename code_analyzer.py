import argparse
import os
import re
import ast


class Check:
    def __init__(self, path, file, code):
        self.line_ast = None
        self.line = None
        self.path = path
        self.file = file
        self.walk = ast.walk(ast.parse(code))
        self.count_line = 1
        self.count = 0

    def check_s001(self):
        if len(self.line) > 79:
            print(f"{self.path}: Line {self.count_line}: S001 Too long")

    def check_s002(self):
        if self.line != "\n" and (len(self.line) - len(self.line.lstrip())) % 4:
            print(f"{self.path}: Line {self.count_line}: S002 Indentation is not a multiple of four")

    def check_s003(self):
        find_hash = self.line.find("#")
        if find_hash == -1 and self.line.rstrip().endswith(";"):
            print(f"{self.path}: Line {self.count_line}: S003 Unnecessary semicolon")
        elif find_hash != -1 and self.line[:find_hash].rstrip().endswith(";"):
            print(f"{self.path}: Line {self.count_line}: S003 Unnecessary semicolon")

    def check_s004(self):
        find_hash = self.line.find("#")
        if find_hash != -1 and find_hash != 0:
            if not self.line[:find_hash].endswith("  "):
                print(f"{self.path}: Line {self.count_line}: S004 At least two spaces required before inline comments")

    def check_s005(self):
        find_hash = self.line.find("#")
        if find_hash != -1:
            if re.match(r".*[Tt][Oo][Dd][Oo].*", self.line[find_hash + 1:]):
                print(f"{self.path}: Line {self.count_line}: S005 TODO found")

    def check_s006(self):
        if self.line == "\n":
            self.count += 1
        elif self.line != "\n":
            if self.count > 2:
                print(f"{self.path}: Line {self.count_line}: S006 More than two blank lines used before this line")
                self.count = 0
            else:
                self.count = 0

    def check_s007(self):
        if self.line.find("def") != -1 and re.match(r".*def\b \w+", self.line) is None:
            print(f"{self.path}: Line {self.count_line}: S007 Too many spaces after 'def'")
        if self.line.find("class") != -1 and re.match(r".*class\b \w+", self.line) is None:
            print(f"{self.path}: Line {self.count_line}: S007 Too many spaces after 'class'")

    def check_s008(self):
        if isinstance(self.line_ast, ast.ClassDef):
            if re.match(r"[A-Z][A-Za-z]+$", self.line_ast.name) is None:
                print(f"{self.path}: Line {self.line_ast.lineno}: S008 Class name '{self.line_ast.name}' should use "
                      f"CamelCase")

    def check_s009(self):
        if isinstance(self.line_ast, ast.FunctionDef):
            if re.match(r"[a-z\d_]+$", self.line_ast.name) is None:
                print(f"{self.path}: Line {self.line_ast.lineno}: S009 Function name '{self.line_ast.name}' should "
                      f"use snake_case")

    def check_s010(self):
        if isinstance(self.line_ast, ast.FunctionDef):
            for i in range(0, len(self.line_ast.args.args)):
                arg = self.line_ast.args.args[i].arg
                if re.match(r"[a-z\d_]+$", arg) is None:
                    print(f"{self.path}: Line {self.line_ast.args.args[i].lineno}: S010 Argument name '{arg}' should "
                          f"be snake_case")

    def check_s011(self):
        if isinstance(self.line_ast, ast.FunctionDef):
            try:
                for i in range(0, len(self.line_ast.body[0].targets)):
                    var = self.line_ast.body[0].targets[i].id
                    if re.match(r"[a-z\d_]+$", var) is None:
                        print(f"{self.path}: Line {self.line_ast.body[0].lineno}: S011 Variable '{var}' should be "
                              f"snake_case")
            except AttributeError:
                pass

    def check_s012(self):
        if isinstance(self.line_ast, ast.FunctionDef):
            for i in range(len(self.line_ast.args.defaults)):
                try:
                    arg_def = self.line_ast.args.defaults[i].elts
                    if isinstance(arg_def, list):
                        print(f"{self.path}: Line {self.line_ast.args.defaults[i].lineno}: S012 Default argument "
                              f"value is mutable")
                except AttributeError:
                    pass

    def all_checks(self):
        for line in self.file:
            self.line_ast = next(self.walk)
            self.line = line
            self.check_s001()
            self.check_s002()
            self.check_s003()
            self.check_s004()
            self.check_s005()
            self.check_s006()
            self.check_s007()
            self.check_s008()
            self.check_s009()
            self.check_s010()
            self.check_s011()
            self.check_s012()
            self.count_line += 1


def checks_file(path):
    with open(path, "r", encoding="utf-8") as file:
        code = open(path).read()
        check = Check(path, file, code)
        check.all_checks()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="you need add files / file path as argument")
    args = parser.parse_args()
    path = args.path
    if path.endswith(".py"):
        checks_file(path)
    else:
        files = os.listdir(path)
        for file in files:
            if file.endswith(".py"):
                checks_file(path + "\\" + file)


if __name__ == "__main__":
    main()
