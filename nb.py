import csv
import itertools
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import BernoulliNB
from sklearn.preprocessing import LabelEncoder
from sklearn import cross_validation

class NYTClassifier(object):

  def __init__(self, stopwords_file, articles):
    with open(stopwords_file) as f:
      self.stopwords = [x.strip() for x in f]

    with open(articles) as f:
      reader = csv.reader(f, delimiter = '\t')
      bodies = []
      labels = []
      self.urls = []
      for url, title, body, section in reader:
        self.urls.append(url)
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
          stop_words = self.stopwords,
          binary=True
        )
    self.features = self.cv.fit_transform(bodies)

  def train(self):
    self.clf = BernoulliNB()
    self.clf.fit(self.features, self.labels)

  def predict(self, text):
    return self.le.inverse_transform(self.clf.predict(self.cv.transform(text)))

  def evaluate(self):
    return cross_validation.cross_val_score(self.clf, self.features, self.labels, cv=2, scoring='f1')

  def hard_to_predict(self):
    log_probs = self.clf.predict_log_proba(self.features)
    min_prob_diffs = [min([abs(a-b) for a,b in itertools.combinations(x, 2)]) for x in log_probs]
    joined = dict(zip(self.urls, min_prob_diffs))
    return sorted(joined, key = joined.get)[:10]