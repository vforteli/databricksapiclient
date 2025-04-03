
from pathlib import Path


def parse_params(params: dict) -> int:
    some_param = params.get("some_param")

    if some_param is None:
        print("some_param is None")
    else:
        print(f"some_param is {some_param}")

    return 42


def concat_path(*parts: str) -> str:
    trimmed_parts = [part.strip("/") for part in parts]
    return str.join('/', trimmed_parts)


def return_meaning_of_life() -> int:
    return 42
