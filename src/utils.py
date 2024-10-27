import os
from pathlib import Path 
import sys 

PROJECT_DIRECTORY: Path = Path(__file__).parent.parent.absolute()
SOURCE_DIRECTORY: Path = PROJECT_DIRECTORY / "src" 
DATA_DIRECTORY: Path = PROJECT_DIRECTORY / "data" 
MODEL_BIN_DIRECTORY: Path = PROJECT_DIRECTORY / "models"

AUTO_BUILD_DIRECTORIES: tuple[Path] = (
    DATA_DIRECTORY,
    MODEL_BIN_DIRECTORY, 
)

for directory in AUTO_BUILD_DIRECTORIES: 
    directory.mkdir(exist_ok=True, parents=False)

def human_bytes_str(num_bytes: int) -> str:
    units: tuple[str] = ("B", "KB", "MB", "GB")
    power: int = 2**10

    for unit in units:
        if num_bytes < power:
            return f"{num_bytes:.1f} {unit}"

        num_bytes /= power

    return f"{num_bytes:.1f} TB"

class SuppressionContext:
    """
    Reference: https://github.com/abetlen/llama-cpp-python/issues/478
    """
    def __enter__(self):
        self.outnull_file = open(os.devnull, 'w')
        self.errnull_file = open(os.devnull, 'w')

        self.old_stdout_fileno_undup = sys.stdout.fileno()
        self.old_stderr_fileno_undup = sys.stderr.fileno()

        self.old_stdout_fileno = os.dup(sys.stdout.fileno())
        self.old_stderr_fileno = os.dup(sys.stderr.fileno())

        self.old_stdout = sys.stdout
        self.old_stderr = sys.stderr

        os.dup2(self.outnull_file.fileno(), self.old_stdout_fileno_undup)
        os.dup2(self.errnull_file.fileno(), self.old_stderr_fileno_undup)

        sys.stdout = self.outnull_file        
        sys.stderr = self.errnull_file
        return self

    def __exit__(self, *_):        
        sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr

        os.dup2(self.old_stdout_fileno, self.old_stdout_fileno_undup)
        os.dup2(self.old_stderr_fileno, self.old_stderr_fileno_undup)

        os.close(self.old_stdout_fileno)
        os.close(self.old_stderr_fileno)

        self.outnull_file.close()
        self.errnull_file.close()