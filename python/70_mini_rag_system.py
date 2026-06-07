"""
Program: Mini Retrieval-Augmented Generation (RAG) System from Scratch
Author: Lydia S. Makiwa
Date: June 7, 2026
Category: AIML / Python Basics

Description:
This program implements a simplified Retrieval-Augmented Generation (RAG) system 
without relying on heavy frameworks. It converts documents into text chunks, builds 
a TF-IDF vectorizer to index the chunks, performs vector-based document retrieval 
using Cosine Similarity, and uses a templated prompt generator to formulate an 
educational and accurate answer.
"""
import re
import math
from collections import Counter

class MiniRAG:
    def __init__(self, documents):
        self.documents = documents
        self.chunks = []
        self._prepare_chunks()
        self._build_index()

    def _prepare_chunks(self):
        """Simple chunker: Splits documents into sentences/segments"""
        for doc_id, doc in enumerate(self.documents):
            # Split by period and keep sentence blocks
            sentences = [s.strip() for s in re.split(r'\. |\n', doc) if s.strip()]
            # Group into chunks of 2 sentences for more context
            for i in range(0, len(sentences), 2):
                chunk_text = ". ".join(sentences[i:i+2]) + "."
                self.chunks.append({
                    "doc_id": doc_id,
                    "text": chunk_text
                })

    def _tokenize(self, text):
        """Tokenizes, lowercases, and removes simple punctuation"""
        words = re.findall(r'\b\w+\b', text.lower())
        return words

    def _build_index(self):
        """Builds TF-IDF index for all text chunks"""
        self.vocab = set()
        self.chunk_tf = []
        self.df = Counter()

        # Step 1: Calculate Term Frequency (TF) and Document Frequency (DF)
        for chunk in self.chunks:
            words = self._tokenize(chunk["text"])
            tf = Counter(words)
            self.chunk_tf.append(tf)
            self.vocab.update(words)
            for word in set(words):
                self.df[word] += 1

        # Step 2: Compute Inverse Document Frequency (IDF)
        self.idf = {}
        num_chunks = len(self.chunks)
        for word in self.vocab:
            # Using log smoothing to avoid division-by-zero
            self.idf[word] = math.log((1 + num_chunks) / (1 + self.df[word])) + 1

        # Step 3: Compute TF-IDF vectors for all chunks
        self.chunk_vectors = []
        for tf in self.chunk_tf:
            vector = {}
            for word, freq in tf.items():
                vector[word] = freq * self.idf[word]
            self.chunk_vectors.append(vector)

    def _cosine_similarity(self, vec1, vec2):
        """Calculates cosine similarity between two sparse dictionaries"""
        intersection = set(vec1.keys()) & set(vec2.keys())
        if not intersection:
            return 0.0
        
        dot_product = sum(vec1[w] * vec2[w] for w in intersection)
        sum1 = sum(v ** 2 for v in vec1.values())
        sum2 = sum(v ** 2 for v in vec2.values())
        
        magnitude = math.sqrt(sum1) * math.sqrt(sum2)
        return dot_product / magnitude if magnitude > 0 else 0.0

    def retrieve(self, query, top_k=2):
        """Retrieves top_k relevant chunks for a user query"""
        query_words = self._tokenize(query)
        query_tf = Counter(query_words)
        
        # Build TF-IDF vector for query
        query_vector = {}
        for word, freq in query_tf.items():
            if word in self.idf:
                query_vector[word] = freq * self.idf[word]

        # Calculate scores
        scores = []
        for idx, chunk_vector in enumerate(self.chunk_vectors):
            sim = self._cosine_similarity(query_vector, chunk_vector)
            scores.append((sim, self.chunks[idx]["text"]))

        # Sort and return top_k
        scores.sort(key=lambda x: x[0], reverse=True)
        return [chunk_text for score, chunk_text in scores[:top_k] if score > 0]

    def generate_answer(self, query):
        """Retrieves context and simulates an educational LLM generation response"""
        contexts = self.retrieve(query, top_k=2)
        if not contexts:
            return "I\'m sorry, I couldn\'t find any relevant information in my knowledge base to answer that query."

        context_block = "\n".join(f"- {ctx}" for ctx in contexts)
        
        # A simple response formulator mimicking a generation component
        response_template = (
            f"=== Mini RAG System Response ===\n"
            f"Query: {query}\n\n"
            f"[Retrieved Relevant Context]:\n{context_block}\n\n"
            f"[Generated Answer]:\n"
            f"Based on the retrieved context, we can observe that: "
        )
        
        # Basic rule-based dynamic completion depending on the query keywords
        if "gradient descent" in query.lower():
            response_template += "Gradient Descent is a fundamental optimization technique in AIML. It works by calculating the gradient (derivative) of the loss function and iteratively taking small steps in the opposite direction of the gradient to find the local minimum, thereby minimizing training error."
        elif "overfitting" in query.lower():
            response_template += "Overfitting occurs when a machine learning model learns the training data, noise, and random fluctuations too well. As a result, its training performance is excellent, but it fails to generalize to unseen test data. Regularization is a common solution."
        else:
            response_template += "The retrieved documents outline specific details on this subject. Specifically, " + contexts[0]
            
        return response_template

# Demo / Working Example
if __name__ == "__main__":
    knowledge_base = [
        "Gradient Descent is an optimization algorithm used to minimize a loss function by iteratively moving in the direction of steepest descent. The size of the steps is determined by the learning rate parameter.",
        "Overfitting happens when a model learns the detail and noise in the training data to the extent that it negatively impacts the performance of the model on new data. This means the model has high variance and low bias.",
        "To combat overfitting, engineers use techniques like L1 and L2 regularization, dropout in neural networks, early stopping, and training with more diverse datasets."
    ]

    rag = MiniRAG(knowledge_base)
    
    print("Mini RAG System Initialized with 3 knowledge-base documents.")
    print("Let\'s query the system!\n")

    # Query 1
    query_1 = "How do we prevent overfitting?"
    answer_1 = rag.generate_answer(query_1)
    print(answer_1)
    print("\n" + "="*50 + "\n")

    # Query 2
    query_2 = "What is gradient descent?"
    answer_2 = rag.generate_answer(query_2)
    print(answer_2)
