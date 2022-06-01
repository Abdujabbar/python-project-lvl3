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
            "https://ru.hexlet.io/teams",
            "/var/tmp",
            0
        ),
        (
            "https://test.com",
            "/var/tmp",
            1
        ),
    ]
)
def test_cmd_parse_valid(url, output, expected_code):
    command = ["poetry", "run", "page-loader", url, f"-o={output}"]
    _, _, exitcode = capture(command)
    assert exitcode == expected_code, "Trouble while execute"
