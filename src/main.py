import DataManagement as dm
import QNAService as qna
import sys

def modelReadData():
	[precedentsWords, prior, likelihood, word2vec, questions, precedents, answerRatio] = dm.readData(printProgress=True)
	return [precedentsWords, prior, likelihood, word2vec, questions, precedents, answerRatio]
	


def qnaStart(precedentsWords, prior, likelihood, word2vec, questions, precedents, answerRatio):
	qna.QNAService(precedentsWords, prior, likelihood, word2vec, questions, precedents, answerRatio, printProgress=True)


def main():
	[precedentsWords, prior, likelihood, word2vec, questions, precedents, answerRatio] = dm.readData(printProgress=True)
	qnaStart(precedentsWords, prior, likelihood, word2vec, questions, precedents, answerRatio)

main()