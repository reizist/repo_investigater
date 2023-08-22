import os
import sys

from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.indexes import VectorstoreIndexCreator

from langchain.document_loaders import GitLoader

from dotenv import load_dotenv
load_dotenv()

# repo = "cube-js/cube"
repo = sys.argv[1] # "reizist/repo_investigater"
repo_path = f"./repos/{repo}"
filter_ext = ".py"
clone_url = f"https://github.com/{repo}"
branch = "main"

if os.path.exists(repo_path):
    clone_url = None

loader = GitLoader(
    clone_url=clone_url,
    branch=branch,
    repo_path=repo_path,
    file_filter=lambda file_path: file_path.endswith(filter_ext),
)

print(f"{repo} について回答します。")

llm = ChatOpenAI(model='gpt-4')


index = VectorstoreIndexCreator(
    vectorstore_cls=Chroma, # Default
    embedding=OpenAIEmbeddings(disallowed_special=(), model='text-embedding-ada-002'), # Default
).from_loaders([loader])

while True:
    print('>>')
    query = input()
    answer = index.query(llm=llm, question=query)
    print(answer)
