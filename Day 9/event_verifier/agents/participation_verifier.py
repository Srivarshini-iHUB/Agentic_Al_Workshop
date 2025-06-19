from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from utils.gemini_chain import get_gemini_model

def verifier_chain():
    prompt = PromptTemplate.from_template(
        "Based on this evidence, confirm if the student actually participated in the event:\n\n{input_text}"
    )
    return LLMChain(llm=get_gemini_model(), prompt=prompt)
