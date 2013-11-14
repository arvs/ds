import csv
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import BernoulliNB
from sklearn.preprocessing import LabelEncoder

class NYTClassifier(object):

  def __init__(self, stopwords_file, articles):
    with open(stopwords_file) as f:
      self.stopwords = [x.strip() for x in f]

    with open(articles) as f:
      reader = csv.reader(f, delimiter = '\t')
      bodies = []
      labels = []
      for url, title, body, section in reader:
        bodies.append(body)
        labels.append(section)
      self.le = LabelEncoder()
      self.le.fit(labels)
      self.labels = self.le.transform(labels)

    self.cv = CountVectorizer(
          input='content', 
          decode_error = 'replace',
          strip_accents = 'unicode',
          ngram_range=(1,1),
          analyzer = 'word',
          stop_words = stopwords,
          binary=True
        )
    self.features = self.cv.fit_transform(bodies)

  def train(self):
    self.clf = BernoulliNB()
    self.clf.fit(self.features, self.labels)

  def predict(self, text):
    return self.le.inverse_transform(self.clf.predict(self.cv.transform(text)))
    