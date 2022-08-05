class InvalidExpression(Exception):
    pass


class UnknownCommand(Exception):
    pass


class InvalidIdentifier(Exception):
    pass


class InvalidAssignment(Exception):
    pass


def checks():
    if enter.endswith(modef_operator):
        raise InvalidExpression
    elif enter == "/exit":
        print("Bye!")
        quit()
    elif enter == "/help":
        print("help")
    elif enter.startswith("/"):
        raise UnknownCommand


def corrections_enter():
    global enter
    enter = enter.replace("(", "( ")
    enter = enter.replace(")", " )")
    for _ in range(len(enter)):
        if enter.find("++") != -1:
            enter = enter.replace("++", "+")
        if enter.find("--") != -1:
            enter = enter.replace("--", "+")
        if enter.find("+-") != -1:
            enter = enter.replace("+-", "-")
        if enter.find("==") != -1:
            enter = enter.replace("==", "=")
        if enter.find("//") != -1:
            raise InvalidExpression
        if enter.find("**") != -1:
            raise InvalidExpression
    for e in modef_operator:
        enter = enter.replace(f"{e}", f" {e} ")

    enter = enter.split()

    if len(enter) > 1 and enter[1].isdigit() and enter[0] not in ("+", "-"):
        raise InvalidExpression


def convert_to_postfix():
    priority = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    stack = list()
    output = ""
    for char in enter:
        if char not in operator:
            output += char + " "
        elif char == "(":
            stack.append("(")
        elif char == ")":
            while stack and stack[-1] != "(":
                output += stack.pop() + " "
            stack.pop()
        else:
            while stack and stack[-1] != '(' and priority[char] <= priority[stack[-1]]:
                output += stack.pop() + " "
            stack.append(char)
    while stack:
        output += stack.pop() + " "

    return output


def calc_postfix():
    stack = []
    for char in postfix.split():
        if char.isdigit():
            stack.append(int(char))
        elif char in operator and len(postfix.split()) > 2:
            first = stack.pop()
            second = stack.pop()

            if char == "+":
                stack.append(second + first)
            elif char == "-":
                stack.append(second - first)
            elif char == "*":
                stack.append(second * first)
            elif char == "/":
                stack.append(second // first)
            elif char == "^":
                stack.append(second ** first)
        elif char == "-" or char == "+":
            stack.append(char)
            stack.reverse()
        else:
            raise InvalidExpression
    return "".join(list(map(str, stack)))


def variable_check():
    if not enter[0].isalpha():
        raise InvalidIdentifier
    elif len(enter) > 3:
        raise InvalidAssignment
    elif not enter[2].isdigit() and not enter[2].isalpha():
        raise InvalidAssignment


def variable_add():
    variables[enter[0]] = enter[2]
    if enter[2].isalpha():
        variables[enter[0]] = variables[enter[2]]


def call_variable_check():
    if not enter[0].isalpha():
        raise InvalidIdentifier


def call_variable():
    print(variables[enter[0]])


def update_variable():
    for i, key in enumerate(enter):
        if key in variables.keys():
            enter[i] = variables[key]


if __name__ == "__main__":
    modef_operator = ('-', '+', '*', '/', '^', '=')
    operator = {'-', '+', '*', '/', '(', ')', '^'}
    variables = dict()
    while True:
        enter = input()
        try:
            checks()
            corrections_enter()
            if len(enter) == 0:
                continue
            if len(enter) == 1 and not enter[0].isdigit():
                call_variable_check()
                call_variable()
            elif enter[1] == "=":
                variable_check()
                variable_add()
            else:
                update_variable()
                postfix = convert_to_postfix()
                print(calc_postfix())
        except InvalidExpression:
            print("Invalid expression")
        except IndexError:
            print("Invalid expression")
        except UnknownCommand:
            print("Unknown command")
        except InvalidIdentifier:
            print("Invalid identifier")
        except InvalidAssignment:
            print("Invalid assignment")
        except KeyError:
            print("Unknown variable")
