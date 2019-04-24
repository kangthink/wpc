"""wpc module

    wpc stands for word pronunciation file collector.
    This module is for download mp3 files from Dictionary site given words.

    example:
        $ python wpc.py

    How it works:
        1. Read words.txt file from root directory.
        2. Download mp3 files from Naver Dictionary.
        3. Add words to no_link.txt file if it fails to download files whatever reason.

"""
import os
import re
import requests 
from bs4 import BeautifulSoup

class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class NoLinkError(Error):
    """Exception raised for no pronunciation file link exist"""
    def __init__(self, msg):
        self.msg = msg
    
    def __str__(self):
        return self.msg


def audioFileURL(word: str) -> str: 
    """Return a link at Naver Dictionary given word
    
    Args:
        word: A str value to search
    Raises:
        NoLinkError: If no mp3 link is found.
    Returns:
        A mp3 link to download.
    """
    url = "%s%s" % ("https://endic.naver.com/search.nhn?sLn=kr&query=",word)
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    try:
        pron_element = soup.find_all('dt', {'class': 'first'})[0]
        anchor_elements = pron_element.find_all('a', {'class': '_soundPlay'})
    
    except IndexError:
        # 네이버 사전 검색 결과가 없을 때.
        raise NoLinkError("Cannot find the word")

    else:
        try:
            us_pron_element = anchor_elements[0]
            link = us_pron_element.attrs['playlist']
            return link

        except KeyError:
            # 검색 결과는 있으나 미국식 발음 파일 링크가 없을 때.
            # 주로 tts로 대신 제공하는 경우 링크가 없음.
            try:
                uk_pron_element = anchor_elements[1]
                link = uk_pron_element.attrs['playlist']
                return link 

            except:
                # 영어식 발음과 영국식 발음 모두 파일이 존재하지 않을 때.
                raise NoLinkError("Cannot find the pronunciation file link")


def downloadFile(link, word):
    """Download mp3 file given link, using a given word as a fileName"""
    # Create directory for downloaded files
    dirName = 'downloaded'
    os.makedirs('./%s' % dirName, exist_ok=True)

    result = requests.get(link)

    # Create path to save
    # e.g. ./downloaded/apple.mp3
    file_name = word + '.mp3'
    full_path = '%s/%s' % (dirName, file_name)

    with open(full_path, 'wb') as f:
        f.write(result.content)


if __name__ == '__main__':

    source_file = 'words.txt'
    no_link_file = 'no_link.txt'

    with open(source_file, 'r') as f:
        
        with open(no_link_file, 'a') as nlf:

            for line in f.readlines():
                word = re.findall(r"\S+", line)[0]
                print('start download ',word)

                try:
                    downloadFile(audioFileURL(word), word)
                except NoLinkError as a:
                    print(a, word)
                    nlf.write(word)
                    nlf.write('\n')

                except:
                    print('exception')
                    print(word)
                    nlf.write(word)
                    nlf.write('\n')

    
