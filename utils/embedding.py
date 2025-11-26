import os
import dotenv
from openai import OpenAI
from utils.vector_utils import vector_store

dotenv.load_dotenv()

class embedding_retriever:
    def __init__(self):
        self.vector_store = vector_store()
        self.api_key = os.getenv("API_KEY")
        self.model_name = os.getenv("EMBEDDING_MODEL_NAME")
        self.url = os.getenv("BASE_URL")

    async def embed_document(self, text):
        doc_embed = await self.embed(text)
        self.vector_store.add_embedding(doc_embed, text)
        return doc_embed
    
    async def embed_query(self, text):
        query_embed = await self.embed(text)
        return query_embed

    async def embed(self, text: str) -> list[float]:
        try:
            client = OpenAI(
                api_key=self.api_key,
                base_url=self.url
            )
            response = client.embeddings.create(
                model=self.model_name,
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"Error embedding text: {e}")
            return None
    
    async def retrieve(self, query: str, top_k: int = 5) -> list[str]:
        query_embed = await self.embed_query(query)
        return self.vector_store.search(query_embed, top_k)

async def main():
    embed = embedding_retriever()
    response = await embed.embed("hello")
    # print(response)


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())