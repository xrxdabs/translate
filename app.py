from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from textblob import TextBlob
import nltk
from nltk.tokenize import sent_tokenize
import json
import requests
import urllib.parse

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('text', type=str)

class Translator(Resource):
    def get(self):
        text = parser.parse_args()
        tl_blob = TextBlob(text["text"])
        
        try:
            translated = tl_blob.translate(from_lang='tl', to='en')
        except:
            translated = text["text"]
        
        # return json.loads(json.dumps(str(translated)))
        tag=str(translated)
        
        tokens=nltk.word_tokenize(tag)
        pos_tag = nltk.pos_tag(tokens)

        # kuha lang ng adjective, proper noun, adverb, verb 
        tags = [
            'JJ',
            'JJR',
            'JJS',
            'VB',
            'VBG',
            'VBD',
            'VBN',
            'VBP',
            'VBZ',
            'NN',
            'NNPS'
        ]

        # final words
        final = []

        for i in pos_tag:
            if i[1] in tags:
                final.append(i[0])

        return json.loads(json.dumps(final))
        
api.add_resource(Translator, '/translate')

if __name__ == '__main__':
    app.run(debug=True)



'''
for deployment
'''

# execute in python

#import nltk
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('tagsets')