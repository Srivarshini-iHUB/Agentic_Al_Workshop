import streamlit as st
from ..config.settings import TASKS

class TaskForm:
    def __init__(self):
        self.task_type = None
        self.title = None
        self.description = None
        self.deadline = None
        self.leetcode_easy = None
        self.leetcode_medium = None
        self.leetcode_hard = None
        self.article_link = None
        self.linkedin_connect_pdf = None
        self.business_card_pdf = None
        self.bootcamp_location = None
        self.bootcamp_date = None
        self.bootcamp_proof = None
        self.hackathon_type = None
        self.hackathon_provider = None
        self.hackathon_platform = None
        self.hackathon_date = None
        self.hackathon_status = None
        self.hackathon_proof = None

    def render(self):
        # Task Type Selection
        self.task_type = st.selectbox("Task Type", TASKS)
        
        # Common Fields
        self.title = st.text_input("Title")
        self.description = st.text_area("Description")
        self.deadline = st.date_input("Deadline")
        
        # Task-specific Fields
        if self.task_type == "Leetcode":
            col1, col2, col3 = st.columns(3)
            with col1:
                self.leetcode_easy = st.number_input("Easy Problems", min_value=0, value=0)
            with col2:
                self.leetcode_medium = st.number_input("Medium Problems", min_value=0, value=0)
            with col3:
                self.leetcode_hard = st.number_input("Hard Problems", min_value=0, value=0)
                
        elif self.task_type == "Linkedin Article":
            self.article_link = st.text_input("Article Link")
            
        elif self.task_type == "Linkedin Connect":
            self.linkedin_connect_pdf = st.file_uploader("Upload Connection Proof (PDF)", type=['pdf'])
            
        elif self.task_type == "Business Card":
            self.business_card_pdf = st.file_uploader("Upload Business Card (PDF)", type=['pdf'])
            
        elif self.task_type in ["DT bootcamp", "Gen AI Bootcamp"]:
            self.bootcamp_location = st.text_input("Location")
            self.bootcamp_date = st.date_input("Date")
            self.bootcamp_proof = st.file_uploader("Upload Proof (PDF)", type=['pdf'])
            
        elif self.task_type == "Hackathon":
            self.hackathon_type = st.selectbox("Type", ["Online", "Offline", "Hybrid"])
            self.hackathon_provider = st.text_input("Provider")
            self.hackathon_platform = st.text_input("Platform")
            self.hackathon_date = st.date_input("Date")
            self.hackathon_status = st.selectbox("Status", ["Completed", "In Progress", "Upcoming"])
            self.hackathon_proof = st.file_uploader("Upload Proof (PDF)", type=['pdf'])

    def get_form_data(self):
        return {
            'task_type': self.task_type,
            'title': self.title,
            'description': self.description,
            'deadline': str(self.deadline) if self.deadline else None,
            'leetcode_easy': self.leetcode_easy,
            'leetcode_medium': self.leetcode_medium,
            'leetcode_hard': self.leetcode_hard,
            'article_link': self.article_link,
            'linkedin_connect_pdf': self.linkedin_connect_pdf,
            'business_card_pdf': self.business_card_pdf,
            'bootcamp_location': self.bootcamp_location,
            'bootcamp_date': str(self.bootcamp_date) if self.bootcamp_date else None,
            'bootcamp_proof': self.bootcamp_proof,
            'hackathon_type': self.hackathon_type,
            'hackathon_provider': self.hackathon_provider,
            'hackathon_platform': self.hackathon_platform,
            'hackathon_date': str(self.hackathon_date) if self.hackathon_date else None,
            'hackathon_status': self.hackathon_status,
            'hackathon_proof': self.hackathon_proof
        } 