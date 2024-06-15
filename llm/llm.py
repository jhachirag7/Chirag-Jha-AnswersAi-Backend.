from getpass import getpass
from dotenv import load_dotenv
import os
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI

load_dotenv()
key=os.environ.get('llm_key')
OPENAI_API_KEY = key
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

def get_answer(ques):
    template = """Question: {ques}

    Answer: Let's think step by step."""

    prompt = PromptTemplate.from_template(template)
    llm = OpenAI()
    llm_chain = prompt | llm

    ans=llm_chain.invoke(ques)
    print(ans)
    return ans