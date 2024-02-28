from typing import List

from langchain_community.vectorstores.faiss import FAISS

from langflow.components.vectorstores.base.model import LCVectorStoreComponent
from langflow.field_typing import Embeddings
from langflow.schema import Record


class FAISSSearchComponent(LCVectorStoreComponent):
    display_name = "FAISS Search"
    description = "Search a FAISS Vector Store for similar documents."
    documentation = "https://python.langchain.com/docs/modules/data_connection/vectorstores/integrations/faiss"

    def build_config(self):
        return {
            "documents": {"display_name": "Documents"},
            "embedding": {"display_name": "Embedding"},
            "folder_path": {
                "display_name": "Folder Path",
                "info": "Path to save the FAISS index. It will be relative to where Langflow is running.",
            },
            "input_value": {"display_name": "Input"},
            "index_name": {"display_name": "Index Name"},
        }

    def build(
        self,
        input_value: str,
        embedding: Embeddings,
        folder_path: str,
        index_name: str = "langflow_index",
    ) -> List[Record]:
        if not folder_path:
            raise ValueError("Folder path is required to save the FAISS index.")
        path = self.resolve_path(folder_path)
        vector_store = FAISS.load_local(
            folder_path=str(path), embeddings=embedding, index_name=index_name
        )
        if not vector_store:
            raise ValueError("Failed to load the FAISS index.")

        return self.search_with_vector_store(
            vector_store=vector_store, input_value=input_value, search_type="similarity"
        )