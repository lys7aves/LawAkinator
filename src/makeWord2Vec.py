from gensim.models import Word2Vec
from gensim.models import KeyedVectors
import pandas as pd
import ast

# ******************** csv에 나오는 list형태 문자열을 진짜 list로 변환하는 함수. ********************
def csvToList(string):
    return ast.literal_eval(string)

def loadWtokenSet(fileName):
    data = pd.read_csv(fileName)
    list_final = [] #최종 2중 리스트.

    for i in range(len(data)):
        list_temp = csvToList(data['reply_token'][i])
        list_final.append(list_temp)

    print(list_final[1])
    return list_final



def makeWord2Vec(wtokenSet):
    '''
    size = 워드 벡터의 특징 값. 즉, 임베딩 된 벡터의 차원.
    window = 컨텍스트 윈도우 크기
    min_count = 단어 최소 빈도 수 제한 (빈도가 적은 단어들은 학습하지 않는다.)
    workers = 학습을 위한 프로세스 수
    sg = 0은 CBOW, 1은 Skip-gram.
    '''

    word2vec = Word2Vec(wtokenSet, size=100, window=5, min_count=0, workers=4, sg=0)

    return word2vec

def saveWord2vec(word2Vec, fileName):
    word2Vec.wv.save_word2vec_format(fileName)

def loadWord2vec(fileName):
    word2vec = KeyedVectors.load_word2vec_format(fileName)
    return word2vec

def main():
    '''
    fileName = 'C:/Users/TG/Desktop/CCP/Modeling/data/re_token.csv'
    wtokenSet = loadWtokenSet(fileName) # 이게 문장 리스트

    fileName = 'C:/Users/TG/Desktop/CCP/Modeling/data/word2vec'
    word2vec = makeWord2Vec(wtokenSet)

    saveWord2vec(word2vec, fileName)
    '''
    
    fileName = 'C:/Users/TG/Desktop/CCP/Modeling/data/word2vec'
    word2vec = loadWord2vec(fileName)

    print(word2vec.most_similar(positive=['회사']))
    print(word2vec.most_similar(positive=['토지']))

    wordList = ['사망', '토지', '회사', '입사']
    for w1 in wordList:
        for w2 in wordList:
            print(w1, w2, word2vec.similarity(w1, w2))





main()