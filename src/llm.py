import ctypes
import dataclasses
import os 
from pathlib import Path
import requests
import subprocess
import sys 
from typing import Optional

import git 
import llama_cpp 
from llama_cpp import Llama 
from rich.progress import Progress

import utils 

class suppress_stdout_stderr(object):
    def __enter__(self):
        self.outnull_file = open(os.devnull, 'w')
        self.errnull_file = open(os.devnull, 'w')

        self.old_stdout_fileno_undup    = sys.stdout.fileno()
        self.old_stderr_fileno_undup    = sys.stderr.fileno()

        self.old_stdout_fileno = os.dup ( sys.stdout.fileno() )
        self.old_stderr_fileno = os.dup ( sys.stderr.fileno() )

        self.old_stdout = sys.stdout
        self.old_stderr = sys.stderr

        os.dup2 ( self.outnull_file.fileno(), self.old_stdout_fileno_undup )
        os.dup2 ( self.errnull_file.fileno(), self.old_stderr_fileno_undup )

        sys.stdout = self.outnull_file        
        sys.stderr = self.errnull_file
        return self

    def __exit__(self, *_):        
        sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr

        os.dup2 ( self.old_stdout_fileno, self.old_stdout_fileno_undup )
        os.dup2 ( self.old_stderr_fileno, self.old_stderr_fileno_undup )

        os.close ( self.old_stdout_fileno )
        os.close ( self.old_stderr_fileno )

        self.outnull_file.close()
        self.errnull_file.close()

LLAMA_CPP_URI: str = "https://github.com/ggerganov/llama.cpp"
LLAMA_CPP_DIRECTORY: Path = utils.PROJECT_DIRECTORY / "llama.cpp"
LLAMA_CPP_BIN: Path = LLAMA_CPP_DIRECTORY / "llama-cli"

def _build_llamacpp() -> None: 
    if not LLAMA_CPP_DIRECTORY.exists(): 
        print("Cloning the repository...")
        git.Repo.clone_from(LLAMA_CPP_URI, str(LLAMA_CPP_DIRECTORY))

    # build the project 
    if not LLAMA_CPP_BIN.exists(): 
        print("Building the project")
        result = subprocess.run(["make"], stdout=subprocess.PIPE, cwd=str(LLAMA_CPP_DIRECTORY))
        print("Finished building the project")

@dataclasses.dataclass
class LLMConfig: 
    # generation
    context_size: Optional[int]=512
    max_tokens: Optional[int]=32
    stop_tokens: Optional[tuple[str]] = ("Q:", "\n")
    echo: Optional[bool]=False
    lazy: Optional[bool]=False

class LLM(Llama): 
    GGUF_URI: str = "https://huggingface.co/ggml-org/gemma-1.1-7b-it-Q4_K_M-GGUF/resolve/main/gemma-1.1-7b-it.Q4_K_M.gguf?download=true"
    GGUF_BIN: Path = utils.MODEL_BIN_DIRECTORY / "custom_model.gguf"

    def __init__(self, config: LLMConfig): 
        self.config = config
        if not self.GGUF_BIN.exists() and not self.config.lazy: 
            self._download()

        with suppress_stdout_stderr(): 
            super().__init__(
                model_path=str(self.GGUF_BIN), 
                n_ctx=self.config.context_size, 
            )

    def _download(self) -> None: 
        _build_llamacpp()
        response = requests.get(self.GGUF_URI, stream=True, timeout=5)

        total_num_bytes: int = int(response.headers.get("content-length", 0))
        block_size: int = 1_024

        print(f"Model binary is {utils.human_bytes_str(total_num_bytes)}")
        print(f"Block size {utils.human_bytes_str(block_size)}")

        with Progress() as progress: 
            download_task = progress.add_task("[red]Downloading...", total=total_num_bytes)
            with open(self.GGUF_BIN, "wb") as file:
                for data in response.iter_content(block_size):
                    progress.update(download_task, advance=len(data))
                    file.write(data)

    def __call__(self, prompt: str) -> str: 
        with suppress_stdout_stderr(): 
            output = super().__call__(
                prompt, 
                max_tokens=self.config.max_tokens, 
                stop=list(self.config.stop_tokens), 
                echo=self.config.echo, 
            )
        return output["choices"][0]["text"]

def main(): 
    config = LLMConfig()
    llm = LLM(config)

    new_ingredient: str = "Chickens"

    PROMPT_TEMPLATE = f"""
    Ingredient Database: [
        ChickenBreast, 
        Lemon, 
        Broth
    ]

    Q: [('Chicken Breasts', '2 Large'), ('Lemons', '3')]
    A: [(ChickenBreast, 2), (Lemon, 3)]

    Q: [('Parsley', '4')]
    A: [(NewIngredient::Parsley, 4)]

    Q: [('{new_ingredient}', 5)]
    A: [(
    """
    out = llm(PROMPT_TEMPLATE)
    print(f"Prompt: {PROMPT_TEMPLATE}")
    print(f"Response: {out}")

if __name__=="__main__": 
    main()