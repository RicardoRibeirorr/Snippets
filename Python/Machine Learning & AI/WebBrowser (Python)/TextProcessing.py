import spacy
import nltk
import unicodedata
import re
import requests

from nltk.stem import PorterStemmer
from nltk.stem import RSLPStemmer

CONTRACTION_MAP = {
"ain't": "is not",
"aren't": "are not",
"can't": "cannot",
"can't've": "cannot have",
"'cause": "because",
"could've": "could have",
"couldn't": "could not",
"couldn't've": "could not have",
"didn't": "did not",
"doesn't": "does not",
"don't": "do not",
"hadn't": "had not",
"hadn't've": "had not have",
"hasn't": "has not",
"haven't": "have not",
"he'd": "he would",
"he'd've": "he would have",
"he'll": "he will",
"he'll've": "he he will have",
"he's": "he is",
"how'd": "how did",
"how'd'y": "how do you",
"how'll": "how will",
"how's": "how is",
"I'd": "I would",
"I'd've": "I would have",
"I'll": "I will",
"I'll've": "I will have",
"I'm": "I am",
"I've": "I have",
"i'd": "i would",
"i'd've": "i would have",
"i'll": "i will",
"i'll've": "i will have",
"i'm": "i am",
"i've": "i have",
"isn't": "is not",
"it'd": "it would",
"it'd've": "it would have",
"it'll": "it will",
"it'll've": "it will have",
"it's": "it is",
"let's": "let us",
"ma'am": "madam",
"mayn't": "may not",
"might've": "might have",
"mightn't": "might not",
"mightn't've": "might not have",
"must've": "must have",
"mustn't": "must not",
"mustn't've": "must not have",
"needn't": "need not",
"needn't've": "need not have",
"o'clock": "of the clock",
"oughtn't": "ought not",
"oughtn't've": "ought not have",
"shan't": "shall not",
"sha'n't": "shall not",
"shan't've": "shall not have",
"she'd": "she would",
"she'd've": "she would have",
"she'll": "she will",
"she'll've": "she will have",
"she's": "she is",
"should've": "should have",
"shouldn't": "should not",
"shouldn't've": "should not have",
"so've": "so have",
"so's": "so as",
"that'd": "that would",
"that'd've": "that would have",
"that's": "that is",
"there'd": "there would",
"there'd've": "there would have",
"there's": "there is",
"they'd": "they would",
"they'd've": "they would have",
"they'll": "they will",
"they'll've": "they will have",
"they're": "they are",
"they've": "they have",
"to've": "to have",
"wasn't": "was not",
"we'd": "we would",
"we'd've": "we would have",
"we'll": "we will",
"we'll've": "we will have",
"we're": "we are",
"we've": "we have",
"weren't": "were not",
"what'll": "what will",
"what'll've": "what will have",
"what're": "what are",
"what's": "what is",
"what've": "what have",
"when's": "when is",
"when've": "when have",
"where'd": "where did",
"where's": "where is",
"where've": "where have",
"who'll": "who will",
"who'll've": "who will have",
"who's": "who is",
"who've": "who have",
"why's": "why is",
"why've": "why have",
"will've": "will have",
"won't": "will not",
"won't've": "will not have",
"would've": "would have",
"wouldn't": "would not",
"wouldn't've": "would not have",
"y'all": "you all",
"y'all'd": "you all would",
"y'all'd've": "you all would have",
"y'all're": "you all are",
"y'all've": "you all have",
"you'd": "you would",
"you'd've": "you would have",
"you'll": "you will",
"you'll've": "you will have",
"you're": "you are",
"you've": "you have"
}
stopword_list = nltk.corpus.stopwords.words('portuguese')
stopword_list

def sentence_segmentation(text,language='english', NLTK=True):
    sentences = []
    
    if NLTK:
        sentences = nltk.sent_tokenize(text)
    else:
        if language == 'english':
            nlp = spacy.load('en_core_web_sm',disable=['tagger', 'ner'])
        elif language == 'portuguese':
            nlp = spacy.load('pt_core_news_sm',disable=['tagger', 'ner'])
            
        if len(text) > 500000:
            ListOfChunks = chunks(text,500000)
            for chunk in ListOfChunks:
                doc = nlp(chunk)

                for sent in doc.sents:
                    sentences.append(sent.text)
        else:
            doc = nlp(text)

            for sent in doc.sents:
                sentences.append(sent.text)
    
    return sentences

def chunks(text, n):
    ListOfChunks = []
    
    """successive n-sized chunks from l."""
    for i in range(0, len(text), n):
        ListOfChunks.append(text[i:i + n])
    
    return ListOfChunks


def remove_extra_newlines(text):
    text = re.sub(r'[\r|\n|\r\n]+', ' ',text)
    return text

def remove_accented_chars(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    return text


def expand_contractions(text, contraction_mapping=CONTRACTION_MAP):
    
    contractions_pattern = re.compile('({})'.format('|'.join(contraction_mapping.keys())), 
                                      flags=re.IGNORECASE|re.DOTALL)
    def expand_match(contraction):
        match = contraction.group(0)
        first_char = match[0]
        expanded_contraction = contraction_mapping.get(match)\
                                if contraction_mapping.get(match)\
                                else contraction_mapping.get(match.lower())                       
        expanded_contraction = first_char+expanded_contraction[1:]
        return expanded_contraction
        
    expanded_text = contractions_pattern.sub(expand_match, text)
    expanded_text = re.sub("'", "", expanded_text)
    return expanded_text

def remove_special_characters(text, remove_digits=False):
    # insert spaces between special characters to isolate them    
    special_char_pattern = re.compile(r'([{.(-)!}])')
    text = special_char_pattern.sub(" \\1 ", text)
    
    #remove special chars
    pattern = r'[^a-zA-z0-9\s]' if not remove_digits else r'[^a-zA-z\s]'
    text = re.sub(pattern, '', text)
    
    #remove extra space
    text = re.sub(' +', ' ', text)

    return text

def lowerCase(text):
    return text.lower()


def stemming(text, language='english'):
    s=""
    if language == 'english':
        s = PorterStemmer()
    elif language == 'portuguese':
        s = RSLPStemmer()
    text = ' '.join([s.stem(word) for word in text.split()])
    return text



def lemmatization(text,language='english'):
    
    if language == 'english':
        nlp = spacy.load('en_core_web_sm',disable=['tagger', 'parser', 'ner'])
    elif language == 'portuguese':
        nlp = spacy.load('pt_core_news_sm',disable=['tagger', 'parser', 'ner'])

    if len(text) > 500000:
        ListOfChunks = chunks(text,500000)
        for chunk in ListOfChunks:
            doc = nlp(chunk)
            text = ' '.join([word.lemma_ for word in doc])
    else:
        doc = nlp(text)
        text = ' '.join([word.lemma_ for word in doc])
    
    return text



def stopwords_removal(text, is_lower_case=False, language = "english",NLTK=False):
    stopword_list = nltk.corpus.stopwords.words(language)

    ListOfTokens = []
    
    if NLTK:
        ListOfTokens = nltk.word_tokenize(text)
    else:
        if language == 'english':
            nlp = spacy.load('en_core_web_sm',disable=['tagger', 'parser', 'ner'])
        elif language == 'portuguese':
            nlp = spacy.load('pt_core_news_sm',disable=['tagger', 'parser', 'ner'])

        if len(text) > 500000:
            ListOfChunks = chunks(text,500000)
            for chunk in ListOfChunks:
                doc = nlp(chunk)
                for token in doc:
                    ListOfTokens.append(token.text.strip()) #empty characters to be removed from beginning or end of the string.
        else:
            doc = nlp(text)
            for token in doc:
                ListOfTokens.append(token.text.strip()) #empty characters to be removed from beginning or end of the string.

    #Se o texto estÃ¡ lowercased entÃ£o entra na primeira condiÃ§Ã£o. Se nÃ£o estÃ¡ lowercased entÃ£o tem que se aplicar a funÃ§Ã£o lower ao token para comparar com a lista de stopwords (que estÃ¡ toda a lowercased)
    if is_lower_case:
        filtered_tokens = [token for token in ListOfTokens if token not in stopword_list]
    else:
        filtered_tokens = [token for token in ListOfTokens if token.lower() not in stopword_list]

    filtered_text = ' '.join(filtered_tokens)    
    
    return filtered_text


def tokenization(text,language='english', NLTK=False):
    ListOfTokens = []
    
    if NLTK:
        ListOfTokens = nltk.word_tokenize(text)
    else:
        if language == 'english':
            nlp = spacy.load('en_core_web_sm',disable=['tagger', 'parser', 'ner'])
        elif language == 'portuguese':
            nlp = spacy.load('pt_core_news_sm',disable=['tagger', 'parser', 'ner'])
            
        if len(text) > 500000:
            ListOfChunks = chunks(text,500000)
            for chunk in ListOfChunks:
                doc = nlp(chunk)

                for token in doc:
                    ListOfTokens.append(token.text)
        else:
            doc = nlp(text)

            for token in doc:
                ListOfTokens.append(token.text)
    
    return ListOfTokens


def PoS(text,language='english', NLTK=False):
    ListOfPoS = []
    
    if NLTK:       
        tokens = nltk.word_tokenize(text)
        ListOfPoS = nltk.pos_tag(tokens)

    else:
        if language == 'english':
            nlp = spacy.load('en_core_web_sm',disable=['ner'])
        elif language == 'portuguese':
            nlp = spacy.load('pt_core_news_sm',disable=['ner'])
            
        if len(text) > 500000:
            ListOfChunks = chunks(text,500000)
            for chunk in ListOfChunks:
                doc = nlp(chunk)

                for token in doc:
                    ListOfPoS.append((token,token.tag_))
        else:
            doc = nlp(text)

            for token in doc:
                ListOfPoS.append((token,token.tag_))
    
    return ListOfPoS


def NER(text,language='english'):
    
    ListOfNER = []
        
    if language == 'english':
        nlp = spacy.load('en_core_web_sm',disable=['tagger', 'parser'])
    elif language == 'portuguese':
        nlp = spacy.load('pt_core_news_sm',disable=['tagger', 'parser'])

    if len(text) > 500000:
        ListOfChunks = chunks(text,500000)
        for chunk in ListOfChunks:
            doc = nlp(chunk)
            for token in doc.ents:
                ListOfNER.append((token.text,token.label_))
    else:
        doc = nlp(text)
        for token in doc.ents:
            ListOfNER.append((token.text,token.label_))
    
    return ListOfNER


def normalize_corpus(corpus, html_stripping=True,
accented_char_removal=True, contraction_expansion=True,
text_lower_case=True, special_char_removal=True, remove_digits=True):

    data = corpus
    if(html_stripping):
        data = sentence_segmentation(data)
    if(accented_char_removal or contraction_expansion or text_lower_case 
       or remove_extra_newlines or remove_digits):
        tempData = []
        for sentence in data:
            if(accented_char_removal):
                sentence= remove_accented_chars(sentence)

            if(contraction_expansion):
                sentence = expand_contractions(sentence)

            if(text_lower_case):  
                sentence = lowerCase(sentence)

            if(special_char_removal):
                sentence = remove_special_characters(sentence)

            if(remove_digits):  
                sentence =remove_extra_newlines(sentence)
                
            tempData.append(sentence)
        
        data = tempData
    return data