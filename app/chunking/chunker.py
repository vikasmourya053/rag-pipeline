# from app.models.chunk import Chunk

# class Chunker:

#     def __init__(self, chunk_size=500):
#         self.chunk_size = chunk_size

#     def split(self, documents):

#         chunks = []

#         for document in documents:

#             text = document.page_content

#             for i in range(0, len(text), self.chunk_size):

#                 chunk_text = text[i:i+self.chunk_size]

#                 chunks.append(
#                     Chunk(
#                         text=chunk_text,
#                         metadata=document.metadata
#                     )
#                 )

#         return chunks



from pathlib import Path

from app.models.chunk import Chunk


class Chunker:

    def __init__(self, chunk_size=500):
        self.chunk_size = chunk_size

    def split(self, documents):

        chunks = []

        for document in documents:

            text = document.page_content

            # Copy metadata
            metadata = document.metadata.copy()

            # Add filename
            if "source" in metadata:
                metadata["file_name"] = Path(metadata["source"]).name

            for i in range(0, len(text), self.chunk_size):

                chunk_text = text[i:i + self.chunk_size]

                chunks.append(
                    Chunk(
                        text=chunk_text,
                        metadata=metadata
                    )
                )

        return chunks