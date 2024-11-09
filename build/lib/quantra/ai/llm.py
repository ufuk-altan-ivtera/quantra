import os
from groq import Groq
from requests import post

GROQ_API_KEY = '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'

class ObtainModel():
    """
    A class used to obtain models.

    Methods
    -------
    obtain_llm_model():
        Obtains a Groq LLM model.
        
    obtain_embedding_model(model_string='all-MiniLM-L6-v2'):
        Obtains a SentenceTransformer model.
    """

    def obtain_language_model(self, tool = 'groq'):
        """
        Obtains a Groq LLM model.

        Returns
        -------
        Groq
            The Groq LLM model.
        """
        if tool == 'groq':
            language_model = Groq(api_key = GROQ_API_KEY)
       
        elif tool == 'ollama':

            model_string = 'llama3:70b'
            #language_model = ChatOllama(model=model_string, base_url='http://178.157.11.179:11434')

        else:
            raise(f"{tool} isn't available !")
            
        return language_model
    
    # def obtain_embedding_model(self, tool = 'ollama', model_string='nomic-embed-text'):
    #     """
    #     Obtains a SentenceTransformer model.

    #     Parameters
    #     ----------
    #     model_string : str, optional
    #         The model string to load (default is 'all-MiniLM-L6-v2').
    #         'all-MiniLM-L6-v2', 'nomic-embed-text'

    #     Returns
    #     -------
    #     SentenceTransformer
    #         The SentenceTransformer model.
    #     """
    #     if tool == 'ollama':
    #         embedding_model = OllamaEmbeddings(model=model_string)
    #     elif tool == 'sentence_transformer':
    #         embedding_model = SentenceTransformer(model_string)
            
    #     return embedding_model

class Predict():
    """
    A class used to make predictions using the LLM model.

    Methods
    -------
    predict_prompt(llm_model, prompt, model_string="llama3-8b-8192"):
        Generates a response from the LLM model based on the given prompt.
        
    predict_embeddings(sentence_list):
        Generates embeddings for the given list of sentences.
    """

    def predict_prompt(self, llm, prompt, model_string = 'llama3-70b-8192', env = 'cloud'):
        """
        llama3-8b-8192
        llama3-70b-8192
        mixtral-8x7b-32768
        """
        if env == 'on-prem':
            response = post("http://ollama:11434/api/chat", json=prompt)
            prediction_dict = response.json()
            prompt_response = prediction_dict["message"]["content"]

        else: 
            chat_completion = llm.chat.completions.create(messages=[{"role": "user", "content": prompt}], model=model_string)
            prompt_response = chat_completion.choices[0].message.content

        return prompt_response
        
    def predict_embeddings(self, embedding_model, query):
        """
        Generates embeddings for the given query.

        Parameters
        ----------
        query : str
            A query string to embed.

        Returns
        -------
        numpy.ndarray
            An array of embeddings.
        """
        embedding = embedding_model.encode([query])[0].tolist()
        return embedding
