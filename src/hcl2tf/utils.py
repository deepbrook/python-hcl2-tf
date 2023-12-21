from collections.abc import MutableMapping
from typing import Any, Iterator


BLOCK_TYPES = (
    "resource",
    "data",
    "variable",
    "locals",
    "output",
    "module",
    "provider",
    "terraform",
    "import",
    "moved",
    "check",
)


class AddressableDict(MutableMapping):
    def __init__(self, config: dict) -> None:
        self.config = config

    def _parse_address(self, addr: str):
        if "." not in addr:
            raise ValueError("Not a valid address!")
        path = addr.split(".")
        if path[0] == "local":
            path = ["locals", *path[1:]]
        elif path[0] == "var":
            path = ["variable", *path[1:]]
        elif path[0] not in BLOCK_TYPES:
            path = ["resource", *path]
        return path

    def __len__(self) -> int:
        return self.config.__len__()

    def __iter__(self) -> Iterator:
        return self.config.__iter__()

    def __setitem__(self, __key: Any, __value: Any) -> None:
        return self.config.__setitem__(__key, __value)

    def __getitem__(self, __key: Any,):
        try:
            return self.config.__getitem__(__key)
        except KeyError as e:
            try:
                addr = self._parse_address(__key)
            except ValueError:
                raise e
            return self._fetch(addr)
            
    def __delitem__(self, __key: Any) -> None:
        return self.config.__delitem__(__key)

    def _fetch(self, addr: list, config=None):
        if config is None:
            config = self.config
        
        if None in addr:
            raise ValueError("address {addr} contains invalid None sub-key!")

        if not addr:
            return config  # Arrived at destination
        
        next, *remaining = addr

        try:
            next_config = config[next]
        except TypeError as e:
            raise KeyError(next) from e
    
        try:
            return self._fetch(remaining, config[next])
        except KeyError as e:
            raise KeyError(addr) from e

