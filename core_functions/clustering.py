import core_functions.similar_docs as sd


def create_List_Vectors_dict(tf_idf_dict):
    """
    Creates and returns a list of dicts where one document is linked to only ONE doc with words as keys in it and the tf*idf as values for each of them.
    Also returns a list of document numbers : the element i in vectorsList refers to the doc number  numberList[i]
    WARNING: it requires to be run after the calculation of tf*idf measures
    """
    vectorsList = []
    numberList = []

    for i in range(107): #107 has to be changed
        a=sd.create_doc_vector_dict(i, tf_idf_dict)
        vectorsList.append([sd.create_doc_vector_dict(i, tf_idf_dict)])
        numberList.append([i])


    return vectorsList, numberList


def merge_Nearest_Elements(vectorsList,numberList):
    """
    Computes the two nearest elements of the vectorsList
    Updates vectorsList and numberList by melting the nearest elements
    """
    similarityMax=0
    currentSimilarity=0
    id1=0
    id2=0


    for i in vectorsList:
        for j in vectorsList:
            if i==j:
                continue
            else:
                #If we compare two texts
                if len(i)==1 and len(j)==1:
                    currentSimilarity=sd.calculate_cosine(i[0], j[0])

                #If we compare 2 groups of texts - Average linkage -----------we can use another method
                else:

                    for k in range(len(i)):
                        for l in range(len(j)):
                            if k==l:
                                continue
                            else:
                                currentSimilarity+=sd.calculate_cosine(i[k], j[l])
                    currentSimilarity*=1/(len(i)*len(j))


                if currentSimilarity > similarityMax:
                    similarityMax=currentSimilarity
                    id1=vectorsList.index(i)
                    id2=vectorsList.index(j)

    vectorsList[id1]+=vectorsList[id2]
    numberList[id1]+=numberList[id2]

    del vectorsList[id2]
    del numberList[id2]

    return vectorsList, numberList


def HCA_loop(vectorsList,numberList,nbClusters):
    """
    Returns a list composed of nbClusters lists of documents by using the hierarchical cluster analysis
    """

    if nbClusters >= len(vectorsList):
        raise Exception('Impossible')

    else:
        L_def=[]

        while len(vectorsList) > nbClusters:
            vectorsList,numberList=merge_Nearest_Elements(vectorsList,numberList)

        return numberList

if __name__ == '__main__':
    pass

