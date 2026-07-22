import streamlit as st

from Services.embeddingservice import getreviewsforembedding, generateembeddings, build_faiss_index, searchreviews

st.title("Knowledge Base")

if st.button("Build Knowledge Base"):
    with st.spinner("Generate embeddings and building index... "):
        try:
            df = getreviewsforembedding()
            embedded_df, vectors = generateembeddings(df)
            build_faiss_index(embedded_df, vectors)
            st.success(f"Indexed {len(df)} reviews successfully!")
        except Exception as e:
            st.error(f"Error: {e}")

st.subheader("Search Reviews")
query = st.text_input("Enter your search query (any language):")
if query:
    results = searchreviews(query)
    st.dataframe(results[["review_id", "review_body"]])  