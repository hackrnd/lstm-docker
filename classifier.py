import os
from keras.models import model_from_json
import pandas as pd
import pickle
from keras.preprocessing.sequence import pad_sequences
import config as cfg
from azure.storage.blob import BlockBlobService

def download_model():
        print("Downloading model from Azure storage")
        block_blob_service = BlockBlobService(account_name=os.environ['AZURE_STORAGE_ACCOUNT'], account_key=os.environ['AZURE_STORAGE_KEY'])
        container_name = os.environ['AZURE_STORAGE_CONTAINER']
        block_blob_service.get_blob_to_path(container_name, cfg.model, cfg.model)
        block_blob_service.get_blob_to_path(container_name, cfg.tokenizer_path, cfg.tokenizer_path)
        block_blob_service.get_blob_to_path(container_name, cfg.model_weights, cfg.model_weights)

class Classifier: 

    if not os.path.exists(cfg.model): 
        download_model()

    try:
        os.environ['FORCE_DOWNLOAD_MODEL']
        download_model()
    except KeyError:
        pass

    # load json and create model
    json_file = open(cfg.model, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights(cfg.model_weights)
    loaded_model.compile(loss='binary_crossentropy', optimizer='Adam')

    with open(cfg.tokenizer_path,'rb') as handle:
        tokenizer = pickle.load(handle)


    def classify(self,msg):
        x = pd.Series(msg)
        sequencesp = self.tokenizer.texts_to_sequences(x)
        x = pad_sequences(sequencesp, maxlen=cfg.max_sent_len)

        p = self.loaded_model.predict(x)
        temp = []
        for i in p:
                if i[0]>i[1]:
                    temp.append("IR")
                else:
                    temp.append("SR")
        p = temp[0]       
        return p