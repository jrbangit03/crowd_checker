from ..utilities.embeddings import ModelEmbeddings, OpenAIModelEmbeddings, \
    HuggingFaceModelEmbeddings


def get_embedder(provider: str) -> ModelEmbeddings:
    providers = {"OPENAI": OpenAIModelEmbeddings(),
                 "HUGGING_FACE": HuggingFaceModelEmbeddings()}
    return providers.get(provider, HuggingFaceModelEmbeddings())

