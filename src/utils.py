from pathlib import Path 

PROJECT_DIRECTORY: Path = Path(__file__).parent.parent.absolute()
SOURCE_DIRECTORY: Path = PROJECT_DIRECTORY / "src" 
DATA_DIRECTORY: Path = PROJECT_DIRECTORY / "data" 

AUTO_BUILD_DIRECTORIES: tuple[Path] = (
    DATA_DIRECTORY,
)

for directory in AUTO_BUILD_DIRECTORIES: 
    directory.mkdir(exist_ok=True, parents=False)