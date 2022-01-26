from gensim.models import KeyedVectors
import pandas as pd
import ast
import numpy as np
import csv
import sys

# 상담 데이터 csv에 나오는 list형태 문자열을 진짜 list로 변환해 주는 함수
def csvToList(string):
	return ast.literal_eval(string)

# 2차원 리스트를 csv에 쓰기. 
def writeDoubleCSV(filename,listdata):
	with open(filename,"w",encoding='utf-8') as file:
		writer = csv.writer(file)
		for data in listdata:
			writer.writerow(data)

# 1차원 리스트를 csv에 쓰기. 
def writeCSV(filename,listdata):
	with open(filename,"w",encoding='utf-8') as file:
		writer = csv.writer(file)
		writer.writerow(listdata)

# 2차원 리스트를 csv에서 읽기. 
def readDoubleCSV(filename):
	doublelist = []
	with open(filename,"r",encoding='utf-8') as file:
		listdata = csv.reader(file)
		for data in listdata:
			try: # 전체가 float이 아니면 탈출. 
				for i in range(len(data)):
					data[i] = float(data[i])
			except:
				pass
			doublelist.append(data)
	return doublelist

# 1차원 리스트를 csv에서 읽기. 
def readCSV(filename):
	with open(filename,"r",encoding='utf-8') as file:
		listdata = csv.reader(file)
		for data in listdata:
			try: # 전체가 float이 아니면 탈출.
				for i in range(len(data)):
					data[i] = float(data[i])
			except: # 만약 하나라도 float이 아니면,
				pass
			return data
	
# word2vec 읽기.
def readWord2vec(fileName):
	word2vec = KeyedVectors.load_word2vec_format(fileName)
	return word2vec

# 모든 데이터 읽기.
def readData(printProgress=False):
	dataDir = './data/'

	if printProgress:
		# print('Start to read data')
		sys.stdout.flush()

	precedentWord = readDoubleCSV(dataDir + 'precedentWord.csv')	# 판례 관련 단어 2중 리스트
	prior = readCSV(dataDir + 'precedentAppearance.csv')	# 사전 확률
	likelihoodTable = readDoubleCSV(dataDir + 'likelihoodTable.csv')	# 우도
	word2vec = readWord2vec(dataDir + 'word2vec')	# word2vec
	questions = readCSV(dataDir + 'questionWord.csv')	#질문
	precedents = readCSV(dataDir + 'precedentList.csv')	# 판례
	answerRatio = readDoubleCSV(dataDir + 'answerRatio.csv')	# answerRatio

	if printProgress:
		# print('End to read data')
		sys.stdout.flush()

	return [precedentWord, prior, likelihoodTable, word2vec, questions, precedents, answerRatio]