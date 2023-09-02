import requests
from bs4 import BeautifulSoup
import re
import string
import multiprocessing
import syllables

def scrapeSentences(URL):
  page = requests.get(URL)
  soup = BeautifulSoup(page.content,'html.parser')
  content = soup.find_all("p")
  combinedText = ""
  for t in content:
      combinedText += t.get_text()
  sentences = combinedText.split('.')
  return sentences

def hasDigit(word):
  for c in word:
    if(c.isdigit()):
      return False
  return True

# score based on Gunning Log formula
#Grade level= 0.4 * ( (average sentence length) + (percentage of Hard Words) )
#Here, Hard Words = words with more than two syllables.
def readability(sentences):
  hard_words = 0
  total_words = 0
  sentence_count = 0
  for sentence in sentences:
    sentence_count += 1
    words = sentence.split()
    for w in words:
      total_words += 1
      if(syllables.estimate(w) >= 2):
        hard_words += 1
  percent_hard_words = hard_words/total_words
  avg_sentence_length = total_words/sentence_count
  score = 0.4*(percent_hard_words + avg_sentence_length)
  return score

def scrape(URL):
  page = requests.get(URL)
  soup = BeautifulSoup(page.content,'html.parser')
  content = soup.find_all("p")
  dict = {}
  for t in content:
      text = t.get_text()
      text = text.strip().lower()
      new_text = re.sub(r'[^\w\s]', '', text)
      new_text = ''.join(i for i in new_text if not i.isdigit())
      list = new_text.split()
      for i in range(len(list)):
          try:
            dict[list[i]] += 1
          except:
            dict[list[i]] = 1
  return dict

def webscrape(url):
    print("webscraping", url)
    sample = scrape(url)
    if not sample:
        return [[], [], [], [], []]
    sample = [[k, v] for k, v in sample.items()]  # convert dictionary into a sortable list
    #sample = sorted(sample, key=lambda x: x[0])  # sorted alphabetically
    # sample = sorted(sample, key=lambda x: x[0])[::-1] #sorted alphabetically in reverse
    # sample = sorted(sample, key=lambda x: x[1]) #sorted based on most used(least to greatest)
    sample = sorted(sample, key=lambda x: len(x[0]))[::-1] #sorted by word length
    average = 0
    size = 0
    biggest = ""
    common = ["", 0]
    for k, v in sample:
        #print(k, ":", v)
        average += len(k)*v
        size += v
        if v > common[1]:
            common = [k, v]
        if len(k) > len(biggest):
            biggest = k
    print("")
    print("Average Word Size:", average/size)
    print("Longest Word: ", biggest)
    print("Number of Words: ", size)
    print("Readability: ", readability(scrapeSentences(url)))
    temp = [sample, round(average/size,2), biggest, size, round(readability(scrapeSentences(url)),2)]
    return temp
  
def timeoutscrape():
    pass