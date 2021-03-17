import time
import requests
import csv
import os

from bs4 import BeautifulSoup
from dotenv import load_dotenv

from modules.content import text
from modules.content import images
from modules import page_info

time_start = time.time()

load_dotenv()

INPUT_DATA_PATH = os.getenv("INPUT_DATA_PATH", "input/input_data.csv")
OUTPUT_DATA_PATH = os.getenv("OUTPUT_DATA_PATH", "output/site_comparison_results.csv")
REQUEST_INTERVAL = int(os.getenv("REQUEST_INTERVAL", 1))


def read_data_from_csv(path):

  print(f'TASK: read data from {path}')
  data = list()
  with open(path) as input_file:
    csv_reader = csv.reader(input_file, delimiter=',')
    for url_pair in csv_reader:
      data.append({
        "before": url_pair[0],
        "after": url_pair[1]
      })
  return data

  
# read url pairs from CSV file
urls = read_data_from_csv(INPUT_DATA_PATH)


def get_markup(url):

  response = requests.get(url)
  status_code = response.status_code
  markup = ''
  if status_code == 200:
    markup = BeautifulSoup(response.text, 'html.parser')

  return {
    "status_code": status_code,
    "markup": markup
  }


def save_data(results):

  print(f'TASK: saving results to {OUTPUT_DATA_PATH}')
  
  with open(OUTPUT_DATA_PATH, 'w', newline='') as results_file:
    wr = csv.writer(results_file, delimiter = ',')
    for url_pair in urls:
      if "errors" in results[urls.index(url_pair)]:
        wr.writerow([
          url_pair["before"],
          url_pair["after"],
          results[urls.index(url_pair)]["errors"]
        ])
      else:
        wr.writerow([
          url_pair["before"],
          url_pair["after"],
          results[urls.index(url_pair)]["TextContent"]["difference"],
          results[urls.index(url_pair)]["ImagesNumber"],
          results[urls.index(url_pair)]["AltAttr"]["missing_alt_attr"],
          results[urls.index(url_pair)]["AltAttr"]["empty_alt_attr"],
          results[urls.index(url_pair)]["PageTitle"]
        ])


class Comparator():

  def __init__(self, before, after):
    self.before_markup = before
    self.after_markup = after
    self.results = dict()

  def accept(self, visitor):
    self.results[visitor.test_name()] = visitor.visit(self)

  def __repr__(self):
    return self.results


class Test():
  def test_name(self):
    return self.__class__.__name__


class TextContent(Test):
  def visit(self, tests):
    return text.compare_text_content(tests)


class ImagesNumber(Test):
  def visit(self, tests):
    return images.compare_number_of_images(tests)


class AltAttr(Test):
  def visit(self, tests):
    return images.check_alt_attr(tests.after_markup)


class PageTitle(Test):
  def visit(self, tests):
    return page_info.compare_page_title(tests)


def main():

  print('TASK: page comparison')

  # define global results
  results = list()

  # iterate over URLs and get differences
  for url_pair in urls:

    print(f'Comparing: {url_pair["before"]} vs {url_pair["after"]}')

    # define URL pair's results
    url_results = dict()

    try:

      # get response for before/after migration URLs requests
      before_url_response = get_markup(url_pair['before'])
      after_url_response = get_markup(url_pair['after'])

    except Exception as e:
      
      # report an error
      url_results["errors"] = f'No results due to a request error: {e}'

    except:
      
      # report an error
      url_results["errors"] = 'No results due to an unidentified error'
      
    else:

      if before_url_response["status_code"] == 200 and after_url_response["status_code"] == 200:

        comparator = Comparator(
          before_url_response["markup"],
          after_url_response["markup"]
        )
        
        contexts = [
          TextContent(),
          ImagesNumber(),
          AltAttr(),
          PageTitle()
        ]

        for context in contexts:
          comparator.accept(context)

        url_results = comparator.results

      else:

        # report status codes other than 200
        url_results["errors"] = f'No results due to status codes: {url_pair["before"]} - {before_url_response["status_code"]}, {url_pair["after"]} - {after_url_response["status_code"]}'

    finally:

      # add URL pair's results to global results
      results.append(url_results)

      # delay between loop iteration to avoid server overload
      time.sleep(REQUEST_INTERVAL)

  # save data to CSV file
  save_data(results)

  time_end = time.time()
  print(f'Execution time: {round(time_end - time_start)}s')
  

if __name__ == "__main__":
  main()