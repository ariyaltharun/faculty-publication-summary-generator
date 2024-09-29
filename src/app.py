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
        self.llm = LLM(
            model_name="llama3-8b-8192", 
            api_key=os.getenv("GROQ_API_KEY"),
            sys_prompt=utils.llm_sys_prompt
        )
        self.tools = SearchAPIs.getTools()
        
    def run(self):
        # Streamlit interface
        st.title("Publication Summary Generator for Faculty Members")
        # 1. Upload file
        file = st.file_uploader(
            label="Please upload excel file",
            type="xlsx"
        )
        if file is not None:
            self.processData(file=file)

    def processData(self, file):
        data = self.parser(file)
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
        searchData.pub_year.dt.strftime("%Y")
        print("Done!!!!")
        # # 3b. generate summary in form of words
        # st.write("Faculty data")
        summary_data: str = self.generateSummary(searchData)

        # 4. Now display the data
        st.write("Publications in tabular format")
        st.write(searchData)

        # 5. Give an option to download the data in desired format
        st.write("Summary of publications")
        st.markdown(summary_data)

        self.downloadData(searchData, summary_data)

    def customDataDisplay(
            self, 
            df: utils.pd.DataFrame,
            start_year: int,
            end_year: int 
        ) -> utils.pd.DataFrame:
        customized_data = df[start_year <= df["pub_year"] <= end_year]
        return customized_data
    
    @st.fragment
    def downloadData(self, searchData, summary_data):
        _, col1, col2 = st.columns(spec=[0.6, 0.2, 0.2])
        col1.download_button(
            label=f"📥 Excel file",
            data=searchData.to_string(),
            file_name="your_gf.xlsx"
        )
        col2.download_button(
            label="📥 Docx file",
            data=summary_data,
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
