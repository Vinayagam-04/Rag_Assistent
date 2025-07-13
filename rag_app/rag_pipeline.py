import nltk
import logging
import os
from sentence_transformers import SentenceTransformer
import chromadb
import google.generativeai as genai
from decouple import config

# Configure logging
logger = logging.getLogger(__name__)

# Download NLTK data
try:
    nltk.download('punkt', quiet=True)
except Exception as e:
    logger.warning(f"Could not download NLTK data: {e}")

class RAGPipeline:
    def __init__(self):
        try:
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            logger.debug("SentenceTransformer initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize SentenceTransformer: {str(e)}")
            raise

        # Use absolute path for ChromaDB
        chroma_path = os.path.join(os.getcwd(), "chroma_db")
        try:
            from chromadb.config import Settings
        except ImportError:
            logger.error("Could not import Settings from chromadb.config. Please ensure you have the correct version of chromadb installed.")
            raise

        self.client = chromadb.PersistentClient(
            path=chroma_path,
            settings=Settings(allow_reset=True, anonymized_telemetry=False)
        )
        logger.debug("ChromaDB client initialized")
        
        try:
            self.collection = self.client.get_or_create_collection(name="legal_docs")
            logger.debug("Collection legal_docs ready")
        except Exception as e:
            logger.error(f"Failed to initialize collection: {str(e)}")
            raise

        # Initialize Gemini API
        try:
            gemini_api_key = config('GEMINI_API_KEY', default=None)
            if not gemini_api_key or gemini_api_key == 'your-gemini-api-key-here':
                logger.warning("GEMINI_API_KEY not set or using default value. Please set a valid API key.")
                self.gemini = None
            else:
                genai.configure(api_key=str(gemini_api_key))
                self.gemini = genai.GenerativeModel('gemini-1.5-flash')
                logger.debug("Gemini API configured")
        except Exception as e:
            logger.error(f"Failed to configure Gemini API: {str(e)}")
            self.gemini = None

    def store_document(self, text, doc_id):
        try:
            sentences = nltk.sent_tokenize(text)
            if not sentences:
                logger.warning(f"No sentences found in document {doc_id}")
                return
            embeddings = self.model.encode(sentences)
            self.collection.add(
                embeddings=embeddings.tolist(),
                documents=sentences,
                ids=[f"{doc_id}_{i}" for i in range(len(sentences))]
            )
            logger.debug(f"Stored document {doc_id} with {len(sentences)} sentences")
        except Exception as e:
            logger.error(f"Error storing document {doc_id}: {str(e)}")
            raise

    def query(self, query_text):
        try:
            if not self.gemini:
                return "Sorry, the AI service is not properly configured. Please check your API key settings."
            
            query_embedding = self.model.encode([query_text])[0]
            results = self.collection.query(
                query_embeddings=[query_embedding.tolist()],
                n_results=5
            )
            
            if not results['documents'] or not results['documents'][0]:
                logger.warning(f"No documents found for query: {query_text}")
                # If no documents found, still try to answer the question
                prompt = f"Answer the following legal question based on general legal knowledge: {query_text}\n\nPlease provide a helpful response:"
            else:
                context = "\n".join(results['documents'][0])
                prompt = f"Based on the following context, answer the query: {query_text}\n\nContext: {context}\n\nAnswer:"
            
            response = self.gemini.generate_content(prompt)
            logger.debug(f"Query response for '{query_text}': {response.text}")
            return response.text
        except Exception as e:
            logger.error(f"Error processing query '{query_text}': {str(e)}")
            return f"Error processing query: {str(e)}"