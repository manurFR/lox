import subprocess
from pytest import fixture


@fixture
def run_lox(tmp_path):
    def _run_lox(command, lox_source):
        with open(tmp_path / "integration.lox", "w") as sf:
            sf.writelines(lox_source)

        cmd = ["python3", "-m", "app.main", command, str(tmp_path / "integration.lox")]
        process = subprocess.run(cmd, text=True, capture_output=True, timeout=1)
        if process.returncode not in (0, 65, 70):
            raise RuntimeError(process.stderr.rstrip())
        return process.returncode, process.stdout.rstrip(), process.stderr.rstrip()
    return _run_lox