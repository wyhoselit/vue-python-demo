from sentence_transformers import SentenceTransformer

class EmbeddingGenerator:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """
        Initializes the EmbeddingGenerator with a Sentence-Transformer model.

        Args:
            model_name (str): The name of the pre-trained model to load.
        """
        self.model = SentenceTransformer(model_name)

    def generate_embedding(self, text: str):
        """
        Generates a vector embedding for a given text.

        Args:
            text (str): The input text to embed.

        Returns:
            list[float]: The generated embedding as a list of floats.
        """
        embedding = self.model.encode(text)
        return embedding.tolist()

    def generate_embeddings(self, texts: list[str]):
        """
        Generates vector embeddings for a list of texts.

        Args:
            texts (list[str]): A list of input texts to embed.

        Returns:
            list[list[float]]: A list of generated embeddings, each as a list of floats.
        """
        embeddings = self.model.encode(texts)
        return embeddings.tolist()

