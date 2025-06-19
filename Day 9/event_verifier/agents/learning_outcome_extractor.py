from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from utils.gemini_chain import get_gemini_model

def learning_outcome_chain():
    prompt = PromptTemplate.from_template(
        "Extract technical terms, key learnings, and insights from these notes:\n\n{input_text}"
    )
    return LLMChain(llm=get_gemini_model(), prompt=prompt)
