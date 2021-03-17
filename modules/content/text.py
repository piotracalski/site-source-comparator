import requests
import re

from functools import reduce


def get_text_content(markup):

  # delete tags
  for script in markup(["script", "style"]):
    script.decompose()

  # form list of text content
  strips = list(markup.stripped_strings)

  # remove unnecesary spaces if present
  strips_cleared = list(map(lambda stripe: re.sub(re.compile(r'[\s]{2,}'), ' ', stripe), strips))
  
  # split into separate words 
  strips_divided = list(map(lambda stripe: stripe.split(' '), strips_cleared))

  # return sum of all stripes
  return reduce(lambda x,y: x + y, strips_divided)


def compare_text_content(object):
  
  # get content of both pages
  before_text = get_text_content(object.before_markup)
  after_text = get_text_content(object.after_markup)
  
  # declariation of differences-related variables
  missing_words = list()
  excess_words = list()
  # separator = ', '

  for word in before_text:
    if word in after_text:
      after_text.remove(word)
    elif word != '':
      missing_words.append(word)
  
  # calculate excess words
  excess_words = after_text

  # calculate percentage difference
  difference = round((len(missing_words) + len(excess_words)) * 100 / len(before_text), 1)  
  
  return {
    "difference": difference,
    # below keys are not being used at this moment but probably will be used in the future as they carry valuable information
    # "missing_words": f'{separator.join(missing_words)}',
    # "excess_words": f'{separator.join(excess_words)}
  }
