plan_details = {
    "Basic Health Plan": """
**Basic Health Plan**
- Ideal for individuals aged 18–55 seeking emergency and basic in-patient coverage.
- $150/month | $1,500 deductible | $100,000 annual limit
- Covers emergency hospitalization, diagnostics, and prescriptions during in-patient care.
- Excludes outpatient, maternity, and dental.
""",

    "Family Health Plus Plan": """
**Family Health Plus Plan**
- Designed for families with children up to age 25.
- $350/month | $1,000 individual / $3,000 family deductible | $500,000 annual limit
- Covers in-patient, outpatient, specialist consultations, ambulance, diagnostics, and family doctor visits.
""",

    "Comprehensive Health & Wellness Plan": """
**Comprehensive Health & Wellness Plan**
- Best for health-conscious individuals/families with holistic needs.
- $500/month | $750 individual / $2,000 family deductible | $1,000,000 annual limit
- Includes all Family Health Plus benefits, plus mental health, wellness programs, preventive screenings.
""",

    "Senior Health Security Plan": """
**Senior Health Security Plan**
- Tailored for individuals aged 55+, focusing on extended care and specialized support.
- $600/month | $1,000 deductible | $750,000 annual limit
- Covers hospitalization, prescriptions, dental, vision, and senior wellness.
""",

    "Dental & Vision Add-On": """
**Dental & Vision Add-On**
- $50/month per member
- Dental exams & basic procedures, vision tests, $200 lens allowance, and laser surgery discounts.
""",

    "Maternity & Newborn Care Add-On": """
**Maternity & Newborn Care Add-On**
- $75/month
- Covers prenatal/postnatal care, delivery, newborn immunizations (after 9-month waiting period).
""",

    "International Travel Medical Insurance": """
**International Travel Medical Insurance**
- $40/month
- Covers emergency hospitalization and evacuation abroad (up to $100,000), global helpline access.
"""
}

def get_recommendation(age, family_type, dependents, maternity, dental_vision, travel, mental_health):
    base_plan = ""
    addons = []

    if age >= 55:
        base_plan = "Senior Health Security Plan"
    elif family_type == "Family":
        base_plan = "Comprehensive Health & Wellness Plan" if mental_health or maternity else "Family Health Plus Plan"
    elif mental_health:
        base_plan = "Comprehensive Health & Wellness Plan"
    else:
        base_plan = "Basic Health Plan"

    if maternity and base_plan in ["Family Health Plus Plan", "Comprehensive Health & Wellness Plan"]:
        addons.append("Maternity & Newborn Care Add-On")
    if dental_vision:
        addons.append("Dental & Vision Add-On")
    if travel:
        addons.append("International Travel Medical Insurance")

    return [plan_details[base_plan]] + [plan_details[addon] for addon in addons]
