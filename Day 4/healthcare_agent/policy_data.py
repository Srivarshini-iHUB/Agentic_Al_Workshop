# policy_data.py

policies = [
    {
        "name": "Basic Health Plan",
        "age_min": 18,
        "age_max": 55,
        "type": "individual",
        "dependents": 0,
        "special": [],
        "premium": 150,
        "description": "Affordable coverage for basic in-patient and emergency needs."
    },
    {
        "name": "Family Health Plus Plan",
        "age_min": 18,
        "age_max": 55,
        "type": "family",
        "dependents": 1,
        "special": [],
        "premium": 350,
        "description": "In-patient and outpatient coverage for families, including emergency transport."
    },
    {
        "name": "Comprehensive Health & Wellness Plan",
        "age_min": 0,
        "age_max": 100,
        "type": "both",
        "dependents": 0,
        "special": ["mental health", "wellness"],
        "premium": 500,
        "description": "Includes wellness, mental health, and specialist services."
    },
    {
        "name": "Senior Health Security Plan",
        "age_min": 55,
        "age_max": 100,
        "type": "individual",
        "dependents": 0,
        "special": ["senior", "dental", "vision"],
        "premium": 600,
        "description": "Specialized for seniors including vision, dental, and mobility services."
    }
]
