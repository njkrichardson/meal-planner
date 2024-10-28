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
        if not self._model_binary_present() and not self.config.lazy: 
            self._download()

        with utils.SuppressionContext(): 
            super().__init__(
                model_path=str(self.GGUF_BIN), 
                n_ctx=self.config.context_size, 
            )

    def _model_binary_present(self) -> bool: 
        """Checks whether the desired model binary is present 
        and has the right size. 
        """
        if not self.GGUF_BIN.exists(): 
            return False

        response = requests.get(self.GGUF_URI, stream=True, timeout=5)
        total_num_bytes: int = int(response.headers.get("content-length", 0))
        model_binary_size: int = self.GGUF_BIN.stat().st_size 
        return total_num_bytes == model_binary_size


    def _download(self) -> None: 
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
        with utils.SuppressionContext(): 
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