from __future__ import print_function
import requests
import sys
import codecs
import json
from time import sleep
from argparse import ArgumentParser

class NYT(object):

  api_key = "067a512751c8adef7b5fd5ca3dffd5b9:6:53584770"
  base_url = "http://api.nytimes.com/svc/search/v1/article"

  @classmethod
  def articles_for_section(cls, sections = [], num_results = 10, outfile = sys.stdout):
    processed_urls = set()
    for s in sections:
      num_processed = 0
      i = 0
      while num_processed < num_results:
        payload = {
          'format' : 'json',
          'query' : 'nytd_section_facet:[%s]' % s,
          'rank' : 'newest',
          'offset' : i,
          'api-key' : cls.api_key
        }
        r = requests.get(cls.base_url, params=payload)
        try:
          req = json.loads(r.content)
          results = filter(lambda x: all([a in x for a in ('url','title','body')]) and x['url'] not in processed_urls, req['results']) #filter garbage and nonunique
          if len(results) + num_processed >= num_results:
            # last page
            results = results[:num_results - num_processed]
          num_processed += len(results)
          for res in results:
            processed_urls.add(res['url'])
            print(u"%s\t%s\t%s\t%s" % (res['url'], res['title'], res['body'], s), file = outfile)
          # rate limiting
          sleep(0.2)
          i += 1
        except ValueError:
          print("Failed on section %s after processing %d" % (s, num_processed), file=sys.stderr)

if __name__ == '__main__':
  parser = ArgumentParser()
  parser.add_argument('--all', action = 'store_true')
  parser.add_argument('--sections', '-s', nargs = '*')
  parser.add_argument('--num_results', '-n', type = int)
  parser.add_argument('--outfile', '-o')
  args = parser.parse_args()
  sections = ["Sports", "Arts", "Business", "Obituaries","Sports", "World"] if args.all else args.sections
  num_results = args.num_results if args.num_results else 10
  f = codecs.open(args.outfile, 'w', 'utf-8') if args.outfile else sys.stdout
  NYT.articles_for_section(sections, num_results, f)