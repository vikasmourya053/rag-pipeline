from pypdf import PdfReader
from app.models.document import Document


class PDFLoader:

    def __init__(self, path):
        self.path = path

    def load(self):
        reader = PdfReader(self.path)

        documents = []

        for page_number, page in enumerate(reader.pages):
            text = page.extract_text()

            documents.append(
                Document(
                    page_content=text,
                    metadata={
                        "source": self.path,
                        "page": page_number + 1
                    }
                )
            )

        return documents