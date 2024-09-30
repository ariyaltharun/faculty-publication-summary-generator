from collections import defaultdict
from typing import List, Tuple
from pprint import pprint
import os

import streamlit as st
import pandas as pd
from utils import InputParser
import utils
from llm import LLM
from googleScholar import GoogleScholar
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
        # Filter by year, if not you r dead
        year_range = st.slider(
            label="Select the year range to get papers between these year", 
            min_value=1999,
            max_value=2025,
            value=(2021, 2023),
            step=1
        )
        st.markdown("---")
        self.start_year = year_range[0]
        self.end_year = year_range[1]
        # Process data
        if file is not None:
            self.processData(file=file)

    def processData(self, file):
        # 2. Parse the uploaded file
        data = self.parser(file)
                
        # 3. Process the data
        # for tool in self.tools:
        #     tool(1)
        # for now use googleScholar
        # 3a. Search the data

        # for author, org_domain in data.values:
        with st.spinner(f"Fetching publications"):    
            scholar_details = self.scholarDetails(scholars=data.values)
        print("Done!!!!")

        # 3b. Now display the data
        st.write("Publications in tabular format")
        st.write(scholar_details)

        # 4. generate summary in form of words
        # st.write("Faculty data")
        summary_data: str = self.generateSummary(scholar_details)
        
        # 5. Give an option to download the data in desired format
        st.write("Summary of publications")
        st.markdown(summary_data)

        self.downloadData(scholar_details, summary_data)

    def customDataDisplay(
            self, 
            df: pd.DataFrame,
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
    
    def scholarDetails(self, scholars: List[List]):
        google_scholar = GoogleScholar()
        scholar_data = list()
        for scholar, org_domain in scholars:
            data = google_scholar(
                scholar_name=scholar, 
                org_domain=org_domain, 
                start_year=self.start_year, 
                end_year=self.end_year
            )
            scholar_data.append(
                pd.DataFrame(data)
            )
        return pd.concat(scholar_data, ignore_index=True)


if __name__ == "__main__":
    load_dotenv()
    app = App()
    app.run()

