import TextProcessing
import json
import os

class InvertedIndex:
    def __init__(self, stemming=True, lemmatization=False, stopwords=False, language="english"):
        self.index = {}
        self.listOfURLs = []
        self.stemming = stemming
        self.lemmatization = lemmatization
        self.stopwords = stopwords
        self.language = language

    #Processa o texto do documento. Os metedos provêm do package TextProcessing
    def __TextProcessing__(self, doc):
        data = TextProcessing.remove_special_characters(doc)
        data = TextProcessing.lowerCase(data)
        #atua se o stemming for desejado
        if(self.stemming):
            data = TextProcessing.stemming(data,self.language) 
        #atua se o lemmatization for desejado
        if(self.lemmatization):        
            data = TextProcessing.lemmatization(data,self.language)
        #atua se o stopwords for desejado
        if(self.stopwords):     
            data = TextProcessing.stopwords_removal(data,self.language)
        data = TextProcessing.tokenization(data, self.language)
        return data

    
    #Guarda os indexes e os urls a eles destinados
    def save2JSon(self):
        os.makedirs(os.path.dirname("data/InvertedIndex.json"), exist_ok=True)
        os.makedirs(os.path.dirname("data/URLs.json"), exist_ok=True)
        with open("data/InvertedIndex.json", 'w') as outfile:  
            json.dump(self.index, outfile)
        with open("data/URLs.json", 'w') as outfile:  
            json.dump(self.listOfURLs, outfile)

            
            
            
    #Carrega os documentos de indexes e urls, e atribui os seus valores
    #à nas variaveis a eles destinados na classe mãe
    def loadFromJSon(self,loadPath):
        with open(loadPath+"InvertedIndex.json") as json_file:  
            self.index=json.load(json_file)
        with open(loadPath+"URLs.json") as json_file:  
            self.listOfURLs=json.load(json_file)

            
            
            
    #adiciona um novo index na lista de indexes
    def __addPositional__(self, term, offset, docID):
        self.index[term]=[
            1,
            1,
            {
                docID:[
                    1,
                    [offset]
                ]
            }
        ]
    
    
    
    #atualização do índex na lista de indexes
    def __updatePositional__(self, term, offset, docID):
        obj = self.index[term]
        #verifica se o termo contem o documento em causa "docID", e se sim:
        if(docID in obj[2]):
            #Acresce um valor ao total de vezes que já surgio.
            obj[1] = int(obj[1]) + 1  
            #Acresce um valor ao total de vezes que já surgio no documento em causa.
            obj[2][docID][0] = int(obj[2][docID][0]) + 1
            #Adiciona a posição(indice/localização) onde se encontra na lista de posições. 
            obj[2][docID][1].append(offset)
        else:
            #Acresce um valor no nº de documento onde aparece
            obj[0] = int(obj[0]) + 1
            #Acresce um valor ao total de vezes que já surgio.
            obj[1] = int(obj[1]) + 1  
            #Adiciona o documento á lista de documentos do termo, bem como a frequencia 
            #e a posição onde o termo se encontra
            obj[2][docID]=[
                1,
                [offset]
            ]
        
    #Metedo responsavel por formatar e adicionar indexes e urls
    #É um metedo de alocagem, querendo isto dizer, que é o responsavel por adicionar conteudo
    #de pesquisa ao sistema
    def add(self, doc, url):
        #Adiciona o url à lista de urls. Util tambem para verificar o index do
        #documento, como pode verificar a seguir na chamada às funções __updatePositional__ e __addPositional__
        self.listOfURLs.append(url)
        doc = self.__TextProcessing__(doc)
        #Corrimento entre todos os indices da lista de termos do documento que deseja adicionar,
        #de forma a obter a posição em que se encontra em primeira mão. Este metedo melhora o tempo 
        #e o processamento consumido no cumprimento das necessidades seguintes(obtenção da word)
        for index in range(len(doc)):
            word = doc[index]
            #verifica o termo já existe na lista de termos da class, se não existir
            #insere um novo termo à lista, se sim faz o update aos dados:
            if word in self.index:
                self.__updatePositional__(word,index,len(self.listOfURLs)-1)
            else:
                self.__addPositional__(word,index,len(self.listOfURLs)-1)
        return self.index
    
    
    #Metedo responsavel por fazer a pesquisa. Utilizado como se fosse o campo de pesquisa da google
    def lookup(self, query, loadPath):
        #carrega a informação guardada nos ficheiros URLs.json e InvertedIndex.json
        self.loadFromJSon(loadPath)
        #Processa o text
        query = self.__TextProcessing__(query)
        positionalList = {}
        #executa um corrimento dos termos na frase(se for o caso) e devolve se existir
        #da lista de termos o objeto a ela correspondente
        for term in query:
            termValue = self.index.get(term)
            if(termValue != None):
                positionalList[term]=termValue
        return positionalList
    
    
    #Convert a lista de positionals em postings, querendo isto dizer que do elevado contiudo 
    #exitente nas positionals, returnará apenas os docIds neles existentes
    def listOfPositional2ListOfPostings(self, listOfPositionals):
        listOfDocs = []
        for positionIndex in listOfPositionals.values():
            #retorno do valor do docId, que está disposto no index 2
            listOfDocs.append(set(positionIndex[2].keys()))
        return listOfDocs
    
    #Função opcional que tem como intuito carregar um ficheiro json
    def openJsonFile(self,loc):
        with open(loc) as json_file:  
            return json.load(json_file)