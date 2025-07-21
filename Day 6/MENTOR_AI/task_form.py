import streamlit as st
from datetime import datetime

TASKS = [
    "Leetcode", "Linkedin Article", "Linkedin Connect",
    "Business Card", "DT bootcamp", "Hackathon", "Gen AI Bootcamp"
]

class TaskForm:
    def __init__(self):
        self.task_type = ""
        self.title = ""
        self.description = ""
        self.deadline = None
        self.estimated_hours = 0
        self.resources_needed = ""
        self.expected_outcome = ""
        self.dependencies = ""
        
        # Task-specific fields
        self.leetcode_easy = 0
        self.leetcode_medium = 0
        self.leetcode_hard = 0
        self.article_link = ""
        self.linkedin_connect_pdf = None
        self.business_card_pdf = None
        self.bootcamp_location = ""
        self.bootcamp_date = None
        self.bootcamp_proof = None
        self.hackathon_type = ""
        self.hackathon_provider = ""
        self.hackathon_platform = ""
        self.hackathon_date = None
        self.hackathon_status = ""
        self.hackathon_proof = None
        
    def render(self):
        st.subheader("Task Submission Form")
        
        # Task Type Selection
        self.task_type = st.selectbox("Select Task Type", TASKS)
        
        # Common fields
        self.title = st.text_input("Task Title", 
                                 help="Enter a clear and concise title for your task")
        
        self.description = st.text_area("Task Description",
                                      help="Provide detailed information about what needs to be done")
        
        self.deadline = st.date_input("Deadline",
                                    help="When does this task need to be completed?")
        
        # Task-specific fields
        if self.task_type == "Leetcode":
            st.subheader("Leetcode Problem Details")
            self.leetcode_easy = st.number_input("Number of Easy Problems", min_value=0, max_value=100)
            self.leetcode_medium = st.number_input("Number of Medium Problems", min_value=0, max_value=100)
            self.leetcode_hard = st.number_input("Number of Hard Problems", min_value=0, max_value=100)
            
        elif self.task_type == "Linkedin Article":
            st.subheader("LinkedIn Article Details")
            self.article_link = st.text_input("Article Link", 
                                            help="Paste the URL of your LinkedIn article")
            
        elif self.task_type == "Linkedin Connect":
            st.subheader("LinkedIn Connection Details")
            self.linkedin_connect_pdf = st.file_uploader("Upload Connection Screenshot (PDF)", 
                                                       type=['pdf'],
                                                       help="Upload a PDF containing your LinkedIn connection screenshots")
            
        elif self.task_type == "Business Card":
            st.subheader("Business Card Details")
            self.business_card_pdf = st.file_uploader("Upload Business Card (PDF)", 
                                                    type=['pdf'],
                                                    help="Upload your business card as a PDF")
            
        elif self.task_type in ["DT bootcamp", "Gen AI Bootcamp"]:
            st.subheader(f"{self.task_type} Details")
            self.bootcamp_location = st.text_input("Location", 
                                                 help="Where is/was the bootcamp held?")
            self.bootcamp_date = st.date_input("Date", 
                                             help="When is/was the bootcamp?")
            self.bootcamp_proof = st.file_uploader("Upload Proof of Participation", 
                                                 type=['pdf', 'jpg', 'png'],
                                                 help="Upload certificate or proof of participation")
            
        elif self.task_type == "Hackathon":
            st.subheader("Hackathon Details")
            self.hackathon_type = st.selectbox("Type", ["Online", "Offline"])
            self.hackathon_provider = st.text_input("Provider/Organizer")
            self.hackathon_platform = st.text_input("Platform (if online)")
            self.hackathon_date = st.date_input("Date")
            self.hackathon_status = st.selectbox("Status", ["Registered", "Participated"])
            self.hackathon_proof = st.file_uploader("Upload Proof", 
                                                  type=['pdf', 'jpg', 'png'],
                                                  help="Upload certificate or proof of participation")
        
    def get_form_data(self):
        base_data = {
            "task_type": self.task_type,
            "title": self.title,
            "description": self.description,
            "deadline": str(self.deadline) if self.deadline else None,
            "submission_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Add task-specific data
        if self.task_type == "Leetcode":
            base_data.update({
                "leetcode_easy": self.leetcode_easy,
                "leetcode_medium": self.leetcode_medium,
                "leetcode_hard": self.leetcode_hard
            })
        elif self.task_type == "Linkedin Article":
            base_data.update({
                "article_link": self.article_link
            })
        elif self.task_type == "Linkedin Connect":
            base_data.update({
                "linkedin_connect_pdf": self.linkedin_connect_pdf
            })
        elif self.task_type == "Business Card":
            base_data.update({
                "business_card_pdf": self.business_card_pdf
            })
        elif self.task_type in ["DT bootcamp", "Gen AI Bootcamp"]:
            base_data.update({
                "bootcamp_location": self.bootcamp_location,
                "bootcamp_date": str(self.bootcamp_date) if self.bootcamp_date else None,
                "bootcamp_proof": self.bootcamp_proof
            })
        elif self.task_type == "Hackathon":
            base_data.update({
                "hackathon_type": self.hackathon_type,
                "hackathon_provider": self.hackathon_provider,
                "hackathon_platform": self.hackathon_platform,
                "hackathon_date": str(self.hackathon_date) if self.hackathon_date else None,
                "hackathon_status": self.hackathon_status,
                "hackathon_proof": self.hackathon_proof
            })
            
        return base_data 