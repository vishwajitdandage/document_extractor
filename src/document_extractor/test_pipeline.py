
from document_extractor.pdf_loader import extract_pdf_pages
from document_extractor.chunker import chunk_pages
from document_extractor.embedder import LocalEmbedder
from document_extractor.vector_store import VectorStore
from document_extractor.answer_generator import AnswerGenerator
from pathlib import Path

def main():
    print("Document ingestion pipeline")

    pdf_path = input("Enter PDF path: ").strip()

    # 1. Extract PDF text
    pages = extract_pdf_pages(pdf_path)
    print(f"Pages extracted: {len(pages)}")

    # 2. Split text into chunks
    chunks = chunk_pages(pages, chunk_size=1000, overlap=150)
    print(f"Chunks created: {len(chunks)}")

    if not chunks:
        print("No chunks found. Check the PDF.")
        return

    # 3. Generate embeddings
    embedder = LocalEmbedder()
    vectors = embedder.embed_documents(
        [chunk["text"] for chunk in chunks]
    )
    print(f"Embeddings generated: {len(vectors)}")

    # 4. Store chunks and embeddings
    store = VectorStore()

    # Remove outdated chunks before indexing the latest version.
    store.delete_source(Path(pdf_path).name)
    store.add_chunks(chunks, vectors)

    print(f"Total chunks in database: {store.collection.count()}")

    # 5. Retrieve relevant passages
    question = input("\nAsk a question about the PDF: ").strip()

    if not question:
        print("No question provided.")
        return

    query_vector = embedder.embed_query(question)
    results = store.search(query_vector, top_k=5)

    #print("\n--- Retrieved passages ---")

    # for index, text in enumerate(results["documents"][0], start=1):
    #     metadata = results["metadatas"][0][index - 1]
    #     distance = results["distances"][0][index - 1]

    #     # print(f"\nResult {index}")
    #     # print(f"Source: {metadata['source']}")
    #     # print(f"Page: {metadata['page']}")
    #     # print(f"Cosine distance: {distance:.4f}")
    #     # print(text[:500])

    # 6. Generate answer
    answer_generator = AnswerGenerator()
    answer = answer_generator.generate(question, results)
    print(f"\nGenerated Answer:\n{answer}")

if __name__ == "__main__":
    main()
