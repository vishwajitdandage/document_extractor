from pathlib import Path
import tempfile

import streamlit as st

from document_extractor.pdf_loader import extract_pdf_pages
from document_extractor.chunker import chunk_pages
from document_extractor.embedder import LocalEmbedder
from document_extractor.vector_store import VectorStore
from document_extractor.answer_generator import AnswerGenerator


st.set_page_config(
    page_title="Document Explainer",
    page_icon="📄",
    layout="wide",
)

st.title("📄 Document Explainer")
st.caption("Ask questions about your PDFs using local AI.")

# Load expensive components only once per Streamlit session.
@st.cache_resource
def load_components():
    return LocalEmbedder(), AnswerGenerator()


embedder, answer_generator = load_components()

uploaded_file = st.file_uploader(
    "Upload a PDF document",
    type=["pdf"],
)

if uploaded_file:
    if st.button("Process PDF", type="primary"):
        with st.spinner("Extracting, chunking, embedding, and indexing..."):
            # Save the uploaded PDF temporarily.
            with tempfile.NamedTemporaryFile(
                suffix=".pdf", delete=False
            ) as temp_file:
                temp_file.write(uploaded_file.getvalue())
                pdf_path = Path(temp_file.name)

            try:
                pages = extract_pdf_pages(str(pdf_path))
                chunks = chunk_pages(
                    pages,
                    chunk_size=1000,
                    overlap=150,
                )

                if not chunks:
                    st.error("No text chunks were extracted.")
                    st.stop()

                embeddings = embedder.embed_documents(
                    [chunk["text"] for chunk in chunks]
                )

                # Use a persistent store and isolate documents by filename.
                store = VectorStore()
                source_name = uploaded_file.name

                for chunk in chunks:
                    chunk["source"] = source_name
                    chunk["id"] = (
                        f"{source_name}-p{chunk['page']}-c{chunk['chunk_index']}"
                    )

                store.delete_source(source_name)
                store.add_chunks(chunks, embeddings)

                st.session_state["processed_source"] = source_name
                st.session_state["processed_chunks"] = len(chunks)
                st.session_state["processed"] = True

                st.success(
                    f"Indexed {len(chunks)} chunks from {source_name}."
                )
            except Exception as exc:
                st.error(f"Could not process PDF: {exc}")
            finally:
                pdf_path.unlink(missing_ok=True)

if st.session_state.get("processed"):
    st.divider()
    st.subheader("Ask your document")

    st.caption(
        f"Document: {st.session_state['processed_source']} · "
        f"{st.session_state['processed_chunks']} chunks indexed"
    )

    question = st.text_input(
        "Your question",
    )

    if st.button("Get answer") and question.strip():
        with st.spinner("Searching the document and generating an answer..."):
            store = VectorStore()
            query_embedding = embedder.embed_query(question.strip())
            results = store.search(query_embedding, top_k=5)

            answer = answer_generator.generate(
                question.strip(),
                results,
            )

        st.markdown("### Answer")
        st.write(answer)

        with st.expander("Retrieved passages"):
            documents = results.get("documents", [[]])[0]
            metadatas = results.get("metadatas", [[]])[0]
            distances = results.get("distances", [[]])[0]

            if not documents:
                st.info("No relevant passages were retrieved.")
            else:
                for index, (text, metadata) in enumerate(
                    zip(documents, metadatas),
                    start=1,
                ):
                    distance = distances[index - 1]
                    st.markdown(
                        f"**Result {index} — {metadata['source']}, "
                        f"page {metadata['page']}** "
                        f"(distance: {distance:.4f})"
                    )
                    st.write(text)
                    st.divider()