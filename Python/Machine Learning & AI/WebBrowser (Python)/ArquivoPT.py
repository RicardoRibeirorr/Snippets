from datetime import datetime
import requests
import os
import json
import TextProcessing



#Nota: o conteudo a guardar está a ser o snippet de forma a baixar o fluxo e peso dos dados
#Guarda o conteudo em formato desejado, na pasta "data/" dentro do diretorio formatado 
def save2File(request,extension="txt"):
    #busca o conteudo returnado da chamada à api
    for item in request['response_items']:
        #atribui o diretorio formatado bem como o ficheiro json
        filename = "data/" + dateBeautify(item["date"]) + "/" + request['request_parameters']['q'] + "_"  + item['tstamp'] + "_"  + item['digest'] + "." + extension 
        #verifica a existencia dos diretorios bem como do ficheiro, e cria-os caso não existam
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        #abre o ficheiro destinado e insere o conteudo
        file = open(filename, 'w')
        file.write(str(item["snippet"]))
        file.close()

    
    
    
#Guarda o conteudo em formato json na pasta "data/" num diretorio formatado   
def save2Json(request):
    #busca o conteudo returnado da chamada à api
    for item in request['response_items']:
        #atribui o diretorio formatado bem como o ficheiro json
        filename = "data/" + dateBeautify(item["date"]) + "/" + request['request_parameters']['q'] + ".json"
        #verifica a existencia dos diretorios bem como do ficheiro, e cria-os caso não existam
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        #abre o ficheiro destinado e insere o conteudo
        with open(filename, 'w') as json_file:  
            dic = dict(query=request['request_parameters']['q'],digest=item["digest"],title=item["title"],url=item["originalURL"],timestamp = item["tstamp"], content = item["snippet"])
            json.dump(item, json_file)

            
            
#Formata a data para o formato desejado
def dateBeautify(date):
    timestamp = int(date)
    date_time = datetime.fromtimestamp(timestamp)
    return date_time.strftime("%m.%d.%Y")
 
    

    
    
#chamada à api do arquivo.pt
def getContents(payload):
    data = requests.get("https://arquivo.pt/textsearch", params=payload).json()
    #A seguinte linha de codigo, tráz o conteudo estraido da pagina, em vez dele estamos a utilizar o snipped
#     data = requests.get(data["response_items"][0]["linkToExtractedText"])
    return data