from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from utils.gemini_chain import get_gemini_model

def evidence_chain():
    prompt = PromptTemplate.from_template(
        "Review the following content to identify valid evidence of event participation:\n\n{input_text}"
    )
    llm = get_gemini_model()
    return LLMChain(llm=llm, prompt=prompt)
