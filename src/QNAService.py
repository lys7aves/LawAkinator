#import pandas as pd
import copy
import numpy as np
import sys

# word2vec을 이용하여 판례와 단어 사이 유사도 측정.
def precedentWordSimilarity(precedent, word, word2vec):
	maxi = 0
	for pword in precedent:
		try:
			similarity = word2vec.similarity(pword, word)
		except KeyError:
			similarity = 0
		maxi = max(maxi, similarity)
	return maxi

# word2vec을 이용하여 모든 판례에 대한 주어진 단어의 유사도 측정.
def calculatePrecedentSimilarity(word, precedentWord, word2vec):
	similaritys = []
	for precedent in precedentWord:
		similaritys.append(precedentWordSimilarity(precedent, word, word2vec))
	
	return similaritys

# P list에서 누적합이 R이 되는 애들 반환.
def highRatioPrecedents(P, R):
	sortedIdx = sorted(range(len(P)), key=lambda i:P[i], reverse=True)

	idx = []
	for i in range(len(P)):
		idx.append(sortedIdx[i])
		R = R-P[sortedIdx[i]]

		if R <= 0:
			break
	
	return idx

# 질문 선별 함수.
def selectQuestion(P, likelihood, q_num):
	precedentIdcs = highRatioPrecedents(P, 0.9)	# 판례 인덱스
	num_question = len(likelihood[0])
	# print('number of 90% precedents :', len(precedentIdcs))
	# print(precedentIdcs[:15])
	P_ = []
	for idx in precedentIdcs[:15]:
		P_.append(P[idx])
	# print(P_)

	lower=0.4
	upper=0.6

	x = [0] * num_question
	y = [0] * num_question

	for i in precedentIdcs:
		for j in range(num_question):
			if likelihood[i][j] >= upper:
				x[j] = x[j] + 1
			if likelihood[i][j] <= lower:
				y[j] = y[j] + 1

	points = []
	for i in range(num_question):
		try:
			point = ((x[i]+y[i])/len(precedentIdcs)) * (min(x[i],y[i])/max(x[i],y[i]))
		except ZeroDivisionError:
			point = 0
		points.append(point)

	# 인덱스들을 점수순으로 정렬
	idcs = sorted(range(num_question), key=lambda i:points[i], reverse=True)

	# print('** question info **')
	# for i in range(10):
		# print(idcs[i], x[idcs[i]], y[idcs[i]], points[idcs[i]])
	
	badWords = [10, 140, 276, 69, 1093, 446, 5, 1222, 754]
	# 과거에 질문한 질문 제거
	for i in range(num_question):
		flag = True
		for q in q_num:
			if idcs[i] == q:
				flag = False

		for badWord in badWords:
			if idcs[i] == badWord:
				flag = False

		if flag:
			# print(idcs[i])
			return idcs[i]

# 확률 계산 함수.
def calculateProbability(P, question, answer, likelihood, answerRatio):
#	similaritys = calculatePrecedentSimilarity(question, precedentWord, word2vec)
	similaritys = []
	for lh in likelihood:
		similaritys.append(lh[question])

	ratio = answerRatio[answer]
	for i in range(len(P)):
		similarity = [similaritys[i], 0, 0, 0, 1-similaritys[i]]

		R = 0
		for j in range(len(similarity)):
			R = R + similarity[j] * ratio[j]
		
		P[i] = P[i] * R
	
	sum = 0
	for p in P:
		sum = sum + p
	
	for i in range(len(P)):
		P[i] = P[i] / sum
	
# 질문 종료 시점 반환 함수.
def QNAEnd(P, step):
	idx = highRatioPrecedents(P, 0.7)

	if len(idx) <= 5:
		return True
	elif step >= 15:
		return True
	else:
		return False

# 질문 예측 함수.
def predictPrecedents(P):
	idx = highRatioPrecedents(P, 1)

	return idx[:5]

# 결과를 바탕으로 학습하는 함수.
def learnResult(q_num, answer, predict, result, prior):
	# 준비중
	return

# 서비스 종료 시점 반환 함수.
def serviceEnd():
	return True

# QNA Servvice.
def QNAService(precedentWord, prior, likelihood, word2vec, questions, precedents, answerRatio, printProgress=False):
	P = copy.deepcopy(prior)

	step = 0
	q_num = []	# 질문 번호 list
	answer = []	# 답변 list
	while True:
		while True:
			# print('#', step)
			sys.stdout.flush()

			q_num.append(selectQuestion(P, likelihood, q_num))	# 질문 선택
			print(questions[q_num[step]] + '과 관련이 있습니까?')
			sys.stdout.flush()
			ans = int(input())
			answer.append(ans)	# 답변 입력

			calculateProbability(P, q_num[step], answer[step], likelihood, answerRatio)	# 확률 계산
#			print(P)

			if QNAEnd(P, step):	# 질문을 끝내도 되는지 확인(?)
				break

			step = step + 1
		print("fin")
		sys.stdout.flush()

		predict = predictPrecedents(P)	# 판례 예측
		for idx in predict:
			print(precedents[idx])

		# result = int(input('0:Correct, 1:Noncorrect'))	# 예측이 맞는지 사용자에게 물어보고
		# learnResult(q_num, answer, predict, result, prior)	# 답변을 토대로 재학습

		if serviceEnd():
			break
		# 끝낼 때도 조건이 필요할 듯
		# 예측을 맞추면 바로 끝내면 되겠지만,
		# 못 맞추면 시스템을 계속 사용할지 물어보기도 하고
		# 계속 못 맞추면 사용자가 생각한 정답(판례)이 뭔지 입력할 수 있도록도 만들어야 할 듯
		#	이건 나중에 우리가 수작업으로 학습시킬 때도 용의할 뜻
		#	하나의 판례를 상황으로 가정하고 질문에 대해 답하다 해당 판례가 나오면 맞다고 말하고
		#	계속 못 맞추면 이 판례가 정답이다라고 학습시키는 등...



def request_question(likelihood,prior,questions,q_num = []	): # q_num : 질문 번호 list | answer : 답변 list
	step = len(q_num)
	P = copy.deepcopy(prior)
	q_num.append(selectQuestion(P, likelihood, q_num))	# 질문 선택
	return questions[q_num[step]],q_num


def receive_answer(answer, P, q_num, prior,questions, likelihood, answerRatio, precedents):
	step = len(q_num)
	calculateProbability(P, q_num[step], answer[step], likelihood, answerRatio)	# 확률 계산
	isEnd = False
	if QNAEnd(P, step):	# 질문을 끝내도 되는지 확인(?)
		isEnd = True
		predict = predictPrecedents(P)	# 판례 예측
		results =[]
		for idx in predict:
			results.append(precedents[idx])
		
		# result = int(input('0:Correct, 1:Noncorrect'))	# 예측이 맞는지 사용자에게 물어보고
		# learnResult(q_num, answer, predict, result, prior)	# 답변을 토대로 재학습
		return isEnd,results

	else :
		question = request_question(likelihood,prior,questions,q_num)
		return isEnd,question