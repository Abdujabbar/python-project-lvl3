import pytest
import subprocess


def capture(command):
    proc = subprocess.Popen(command,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)

    out, err = proc.communicate()
    return out, err, proc.returncode


@pytest.mark.parametrize(
    "url, output, expected_code",
    [
        (
            "https://localhost:1233",
            "/var/tmp",
            1
        ),
        (
            "https://test.com",
            "/var/tmp",
            1
        ),
    ]
)
def test_cmd_exception(url, output, expected_code):
    command = ["poetry", "run", "page-loader", url, f"-o={output}"]
    _, _, exitcode = capture(command)
    assert exitcode == expected_code, "Trouble while execute"


def test_cmd_failure():
    command = ["poetry", "run", "page-loader"]
    _, _, exitcode = capture(command)
    assert exitcode != 0, "Trouble cmd args"
