import requests
import pprint
import re
import bs4
import requests

if __name__ == "__main__":
    ## Определяем список ключевых слов:
    KEYWORDS = ['дизайн', 'фото', 'web', 'python']
    regex = "|".join(KEYWORDS)
    response = requests.get('https://habr.com/ru/articles/')
    soup = bs4.BeautifulSoup(response.text, features='lxml')
    articles_list = soup.find_all('article', class_='tm-articles-list__item')
    print(len(articles_list),
          ' статей')
    parsed_list = []
    parsed_data = []

    for article in articles_list:

        link = 'https://habr.com' + article.select_one('a.tm-title__link')['href']
        article_response = requests.get(link)
        article_soup = bs4.BeautifulSoup(article_response.text, features='lxml')
        header = article_soup.select_one('h1').text
        time = article_soup.select_one('time')['datetime']
        text = article_soup.select_one('div.article-formatted-body').text
        res_find = []
        matches = re.finditer(regex, text, re.IGNORECASE)

        for matchNum, match in enumerate(matches, start=1):

            res_find.append(
                "Match {matchNum} was found at {start}-{end}: {match}".format(matchNum=matchNum, start=match.start(),
                                                                              end=match.end(), match=match.group()))

            for groupNum in range(0, len(match.groups())):
                groupNum = groupNum + 1

                res_find.append("Group {groupNum} found at {start}-{end}: {group}".format(groupNum=groupNum,
                                                                                          start=match.start(groupNum),
                                                                                          end=match.end(groupNum),
                                                                                          group=match.group(groupNum)))

        if (re.search(regex, text)):
            parsed_data.append({
                'title': header,
                'link': link,
                'time': time,
                'finded': res_find
            })
            # print(res_find)

            # 'span.tm-publication-hub__link-container')
    pprint.pprint(parsed_data)
