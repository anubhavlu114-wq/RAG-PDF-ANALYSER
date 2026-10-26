import os
import sys
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.messages import HumanMessage, AIMessage

# Windows terminal encoding fix
sys.stdout.reconfigure(encoding='utf-8')

# .env file se environment variables load karna
load_dotenv()

# ==========================================
# 0. SETTINGS
# ==========================================
CHROMA_PATH = './chroma_db'  # Local Chroma vector database folder

# ==========================================
# 1. HELPER FUNCTIONS
# ==========================================

def load_document(file):
    if not os.path.isfile(file):
        print(f'File not found: {file}')
        return None

    name, extension = os.path.splitext(file)
    if extension.lower() == '.pdf':
        from langchain_community.document_loaders import PyPDFLoader
        print(f'Loading {file}...')
        loader = PyPDFLoader(file)
    elif extension.lower() == '.docx':
        from langchain_community.document_loaders import Docx2txtLoader
        print(f'Loading {file}...')
        loader = Docx2txtLoader(file)
    else:
        print('Document format is not supported!')
        return None
    return loader.load()


def chunk_data(data, chunk_size=256, chunk_overlap=50):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return text_splitter.split_documents(data)


def get_embeddings():
    print("⏳ Local HuggingFace Embeddings load ho rahi hain...")
    return HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')


def get_chroma_vector_store(chunks):
    embeddings = get_embeddings()
    
    # Agar chroma_db folder pehle se hai toh load karega, nahi toh naya banayega
    if os.path.exists(CHROMA_PATH):
        print(f"📁 Purana Chroma DB '{CHROMA_PATH}' mil gaya, load kiya ja raha hai...")
        vector_store = Chroma(
            persist_directory=CHROMA_PATH, 
            embedding_function=embeddings
        )
    else:
        print(f"📁 Naya Chroma DB '{CHROMA_PATH}' banaya ja raha hai...")
        vector_store = Chroma.from_documents(
            documents=chunks, 
            embedding=embeddings, 
            persist_directory=CHROMA_PATH
        )
    return vector_store


def ask_question(q, vector_store, llm, chat_history):
    print("⏳ AI aapke sawal ka jawab dhoondh raha hai, thoda wait karein...")
    try:
        # 1. Agar chat history hai, toh purane context ko dhyan mein rakhte hue sawal ko standalone banana
        if chat_history:
            rephrase_prompt = ChatPromptTemplate.from_messages([
                ("system", "Given a chat history and the latest user question which might reference context in the chat history, formulate a standalone question which can be understood without the chat history. Do NOT answer the question, just reformulate it if needed and otherwise return it as is."),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ])
            rephrase_chain = rephrase_prompt | llm | StrOutputParser()
            query_to_search = rephrase_chain.invoke({"input": q, "chat_history": chat_history})
        else:
            query_to_search = q

        # 2. Vector DB se relevant chunks retrieve karna
        retriever = vector_store.as_retriever(search_type='similarity', search_kwargs={'k': 5})
        docs = retriever.invoke(query_to_search)
        context_text = "\n\n".join(doc.page_content for doc in docs)

        # 3. LLM ko context aur history ke sath final prompt bhejna
        qa_prompt = ChatPromptTemplate.from_messages([
            ("system", "Use the following pieces of retrieved context to answer the question. If you don't know the answer, say that you don't know.\n\nContext: {context}"),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ])
        
        qa_chain = qa_prompt | llm | StrOutputParser()
        answer = qa_chain.invoke({
            "context": context_text,
            "chat_history": chat_history,
            "input": q
        })
        
        return answer
    except Exception as e:
        return f"⚠️ Error aaya: {e}"


# ==========================================
# 2. MAIN EXECUTION PIPELINE
# ==========================================

if __name__ == "__main__":
    pdf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'constitution.pdf')
    data = load_document(pdf_path)

    if data:
        print(f'Aapke data mein {len(data)} pages hain.')

        chunks = chunk_data(data, chunk_size=256)
        print(f'Total chunks ban gaye: {len(chunks)}')

        # Vector store initialize karna
        vector_store = get_chroma_vector_store(chunks)

        # Yantra AI LLM setup
        llm = ChatOpenAI(
            model='gpt-4o-mini',
            temperature=0,
            api_key=os.getenv("YANTRA_API_KEY"),
            base_url=os.getenv("YANTRA_BASE_URL"),
            max_retries=0,
            timeout=20
        )

        # Chat history list
        chat_history = []

        print("\n✅ Setup poora ho gaya hai! Ab aap apne sawal pooch sakte hain. (Band karne ke liye 'exit' likhein)")
        
        while True:
            q = input("\nAapka Sawal: ")
            
            if q.lower() in ['exit', 'quit']:
                print("Chat band ki ja rahi hai...")
                break
            
            # Sawal, vector store, llm aur history pass karke jawab lena
            answer = ask_question(q, vector_store, llm, chat_history)
            print("\n🤖 Jawab:\n", answer)
            
            # Chat history update karna taaki memory bani rahe
            chat_history.append(HumanMessage(content=q))
            chat_history.append(AIMessage(content=answer))

    else:
        print("Failed to load document.")