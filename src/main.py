import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic 
from langchain.prompts import ChatPromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA

load_dotenv()


class LangChainApp:
    def __init__(self):
        self.documents = self.load_documents()
        self.retriever = self.documents.as_retriever()
        self.llm = ChatAnthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY"),
            model="claude-3-5-sonnet-latest",
            temperature=0,
            max_tokens=1024,
            timeout=None,
            max_retries=2,
        )
        # Adjust the prompt to fit the desired output.
        self.prompt_template = ChatPromptTemplate.from_template(
            """
            You are an expert on tyranny, authoritariasm, and nonviolence.
            
            Given the following context and relevant news, explain the news in
            terms of authoritarian tactics and suggest specific nonviolent
            strategies to counteract the actions referenced in the news.

            Context: {context}

            News: {question}
            """
        )
        self.chain = self.prompt_template | self.llm

    def load_documents(self) -> FAISS:
        # Load preferred text sources (The Origins of Totalitarianism,
        # From Dictatorship to Democracy, etc). These documents are expected
        # to be in the root directory of the project.
        loader1 = PyPDFLoader("document1.pdf")
        loader2 = PyPDFLoader("document2.pdf")
        docs = loader1.load() + loader2.load()

        # Split documents into manageable chunks.
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        split_docs = text_splitter.split_documents(docs)

        # Create vector store with embeddings.
        embeddings = OpenAIEmbeddings()
        vectorstore = FAISS.from_documents(split_docs, embeddings)

        return vectorstore

    def generate_response(self, news) -> str:
        qa = RetrievalQA.from_chain_type(
          llm=self.llm,
          retriever=self.retriever,
          chain_type_kwargs={"prompt": self.prompt_template},
        )

        answer = qa.run(news)
        return answer


def main():
    app = LangChainApp()
    # Example news article. Replace this with the contents of given news
    # article. This will be treated as the "question" in the prompt template.
    news = "A theoretical group of government insiders have shut down USAID without proper authority."
    chain_response = app.generate_response(news)
    print(f"Response: {chain_response}")


if __name__ == "__main__":
    main()
