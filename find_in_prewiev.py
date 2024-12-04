import requests
import pprint
import re
import requests
import bs4
from fake_headers import Headers

if __name__ == "__main__":
    ## Определяем список ключевых слов:
    KEYWORDS = ['дизайн', 'фото', 'web', 'python']
    regex = "|".join(KEYWORDS)
    response = requests.get('https://habr.com/ru/articles/', headers=Headers(browser='chrome', os='mac').generate())
    soup = bs4.BeautifulSoup(response.text, features='lxml')
    articles = soup.find_all(class_='tm-articles-list__item')
    parsed_list = []
    parsed_data = []
    res_find = []

    for article in articles:
        pars_text = article.select_one('div.article-formatted-body')
        pars_text = str(pars_text.select_one('p'))
        parsed_list.append(pars_text)
        # print(pars_text)

        header = article.select_one('a.tm-title__link')
        header = header.select_one('span')
        time = article.select_one('time')['datetime']

        matches = re.finditer(regex, pars_text, re.MULTILINE)

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

        if (re.search(regex, pars_text)):
            parsed_data.append({
                'title': header,
                'time': time,
                'finded': res_find
            })

    if len(parsed_data):
        pprint.pprint(parsed_data)
    else:
        print("ничего не найдено в превьювах")
