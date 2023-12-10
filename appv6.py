from dotenv import load_dotenv
import os
import fitz
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.embeddings.cohere import CohereEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import LLMChain, LLMMathChain, SequentialChain, TransformChain, ConversationalRetrievalChain, RetrievalQA
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.llms import HuggingFaceHub
from langchain.llms import Cohere
import re

load_dotenv(dotenv_path=".env")

#create a Title for the App
st.title("_Resume-Based Job Recommendation_ :blue[& Skill Gap Analysis] :newspaper:")
st.header("Upload Your Resume in PDF Format")
pdf = st.file_uploader("Upload your PDF", type="pdf")

# Function to extract skills, experience, and education from resume text
def extract_information(resume_text):
    # Define patterns for skills, experience, and education
    skills_pattern = re.compile(r'\b(?:skill(?:s)?|tool(?:s)?|language(?:s)?)\b.*?:(.*?)(?=\b\w+\b|$)', re.IGNORECASE | re.DOTALL)
    experience_pattern = re.compile(r'\b(?:experience)\b.*?:(.*?)(?=\b\w+\b|$)', re.IGNORECASE | re.DOTALL)
    education_pattern = re.compile(r'\b(?:education)\b.*?:(.*?)(?=\b\w+\b|$)', re.IGNORECASE | re.DOTALL)

    # Extract information using regular expressions
    skills_match = skills_pattern.search(resume_text)
    experience_match = experience_pattern.search(resume_text)
    education_match = education_pattern.search(resume_text)

    # Extracted information
    skills = skills_match.group(1).strip() if skills_match else None
    experience = experience_match.group(1).strip() if experience_match else None
    education = education_match.group(1).strip() if education_match else None

    return skills, experience, education

# Display PDF content in a text area
if pdf is not None:
    pdf_reader = PdfReader(pdf)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    st.text_area("PDF content is displayed below", value=text, height=300)

    # Extract skills, experience, and education
    skills, experience, education = extract_information(text)

    # Display the extracted information
    st.text(f"Skills: {skills}")
    st.text(f"Experience: {experience}")
    st.text(f"Education: {education}")


col1, col2 = st.columns(2)

with col1:
    query_option = st.text_area("Prompt", placeholder="Enter your questions here...", height=160)
    

with col2:
    on = st.toggle("Advance Settings")
    choose = "Cohere"  # Initialize choose outside the if block
    temperature=0.7
    if on:
        choose = st.radio(
            "Select Language Model👇",
            ["Cohere", "OpenAI", "HuggingFace"],
            key="visibility",
            horizontal=True,
        )
        temperature = st.slider("Degree of reasoning", min_value=0.0, max_value=1.0, value=0.7, step=0.1)


def choose_language_model(choose):
    if choose == "Cohere":
        llm = Cohere(temperature=temperature)
    elif choose == "OpenAI":
        llm = OpenAI(temperature=temperature)
    else:
        llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature": temperature})        
            
    return llm

def choose_embeddings(choose):
    if choose == "Cohere":
        return CohereEmbeddings()
    elif choose == "OpenAI":
        return OpenAIEmbeddings()
    else:
        return HuggingFaceEmbeddings()

# check if the uploaded file is not none


if pdf is None:
    st.button("Run", disabled=True) 

else:
    text_splitter = CharacterTextSplitter(
        separator = "\n",
        chunk_size = 1000,
        chunk_overlap = 200,
        length_function = len
    )
       
    # split the text into smaller chunks
    chunks = text_splitter.split_text(text)

    # select the embeddings we want to use
    embeddings = choose_embeddings(choose)

    # create  a knowledge base
    knowledge_base = FAISS.from_texts(chunks, embeddings)
   
    # search the knowledge base for document
    docs = knowledge_base.similarity_search(query_option)
    
    # initialize an a language model
    llm = choose_language_model(choose)

    # load a summarization chain
    chain = load_qa_chain(llm, chain_type="stuff")

    if st.button("Run", disabled=False):

        #run the chain with input document and user option
        response = chain.run(input_documents = docs, question=query_option)

        # display the response generated by the AI model
        st.success(response)