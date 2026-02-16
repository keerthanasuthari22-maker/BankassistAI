"""
RAG (Retrieval Augmented Generation) System for Banking AI Agent
Handles document loading, embedding, and retrieval using Simple TF-IDF embeddings + FAISS.
"""

import json
import pickle
from pathlib import Path
from typing import List, Dict, Optional
import logging
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

logger = logging.getLogger(__name__)


# -------------------------
# SIMPLE EMBEDDINGS CLASS
# -------------------------
class SimpleEmbeddings(Embeddings):
    """
    Simple embeddings class using TF-IDF for banking documents.
    No API calls needed - completely free and fast.
    """

    def __init__(self, model_path: Optional[Path] = None):
        self.vectorizer = TfidfVectorizer(max_features=384, stop_words='english')
        self.is_fitted = False
        self.model_path = model_path
        
        # Load existing model if available
        if self.model_path and self.model_path.exists():
            self.load_model()

    def fit(self, texts: List[str]):
        """Fit the vectorizer on texts"""
        self.vectorizer.fit(texts)
        self.is_fitted = True
        if self.model_path:
            self.save_model()

    def save_model(self):
        """Save vectorizer to disk"""
        if self.model_path:
            try:
                with open(self.model_path, 'wb') as f:
                    pickle.dump(self.vectorizer, f)
                logger.info(f"✅ Saved TF-IDF model to {self.model_path}")
            except Exception as e:
                logger.error(f"❌ Failed to save TF-IDF model: {e}")

    def load_model(self):
        """Load vectorizer from disk"""
        if self.model_path and self.model_path.exists():
            try:
                with open(self.model_path, 'rb') as f:
                    self.vectorizer = pickle.load(f)
                self.is_fitted = True
                logger.info(f"✅ Loaded TF-IDF model from {self.model_path}")
            except Exception as e:
                logger.error(f"❌ Failed to load TF-IDF model: {e}")

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of documents"""
        if not self.is_fitted:
            # Fit vectorizer on all texts if not loaded
            self.fit(texts)
        
        vectors = self.vectorizer.transform(texts)
        
        # Convert sparse matrix to dense and return as list
        embeddings = vectors.toarray().tolist()
        return embeddings

    def embed_query(self, text: str) -> List[float]:
        """Embed a single query"""
        if not self.is_fitted:
            logger.warning("⚠ TF-IDF not fitted! Query embedding will be poor. Rebuild vectorstore.")
            # Fallback: simple fit on query (leads to poor results but prevents crash)
            self.vectorizer.fit([text])
            self.is_fitted = True
        
        vector = self.vectorizer.transform([text]).toarray()[0]
        return vector.tolist()


# -------------------------
# BANKING RAG SYSTEM
# -------------------------
class BankingRAG:
    """
    Banking RAG system:
    - Loads FAQ + Branch data
    - Creates FAISS vectorstore
    - Retrieves relevant context for user query
    """

    def __init__(self, config):
        self.config = config
        
        # Define model path
        self.tfidf_path = config.VECTORSTORE_DIR / "tfidf_model.pkl"
        self.embeddings = SimpleEmbeddings(model_path=self.tfidf_path)
        
        self.vectorstore = None

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP,
            separators=["\n## ", "\n### ", "\n", " ", ""]
        )

    # -------------------------
    # LOAD DOCUMENTS
    # -------------------------
    def load_documents(self) -> List[Document]:
        documents = []

        # Load FAQ file
        faq_path = self.config.DATA_DIR / "banking_docs.txt"
        if faq_path.exists():
            content = faq_path.read_text(encoding="utf-8").strip()

            if content:
                chunks = self.text_splitter.split_text(content)

                for i, chunk in enumerate(chunks):
                    documents.append(
                        Document(
                            page_content=chunk,
                            metadata={
                                "doc_id": f"faq_{i}",
                                "source": "banking_docs",
                                "chunk": i
                            }
                        )
                    )

                logger.info(f"✅ Loaded {len(chunks)} FAQ chunks from banking_docs.txt")

        # If no FAQ file, use default FAQ
        if not documents:
            logger.warning("⚠ No banking_docs.txt found or file empty. Loading default FAQ...")

            default_faq = """
# BANKING CUSTOMER SERVICE DOCUMENTATION

## Account Management
### How do I open a new account?
To open a new account, visit your nearest branch with valid ID proof, PAN card, and address proof.
You can also apply online. The process takes 2-3 business days.

### What are the minimum balance requirements?
- Savings Account: Rs. 5,000
- Current Account: Rs. 50,000
- Salary Account: No minimum balance required

### What is the daily transaction limit?
- ATM Withdrawals: Rs. 50,000 per day
- NEFT/RTGS Transfer: Rs. 10,00,000 per transaction
- Mobile Banking: Rs. 2,00,000 per day

### How long do transfers take?
- NEFT: 1-2 hours (during banking hours)
- RTGS: 30 minutes
- IMPS: Instant (24/7 available)

## Loan Services
### What loan options are available?
1. Personal Loan: Up to Rs. 50 lakhs, 9% - 12% interest rate
2. Home Loan: Up to Rs. 1 crore, 8.5% - 9.5% interest rate
3. Business Loan: Up to Rs. 10 lakhs, 12% - 15% interest rate
4. Auto Loan: Up to Rs. 50 lakhs, 8% - 10% interest rate

### How do I apply for a loan?
Submit your application online or visit the nearest branch with salary slips, income tax returns,
bank statements, and identity proof. Approval typically takes 3-5 business days.

## Branch & ATM Services
### What are branch timings?
Standard timings: 9:00 AM - 5:00 PM (Monday - Friday),
9:00 AM - 2:00 PM (Saturday), Closed on Sundays and national holidays.
"""

            chunks = self.text_splitter.split_text(default_faq)

            for i, chunk in enumerate(chunks):
                documents.append(
                    Document(
                        page_content=chunk,
                        metadata={
                            "doc_id": f"default_faq_{i}",
                            "source": "default_faq",
                            "chunk": i
                        }
                    )
                )

            logger.info(f"✅ Loaded {len(chunks)} default FAQ chunks")

        # Load Branch Data
        branch_path = self.config.DATA_DIR / "branch_data.json"

        if branch_path.exists():
            try:
                branch_data = json.loads(branch_path.read_text(encoding="utf-8"))
            except Exception:
                branch_data = []
        else:
            branch_data = []

        # If branch_data is dict format, normalize
        if isinstance(branch_data, dict) and "branches" in branch_data:
            branch_data = branch_data["branches"]

        # If no branches, add default ones
        if not branch_data:
            logger.warning("⚠ No branch_data.json found or empty. Loading default branches...")

            branch_data = [
                {
                    "id": "BR001",
                    "name": "Downtown Branch",
                    "city": "Mumbai",
                    "address": "123 Financial Plaza, Mumbai - 400001",
                    "phone": "022-1234-5678",
                    "email": "downtown@bankassist.com",
                    "timings": "9:00 AM - 5:00 PM",
                    "services": ["Account Opening", "Loan Application", "Safe Deposit Lockers"],
                    "atm_available": True
                },
                {
                    "id": "BR002",
                    "name": "Airport Branch",
                    "city": "Mumbai",
                    "address": "Terminal 2, Mumbai Airport",
                    "phone": "022-9876-5432",
                    "email": "airport@bankassist.com",
                    "timings": "24/7",
                    "services": ["International Transfers", "Forex", "Travel Cards"],
                    "atm_available": True
                },
                {
                    "id": "BR003",
                    "name": "IT Hub Branch",
                    "city": "Bangalore",
                    "address": "Tech Park, Whitefield, Bangalore - 560066",
                    "phone": "080-4456-7890",
                    "email": "ithub@bankassist.com",
                    "timings": "9:00 AM - 6:00 PM",
                    "services": ["Account Opening", "Credit Cards", "Digital Services"],
                    "atm_available": True
                },
                {
                    "id": "BR004",
                    "name": "Central Branch",
                    "city": "Delhi",
                    "address": "456 Business Central, New Delhi - 110001",
                    "phone": "011-2345-6789",
                    "email": "central@bankassist.com",
                    "timings": "9:00 AM - 5:00 PM",
                    "services": ["Bulk Services", "Corporate Accounts", "Investment"],
                    "atm_available": True
                }
            ]

        for branch in branch_data:
            branch_text = f"""
Branch Name: {branch.get('name')}
Branch ID: {branch.get('id')}
City: {branch.get('city')}
Address: {branch.get('address')}
Phone: {branch.get('phone')}
Email: {branch.get('email')}
Timings: {branch.get('timings')}
Services: {', '.join(branch.get('services', []))}
ATM Available: {branch.get('atm_available')}
""".strip()

            documents.append(
                Document(
                    page_content=branch_text,
                    metadata={
                        "doc_id": f"branch_{branch.get('id')}",
                        "source": "branch_info",
                        "city": branch.get("city"),
                        "branch_id": branch.get("id")
                    }
                )
            )

        logger.info(f"✅ Loaded {len(branch_data)} branch documents")

        return documents

    # -------------------------
    # INITIALIZE VECTORSTORE
    # -------------------------
    def initialize_vectorstore(self) -> FAISS:
        vectorstore_path = self.config.VECTORSTORE_DIR / "banking_vectorstore"

        # Check if both vectorstore AND tfidf model exist
        if vectorstore_path.exists() and self.embeddings.is_fitted:
            logger.info("📌 Loading existing FAISS vectorstore...")
            try:
                self.vectorstore = FAISS.load_local(
                    str(vectorstore_path),
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
                logger.info("✅ Vectorstore loaded successfully.")
                return self.vectorstore
            except Exception as e:
                logger.error(f"❌ Failed to load vectorstore: {e}. Rebuilding...")
        
        logger.info("📌 Creating new vectorstore from documents...")
        documents = self.load_documents()

        if not documents:
            raise ValueError("No documents available for vectorstore creation")

        # FIX: Explicit IDs required (LangChain new versions)
        ids = [str(i) for i in range(len(documents))]

        # Initial fit is handled inside embed_documents
        self.vectorstore = FAISS.from_documents(
            documents=documents,
            embedding=self.embeddings,
            ids=ids
        )

        vectorstore_path.mkdir(parents=True, exist_ok=True)
        self.vectorstore.save_local(str(vectorstore_path))
        
        # Ensure embeddings are saved (redundant check)
        self.embeddings.save_model()

        logger.info(f"✅ Vectorstore created and saved at: {vectorstore_path}")
        return self.vectorstore

    # -------------------------
    # RETRIEVE DOCUMENTS
    # -------------------------
    def retrieve(self, query: str, k: int = None) -> List[Dict]:
        if self.vectorstore is None:
            self.initialize_vectorstore()

        k = k or self.config.TOP_K_RETRIEVAL

        try:
            docs = self.vectorstore.similarity_search_with_score(query, k=k)

            results = []
            for doc, score in docs:
                results.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "score": float(score)
                })

            return results

        except Exception as e:
            logger.error(f"❌ Error retrieving documents: {e}")
            return []

    # -------------------------
    # CONTEXT FORMATTER
    # -------------------------
    def get_context(self, query: str) -> str:
        results = self.retrieve(query)

        if not results:
            return "No relevant documents found."

        context = "## Relevant Banking Information:\n\n"

        for i, result in enumerate(results, 1):
            context += f"Document {i} (Score: {result['score']:.4f}):\n"
            context += f"{result['content']}\n\n"

        return context


# -------------------------
# FACTORY INITIALIZER
# -------------------------
def initialize_rag(config) -> BankingRAG:
    rag = BankingRAG(config)
    rag.initialize_vectorstore()
    return rag