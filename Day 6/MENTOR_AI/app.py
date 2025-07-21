import streamlit as st
import json
import os
import google.generativeai as genai
from task_form import TaskForm
import PyPDF2
import requests
from bs4 import BeautifulSoup
import io
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import Literal
from src.analysis.task_analyzer import analyze_task_with_gemini
from src.utils.file_handler import save_result

# Set your Gemini API key
GOOGLE_API_KEY = "AIzaSyBHEVrruMH7quV5ChBk5cmnzTsN-KlBhvE"
genai.configure(api_key=GOOGLE_API_KEY)

TASKS = [
    "Leetcode", "Linkedin Article", "Linkedin Connect",
    "Business Card", "DT bootcamp", "Hackathon", "Gen AI Bootcamp"
]

# Define the output schema
class TaskAnalysis(BaseModel):
    priority: Literal["High", "Medium", "Low"] = Field(description="Priority level of the task")
    status: Literal["Accepted", "Rejected", "Send to Mentor"] = Field(description="Status of the task")
    reason: str = Field(description="Brief reason for the decision (max 20 words)")

def extract_text_from_pdf(pdf_file):
    try:
        if pdf_file is None:
            return "No PDF file provided"
            
        pdf_bytes = pdf_file.getvalue()
        pdf_stream = io.BytesIO(pdf_bytes)
        
        # Read the PDF
        pdf_reader = PyPDF2.PdfReader(pdf_stream)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        st.error(f"Error processing PDF: {str(e)}")
        return f"Error extracting text from PDF: {str(e)}"

def create_analysis_chain(task_type):
    # Initialize the LLM with API key
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0.3,
        google_api_key=GOOGLE_API_KEY
    )
    
    # Create the output parser
    parser = PydanticOutputParser(pydantic_object=TaskAnalysis)
    
    # Create the prompt template
    if task_type == "Linkedin Connect":
        template = """
        Analyze this LinkedIn connection proof and provide a brief assessment.
        {format_instructions}
        
        Consider:
        - Number and quality of connections
        - Professional network growth
        
        Content: {content}
        """
    elif task_type == "Business Card":
        template = """
        Analyze this business card and provide a brief assessment.
        {format_instructions}
        
        Consider:
        - Completeness of essential information (company, single contact number, email)
        - Professional information accuracy
        - No redundant contact information (e.g., Same phone numbers)
        
        Reject if:
        - Missing essential contact information
        - Contains redundant contact numbers(e.g., Same phone numbers)
        
        Content: {content}
        """
    elif task_type == "Linkedin Article":
        template = """
        Analyze this LinkedIn article and provide a brief assessment.
        {format_instructions}
        
        Consider:
        - Article quality and professionalism
        - Value to readers
        - Engagement potential
        
        Content: {content}
        """
    else:  # For bootcamp/hackathon certificates
        template = """
        Analyze this certificate/proof and provide a brief assessment.
        {format_instructions}
        
        Consider:
        - Certificate authenticity
        - Event significance
        - Achievement level
        
        Content: {content}
        """
    
    prompt = PromptTemplate(
        template=template,
        input_variables=["content"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    
    # Create the chain
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain, parser

def analyze_pdf_content(pdf_file, task_type):
    if pdf_file is None:
        return {
            "priority": "Low",
            "status": "Rejected",
            "reason": "No PDF file was uploaded"
        }
        
    text = extract_text_from_pdf(pdf_file)
    
    if text.startswith("Error") or text == "No PDF file provided":
        return {
            "priority": "Low",
            "status": "Rejected",
            "reason": text
        }
    
    try:
        chain, parser = create_analysis_chain(task_type)
        result = chain.run(content=text[:2000])
        return parser.parse(result).dict()
    except Exception as e:
        return {
            "priority": "Low",
            "status": "Rejected",
            "reason": f"Error analyzing PDF: {str(e)}"
        }

def analyze_leetcode_submission(form_data):
    total_problems = form_data['leetcode_easy'] + form_data['leetcode_medium'] + form_data['leetcode_hard']
    difficulty_score = (form_data['leetcode_easy'] * 1 + form_data['leetcode_medium'] * 2 + form_data['leetcode_hard'] * 3) / total_problems if total_problems > 0 else 0
    
    if total_problems == 0:
        return {"priority": "Low", "status": "Rejected", "reason": "No problems solved"}
    elif total_problems < 5:
        return {"priority": "Low", "status": "Rejected", "reason": "Too few problems solved"}
    elif difficulty_score < 1.5:
        return {"priority": "Medium", "status": "Rejected", "reason": "Problems are too easy"}
    elif difficulty_score < 2.0:
        return {"priority": "Medium", "status": "Accepted", "reason": f"Good mix of problems with difficulty score {difficulty_score:.2f}"}
    else:
        return {"priority": "High", "status": "Accepted", "reason": f"Excellent mix of problems with high difficulty score {difficulty_score:.2f}"}

def analyze_linkedin_article(article_link):
    try:
        response = requests.get(article_link)
        soup = BeautifulSoup(response.text, 'html.parser')
        article_text = soup.get_text()
        
        if not article_text:
            return {"priority": "Low", "status": "Rejected", "reason": "Article content could not be retrieved"}
        
        try:
            chain, parser = create_analysis_chain("Linkedin Article")
            result = chain.run(content=article_text[:1000])
            return parser.parse(result).dict()
        except Exception as e:
            return {"priority": "Low", "status": "Rejected", "reason": f"Error analyzing article: {str(e)}"}
    except Exception as e:
        return {"priority": "Low", "status": "Rejected", "reason": f"Error accessing article: {str(e)}"}

def analyze_task_with_gemini(form_data):
    task_type = form_data['task_type']
    
    # Task-specific analysis
    if task_type == "Leetcode":
        return analyze_leetcode_submission(form_data)
    elif task_type == "Linkedin Article":
        return analyze_linkedin_article(form_data['article_link'])
    elif task_type == "Linkedin Connect":
        return analyze_pdf_content(form_data.get('linkedin_connect_pdf'), task_type)
    elif task_type == "Business Card":
        return analyze_pdf_content(form_data.get('business_card_pdf'), task_type)
    elif task_type in ["DT bootcamp", "Gen AI Bootcamp"]:
        return analyze_pdf_content(form_data.get('bootcamp_proof'), task_type)
    elif task_type == "Hackathon":
        return analyze_pdf_content(form_data.get('hackathon_proof'), task_type)
    
    # For other tasks or if no PDF is provided, use the general analysis
    task_description = f"""
    Task Type: {form_data['task_type']}
    Title: {form_data['title']}
    Description: {form_data['description']}
    Deadline: {form_data['deadline']}
    """
    
    # Add task-specific details
    if task_type == "Linkedin Connect":
        task_description += f"\nConnection Proof: {'PDF uploaded' if form_data.get('linkedin_connect_pdf') else 'No PDF provided'}"
    elif task_type == "Business Card":
        task_description += f"\nBusiness Card: {'PDF uploaded' if form_data.get('business_card_pdf') else 'No PDF provided'}"
    elif task_type in ["DT bootcamp", "Gen AI Bootcamp"]:
        task_description += f"""
        Location: {form_data.get('bootcamp_location', 'Not specified')}
        Date: {form_data.get('bootcamp_date', 'Not specified')}
        Proof: {'File uploaded' if form_data.get('bootcamp_proof') else 'No proof provided'}
        """
    elif task_type == "Hackathon":
        task_description += f"""
        Type: {form_data.get('hackathon_type', 'Not specified')}
        Provider: {form_data.get('hackathon_provider', 'Not specified')}
        Platform: {form_data.get('hackathon_platform', 'Not specified')}
        Date: {form_data.get('hackathon_date', 'Not specified')}
        Status: {form_data.get('hackathon_status', 'Not specified')}
        Proof: {'File uploaded' if form_data.get('hackathon_proof') else 'No proof provided'}
        """
    
    try:
        chain, parser = create_analysis_chain("General")
        result = chain.run(content=task_description)
        analysis = parser.parse(result).dict()
        analysis.update(form_data)
        return analysis
    except Exception as e:
        return {"priority": "Low", "status": "Rejected", "reason": f"Error analyzing task: {str(e)}", "error": "Could not parse response"}

st.title("OKR Task Submission Classifier")

# Initialize and render the task form
task_form = TaskForm()
task_form.render()

if st.button("Submit Task"):
    # Get form data
    form_data = task_form.get_form_data()
    
    # Validate required fields
    if not form_data['title'] or not form_data['description']:
        st.error("Please fill in all required fields (Title and Description)")
    else:
        with st.spinner("Analyzing task..."):
            result = analyze_task_with_gemini(form_data)
            if "error" not in result:
                save_result(result)
                st.success(f"Task Analysis Complete")
                st.write(f"Priority: {result.get('priority', 'Not specified')}")
                st.write(f"Status: {result.get('status', 'Not specified')}")
                st.write(f"Reason: {result.get('reason', 'Not specified')}")
                
                # Display task details
                st.subheader("Task Details")
                for key, value in result.items():
                    if key not in ['priority', 'status', 'reason', 'error']:
                        st.write(f"{key.replace('_', ' ').title()}: {value}")
            else:
                st.error(result["error"])