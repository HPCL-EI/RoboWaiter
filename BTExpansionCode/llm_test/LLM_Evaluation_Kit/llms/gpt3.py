import os

from openai import OpenAI


class LLMGPT3():
    def __init__(self):
        self.client = OpenAI(
            base_url="URL", api_key="Your-Key")

    def request(self, message):  # question
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=message
        )

        return completion.choices[0].message.content

    def embedding(self, question):
        embeddings = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=question
        )

        return embeddings

    def list_models(self):
        response = self.client.models.list()
        return response.data

    def list_embedding_models(self):
        models = self.list_models()
        embedding_models = [model.id for model in models if "embedding" in model.id]
        return embedding_models


if __name__ == '__main__':
    llm = LLMGPT3()
    embedding_models = llm.list_embedding_models()
    print("Available embedding models:")
    for model in embedding_models:
        print(model)

    models = llm.list_models()
    for model in models:
        print(model.id)

    # answer = llm.request(question="who are you,gpt?")
    # # answer = llm.embedding(question="who are you,gpt?")
    # print(answer)

