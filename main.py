import csv
import xml.dom.minidom as minidom


DATASET_PATH = "books-en.csv"
TXT_PATH = "20_books.txt"
XML_PATH = "currency.xml"

ISBN = 0
TITLE = 1
AUTHOR = 2
YEAR = 3
PUBLISHER = 4
DOWNLOADS = 5
PRICE = 6


def get_n_line(dataset, number):
    line = ""
    dataset.seek(0)
    for i in range(number):
        line = next(dataset)
    return line


def str_to_list(string=""):
    ans = string
    ans = ans.replace("&amp;", "&")
    ans = ans.replace("&lt;", "<")
    ans = ans.replace(" ; ", "#@!_lr")
    ans = ans.replace(" ;", "#@!_left")
    ans = ans.replace("; ", "#@!_right")
    ans = ans.split(';')
    for item in ans:
        item = item.replace("#@!_lr", " ; ")
        item = item.replace("#@!_left", " ;")
        item = item.replace("#@!_right", "; ")
        # можно еще убрать \n в поле Цена
    return ans


# def opechatki_finder():
#         while True:
#             number_of_line += 1
#             title = next(dataset)
#             title = str_to_list(title)
#             if len(title) != 7:
#                 print(number_of_line, title)
#                 print(len(title))


def count_headers_longer_30_sym(dataset):
    ans = 0
    line = get_n_line(dataset, 2)
    while line != "END_OF_DOC":
        listed = str_to_list(line)
        if len(listed[1]) > 30:
            ans += 1
        line = next(dataset, "END_OF_DOC")
    print(ans)


def author_finder_ver7(dataset, author_name, year_from, year_to):
    dataset.seek(0)
    line = next(dataset)
    while line != "END_OF_DOC":
        listed = str_to_list(line)
        if listed[2].find(author_name) != -1:
            # условие варианта 7
            if int(listed[3]) >= year_from and int(listed[3]) <= year_to:
                print(listed[0], listed[1])
                # ничего не напишет (наверное), так как вообще книг таких годов нет
                # books-en имел неточности, которые я убрал (например John Peterman в поле Год),
                # так что прошу сравнивать с файлом в репозитории
        line = next(dataset, "END_OF_DOC")
    print_solid_line()


def generator(dataset):
    with open(TXT_PATH, 'w') as txt_file:
        to_the_txt = ""
        line = get_n_line(dataset, 4851)
        for i in range(20):
            listed = str_to_list(line)
            to_the_txt += (
                f"{4851 + i}: {listed[2]}. {listed[1]} - {listed[3]}\n")
            line = next(dataset)
        txt_file.write(to_the_txt)


def xml():
    with open(XML_PATH, "r", encoding="UTF-8") as xml_file:
        xml_data = xml_file.read()

        dom = minidom.parseString(xml_data)
        dom.normalize()

        elements = dom.getElementsByTagName('Valute')
        list_of_charCodes = []

        for node in elements:
            CharCode = ""
            for child in node.childNodes:
                if child.nodeType == 1:
                    if child.tagName == 'CharCode':
                        if child.firstChild.nodeType == 3:
                            CharCode = str(child.firstChild.data)
                    if child.tagName == 'Nominal':
                        if child.firstChild.nodeType == 3:
                            Nom = int(child.firstChild.data)
                            if Nom == 100 or Nom == 10:
                                list_of_charCodes.append(CharCode)
        print(list_of_charCodes)
    print_solid_line()


def create_list(count, default_value):
    created_list = []
    for i in range(count):
        created_list.append(default_value)
    return created_list


def add_into_list(cur_list=list, value=list):
    ans_list = cur_list
    for i in range(len(ans_list)):
        if int(ans_list[i][0]) <= int(value[0]):
            ans_list.insert(i, value)
            ans_list.pop()
        break
    return ans_list


def most_popular_20_books(dataset):
    ans = create_list(20, [-1, ""])
    line = get_n_line(dataset, 2)
    while line != "END_OF_DOC":
        listed = str_to_list(line)
        ans = add_into_list(ans, [listed[DOWNLOADS], listed[TITLE]])
        line = next(dataset, "END_OF_DOC")

    for item in ans:
        print(item[1] + " (Downloads: " + str(item[0]) + ")")
    print_solid_line()


def print_solid_line():
    print("####################################################")


def list_of_pushishers(dataset):
    line = get_n_line(dataset, 1)
    line = next(dataset, "END_OF_DOC")
    set_of_publishers = set()
    while line != "END_OF_DOC":
        set_of_publishers.add(str_to_list(line)[PUBLISHER])
        line = next(dataset, "END_OF_DOC")
    ans = list(set_of_publishers)
    ans.sort()
    print(ans)
    same_item_checker(ans)


def same_item_checker(cur_list=list):
    if len(cur_list) == 1:
        print("Nice!")
    for i in range(len(cur_list) - 1):
        if cur_list[i] == cur_list[i + 1]:
            print("INTRUDER ALERT!!! RED SPY IS IN THE BASE!!!")


if __name__ == "__main__":
    with open(DATASET_PATH, encoding="Latin-1") as dataset:

        count_headers_longer_30_sym(dataset)
        author_finder_ver7(dataset, " ", 2016, 2018)
        generator(dataset)
        xml()
        most_popular_20_books(dataset)
        list_of_pushishers(dataset)
