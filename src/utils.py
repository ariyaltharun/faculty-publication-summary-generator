from typing import Any
import bibtexparser
import pandas as pd


# Utils to parse input
class InputParser:
    def __init__(self) -> None:
        pass
    
    def __call__(self, file: Any) -> pd.DataFrame:
        if file is None:
            return
        file_name = file.name
        data: pd.DataFrame
        if file_name.endswith(".bib"):
            data = self.parseBibtex(file)
        elif file_name.endswith(".xlsx"):
            data = self.excelParser(file)
        else:
            raise Exception("Invalid file format, please upload either excel or bibtex")
        return data

    def parseBibtex(self, file_name: str) -> pd.DataFrame:
        with open(file_name, 'r') as bib_str:
            library = bibtexparser.load(bib_str)
            return pd.DataFrame(library.entries) # .to_string()
        return

    def excelParser(self, file_name: str) -> pd.DataFrame:
        df = pd.ExcelFile(file_name)
        page1 = df.parse(0)
        return page1 # .to_string()


# System Prompt for llm
llm_sys_prompt =  """
You are a helpful summary generator. I will provide data in a pandas dataframe format, and your task is to generate a concise summary for each author using their attributes. The summary format should be as follows:
Just give the summary in right format don't tell anything extra
```markdown
<author-name>
Expertise: <author-expertise>
Interests: <author-interest>

Author publications:
* Title: <author-paper-title>
  Summary: <a-short-summary-of-the-paper-by-considering-the-attributes-provided>
```
"""

if __name__ == "__main__":
    parser = InputParser()
    data = parser("../data/sample_bibtex.bib")
    print(type(data))
    print(data)
