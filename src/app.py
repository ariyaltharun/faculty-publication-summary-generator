from collections import defaultdict
from typing import List, Tuple
from pprint import pprint
import os

import streamlit as st
from utils import InputParser
import utils
from llm import LLM
from googleScholar import googleScholar
from acedemicsDBs import SearchAPIs
from dotenv import load_dotenv


class App:
    def __init__(self) -> None:
        self.parser = InputParser()
        self.llm = LLM("llama3-8b-8192", os.getenv("GROQ_API_KEY"))
        self.tools = SearchAPIs.getTools()
        
    def run(self):
        # Streamlit interface
        st.title("Publication Summary Generator for Faculty Members")

        # # 1. Upload file
        excel_file = st.file_uploader(
            label="Please upload excel file",
            type="xlsx"
        )
        if excel_file is not None:
            data = self.parser(excel_file)
            st.write(data)

        # # 2. Parse the uploaded file
        # author_details = []
        # for row in data:
        #     author_details.append(
        #         (row['name'], row['org'])
        #     )
        
        # 3. Process the data
        # for tool in self.tools:
        #     tool(1)
        # for now use googleScholar
        # 3a. Search the data
        with st.spinner("Processing"):
            searchData = self.searchPubs([["Meera Devi", "@msrit.edu"], ["Sowmya B J", "@msrit.edu"]])
        print("Done!!!!")
        # 3b. generate summary in form of words
        st.write("Faculty data")
        summary_data = self.generateSummary(searchData)

        # print(searchData)
        # print(searchData.to_string())
        # # 4. Now display the data
        st.write(searchData)

        # 5. Give an option to download the data in desired format
        self.download_excel_file(searchData)
        self.download_doc_file(summary_data)
        # st.download_button(
        #     label="Download Excel file",
        #     data=searchData.to_string(),
        #     file_name="your_gf.xlsx"
        # )
        # st.download_button(
        #     label="Download Summary in Doc fmt",
        #     data=summary_data,
        #     file_name="summary_data.doc"
        # )
        pass

    @st.fragment
    def download_excel_file(self, data):
        st.download_button(
            label="Download Excel file",
            data=data.to_string(),
            file_name="your_gf.xlsx"
        )

    @st.fragment
    def download_doc_file(self, data):
        st.download_button(
            label="Download Doc file",
            data=data,
            file_name="summary.doc"
        )
    
    def generateSummary(self, data) -> str:
        data = data.to_string()
        # call llm and generate summary for each author
        summy_data = self.llm(data)
        return summy_data

    def searchPubs(self, authors: List[Tuple[str, str]]):
        df = defaultdict(list)
        for author, email_domain in authors:
            # Search in googlescholar
            pubs = googleScholar(author_name=author, uuid=email_domain)
            # pprint(pubs[:3])
            for pub in pubs[:3]:
                df["author_name"].append(author)
                df["paper_title"].append(pub.get("title", None))
                df["abstract"].append(pub.get("abstract", None))
                df["authors"].append(pub.get("author", None))
                df["pub_year"].append(pub.get("pub_year", None))
                df["Journal"].append(pub.get("journal", None))
        # pprint(df)
        return utils.pd.DataFrame(df)


if __name__ == "__main__":
    load_dotenv()
    app = App()
    app.tools.append(googleScholar)
    app.run()
