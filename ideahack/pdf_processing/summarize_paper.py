from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.output_parsers import JsonOutputParser


load_dotenv()
system_prompt = (
    "You are a research paper summarizer. Read given paper, "
    "write a short summary, and give at least 3 ideally 5 keywords "
    "that describe field of research from this paper. I need this "
    "keywords to be very spefic because all of the papers will be "
    "from the field of AI. "
    "Return answer in json format"
    "\n\n"
    "{context}"
)

parser = JsonOutputParser()
llm = ChatOpenAI(model="gpt-4o-mini")


def summarize_pdf(source: str = "https://arxiv.org/pdf/1706.03762") -> dict:
    loader = PyPDFLoader(source)

    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    vectorstore = InMemoryVectorStore.from_documents(
        documents=splits, embedding=OpenAIEmbeddings()
    )

    retriever = vectorstore.as_retriever()

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
        ]
    )

    question_answer_chain = create_stuff_documents_chain(llm, prompt, output_parser=parser)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)

    results = rag_chain.invoke({"input": ""})

    return results["answer"]


if __name__ == "__main__":
    out = summarize_pdf("")
    print(out)
