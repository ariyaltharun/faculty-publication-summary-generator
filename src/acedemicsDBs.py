from typing import List, Callable
from scholarly import scholarly


class SearchAPIs:
    def __init__(self) -> None:
        self.tools = [lambda x: print(f"Helo world, {x}")]
        pass

    @staticmethod
    def getTools() -> List[Callable[[str, str], str]]:
        return SearchAPIs().tools

    def addTool(self, func) -> bool:
        self.tools.append(func)
