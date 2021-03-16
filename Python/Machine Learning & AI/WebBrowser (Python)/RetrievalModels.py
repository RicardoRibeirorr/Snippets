#O metedo seguinte retorna os docIds dos documentos que têm 1 ou mais termos passados por parametros
def Union(postings):
    unionSet=set()
    #corre os postings e traz os seus valores
    for post in postings:
        #introduz o primeiro valor da lista, de modo a que possa ser utilizado posteriormente,
        #sem que a union atue sobre uma lista vazia
        if(len(unionSet) == 0):
            unionSet = post
            continue
        #uniao dos documentos que tenham 1 ou mais ocorrencias do mesmo termo
        unionSet = set.union(unionSet,post)
    return list(unionSet) 



#O metedo seguinte retorna os docIds dos documentos que tenham todos os termos pretendidos
def Intersection(postings):
    intersectionSet=set()
    for post in postings:
        #introduz o primeiro valor da lista, de modo a que possa ser utilizado posteriormente,
        #sem que a union atue sobre uma lista vazia
        if(len(intersectionSet) == 0):
            intersectionSet = post
            continue
        #interseção entre termos
        intersectionSet = set.intersection(intersectionSet,post)
    return list(intersectionSet) 



#O metedo seguinte retorna os docIds dos documentos que tenham todos os termos pretendidos e 
# que na lista se encontrem na mesma ordem que a query
def Restrict(positionalList,postings):
    #não terminado
    return false;