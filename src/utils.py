from pathlib import Path 

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