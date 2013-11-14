#!/usr/bin/env python

import sys

class SumReducer(object):

  def __init__(self):
    self.current_word = None
    self.word_count = 0

  def process(self, line):

    # Split input to key and value.
    word, count = line.split('\t')

    if not self.current_word:
      self.current_word = word
      self.word_count = int(count)
    elif self.current_word != word:
      print self.__repr__()
      self.current_word = word
      self.word_count = int(count)
    else:
      self.word_count += int(count)

  def __repr__(self):
    return "%s\t%d" % (self.current_word, self.word_count)

if __name__ == '__main__':
  reducer = SumReducer()
  for line in sys.stdin:
    reducer.process(line)

  print reducer