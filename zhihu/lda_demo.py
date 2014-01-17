from gensim import corpora, models, similarities
from zhihu_config import *

question_corpus = corpora.BleiCorpus('./zhihu_dat/item.dat')

def build_lda_mode():
    # corpus is bag of words, which is the original feature
    corpus = corpora.BleiCorpus('./zhihu_dat/item.dat') # the bag of words feature of question data

    # build up lda model: using lda model, given a bag of words feature, return the topic feature, so the topic model is to reduce the dimension of the features of  a document
    lda_model = models.LdaModel(corpus, id2word = dictionary, num_topics = 10)

    # save the model to disk for future use(Given a document such as question, return the topic feature of the document)

    lda_model.save('./zhihu_dat/zhihu_10.lda')
    print 'Building complete'

def test_model():
    '''
    after setting the lda model, test the model
    '''
    lda_model = models.LdaModel.load('./zhihu_dat/zhihu_10.lda')

    # transform the question_corpus into lda space, print the lda feature
    question_lda = lda_model[question_corpus]
    for doc in question_lda:
        print doc


if __name__ == '__main__':
    # print 'build lda model of 10 topics'
    # build_lda_mode()

    test_model()
