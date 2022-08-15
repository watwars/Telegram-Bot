
import subprocess
import os
from helpers import utils

dirname = os.path.dirname(__file__)
ERROR_FILE_NAME = os.path.join(dirname, "../code/stderr.txt")
OUTPUT_FILE_NAME = os.path.join(dirname, "../code/stdout.txt")
CODE_BASE_NAME = os.path.join(dirname, "../code/code")


def generate_output(entire_text, language):
    code = ' '.join(entire_text[1:])
    specs = utils.get_language_specs(language)
    filename = f"{CODE_BASE_NAME}.{specs.extension}"
    with open(filename, 'w') as f:
        f.write(code)
    bash_command = specs.command + [filename]
    with open(OUTPUT_FILE_NAME, "w") as out, open(ERROR_FILE_NAME, "w") as err:
        subprocess.call(bash_command, stdout=out, stderr=err)


def get_run_code_message():
    with open(ERROR_FILE_NAME, "r") as f:
        error = str(f.read())
        if error != "":
            return utils.parse_error_message(error)
    with open(OUTPUT_FILE_NAME, "r") as f:
        response = f.read()
        if response == "":
            return "No output, make to sure to include some code and print statements to see actual output."
        return response


def run_interpreted_code(entire_text, language):
    generate_output(entire_text, language)
    return get_run_code_message()


def run_compiled_code(entire_text, language):
    generate_output(entire_text, language)

    # check for compile error
    with open(ERROR_FILE_NAME, "r") as f:
        error = str(f.read())
        if error != "":
            return error

    # Run binary
    run_command = ["./a.out"]
    with open(OUTPUT_FILE_NAME, "w") as out, open(ERROR_FILE_NAME, "w") as err:
        subprocess.call(run_command, stdout=out, stderr=err)
    return get_run_code_message()
