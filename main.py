import imageio
from pathlib import Path
import re
import random
from wordcloud import WordCloud

"""
Script dedicated to search words in .text file by regex formula and make a .png Word Cloud shaped by a .png file.

"""


def load_shape(url):
    if not url.endswith('.png'):
        raise ValueError('Input only .png files.')
    shape = imageio.imread(url)
    return shape


def load_text(r_url, l_sep, r_sep, force_sticking=True):
    """
    Function to load text file and make a list of WordCloud words.

    :param r_url: input str value leading to text file
    :param l_sep: input str value for left regex pattern
    :param r_sep: input str value for right regex pattern
    :param force_sticking=True
        input text consisting only of short acronyms should stay consistent
        can avoid by changing :param force_sticking=False
    :return: list value for randomize_text function or join function
    """

    if not r_url.endswith('.txt'):
        raise ValueError('Input only .txt files.')
    if not isinstance(l_sep, str) and not isinstance(r_sep, str):
        raise ValueError('Regex wrapper error, check separators.')
    l_text = Path(r_url).read_text()
    l_text = re.findall(rf'{l_sep}(.*){r_sep}', l_text)

    if len(max(l_text)) <= 5 and force_sticking is True:
        l_text = [x.replace(' ', '_') for x in l_text]
    return l_text


def randomize_text(l_text, value):
    if not isinstance(l_text, list):
        raise TypeError('Invalid output from the preceding function.')
    if not isinstance(value, int) and not value > 0:
        raise ValueError('Invalid value of range of randomness.')
    f_text = [(item + ' ') * random.randint(1, value - 1) for item in l_text]
    f_text = ''.join([item for item in f_text])
    return f_text


mask_image = load_shape('electric-guitar-silhouette.png')
text = load_text(r'text.txt', 'â€ž', 'â€ť')
text = randomize_text(text, 15)


word_cloud = WordCloud(width=1024, height=1024, colormap='RdYlBu',
                       normalize_plurals=False, collocations=False,
                       mask=mask_image, background_color='grey').generate(text).to_file('Handyman.png')
