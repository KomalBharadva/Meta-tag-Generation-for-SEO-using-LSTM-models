#from __future__ import division, print_function
from flask import Flask, request, render_template
from keras.models import load_model
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
tokenizer = Tokenizer()
import keras.utils as ku 
import tensorflow
tensorflow.random.set_seed(2)
import pandas as pd
import numpy as np
import string, warnings
warnings.filterwarnings("ignore")
warnings.simplefilter(action='ignore', category=FutureWarning)

# Define a flask app
app = Flask(__name__)

df = pd.read_csv("linux_master_df.csv")
df = df.loc[df['position'].isin([1,2,3])]
df['metatags'] = df['metatags'].str.replace(r'\\r', '',regex=True)
df['metatags'] = df['metatags'].str.replace(r'\\n', ' ',regex=True)
df['metatags'] = df['metatags'].str.replace(r'\\xa0', '',regex=True)

def clean_text(txt):
    txt = "".join(v for v in txt if v not in string.punctuation).lower()
    txt = txt.encode("utf8").decode("ascii",'ignore')
    return txt 
corpus = [clean_text(x) for x in df['metatags']]

tokenizer = Tokenizer()
def get_sequence_of_tokens(corpus):
    ## tokenization
    tokenizer.fit_on_texts(corpus)
    total_words = len(tokenizer.word_index) + 1
    ## convert data to sequence of tokens 
    input_sequences = []
    for line in corpus:
        token_list = tokenizer.texts_to_sequences([line])[0]
        for i in range(1, len(token_list)):
            n_gram_sequence = token_list[:i+1]
            input_sequences.append(n_gram_sequence)
    return input_sequences, total_words
inp_sequences, total_words = get_sequence_of_tokens(corpus)

sample_in = inp_sequences[:10000]
def generate_padded_sequences(input_sequences):
    max_sequence_len = max([len(x) for x in input_sequences])
    input_sequences = np.array(pad_sequences(input_sequences, maxlen=max_sequence_len, padding='pre'))
    predictors, label = input_sequences[:,:-1],input_sequences[:,-1]
    label = ku.to_categorical(label, num_classes=total_words)
    return predictors, label, max_sequence_len
predictors, label, max_sequence_len = generate_padded_sequences(sample_in)

# Load your trained model
loaded_model = load_model('network.h5')

def generate_text(seed_text, next_words, model=loaded_model, max_sequence_len=223):
    for i in range(next_words):
        token_list = tokenizer.texts_to_sequences([seed_text])[0]
        token_list = pad_sequences([token_list], maxlen=max_sequence_len-1, padding='pre')
        predicted = model.predict_classes(token_list, verbose=0)
        
        output_word = ""
        for word,index in tokenizer.word_index.items():
            if index == predicted:
                output_word = word
                break
        seed_text += " "+output_word
    return seed_text.title()

@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html', length = 10)

@app.route('/', methods=['POST'])
def generate_bootstrap():
    initial_text = request.form.get('input')
    length = int(request.form.get('length'))
    generated = generate_text(initial_text, length)
    return render_template('index.html', input = initial_text, length = length, output = generated)

if __name__ == '__main__':
    app.run(debug=True)