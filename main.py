import requests, json, threading
import sqlalchemy
from sqlalchemy.orm import Session
from models.Tables import *

URL = r"https://swapi.dev/api/"
URL_CATEGORY = ["people/", "planets/", "species/", "starships/", "vehicles/", "films/"]

people_full = []
planets_full = []
films_full = []
species_full = []
vehicles_full = []
starships_full = []
res_list = [people_full, planets_full, species_full, starships_full, vehicles_full, films_full]
db_tables = [People, Planets, Species, Starships, Vehicles, Films]

engine = sqlalchemy.create_engine("sqlite:///star_wars.db")
connection = engine.connect()
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
session = Session(engine)

# функция с запросами
def get_data(url, results:list):
    response = requests.get(url)
    if response.status_code != 200:
        return
    
    res = json.loads(response.text)
    results.extend(res['results'])       

    if res['next'] != None:
        get_data(res['next'], results)

# функция для создания и запуска потоков на запросы (чтоб быстрее)
def request_threads():
    threads = []

    for category, res in list(zip(URL_CATEGORY, res_list)):
        th = threading.Thread(target=get_data, args=(URL+category, res))
        threads.append(th)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

# функция для получения только номера из url (нужна для некоторых данных)
def get_key_from_url(url:str):
        temp = url.split('/')
        return int(temp.pop((len(temp)-2)))

# функция для заполнения основных таблиц данными
def fill_main_tables(table, data_lt):
    with session as db:
        for el in data_lt:
            _temp = table()
            for i in el:
                # для данных людей специальное условие, т.к. строение у этих данных отличается
                if data_lt == people_full:
                    if i == 'films':
                        continue
                    if i == 'species':
                        if not el[i]:
                            el[i] = None
                        else:
                            el[i] = get_key_from_url(el[i][0])
                
                # если это url - достать только номер (это будет id)
                if el[i] is not None and isinstance(el[i], str) and 'https' in el[i]:
                    el[i] = get_key_from_url(el[i])
                
                # если список, прервать цикл (списки идут в промежуточные таблицы)
                if not isinstance(el[i], list):
                    _temp.__setattr__(i, el[i])
                    db.add(_temp)
                    db.commit()
                else:
                    break

# функция для заполнения промежуточных таблиц (для связи многие ко многим)
def fill_assosiation_tables(list_full, category, list_ref, Parent, Child, parent_attr):
    with session as db:
        for i in range(len(list_full)):
            temp = list_full[i][category]

            # просто извлекать номер из url не получится, т.к. номера starships и vehicles идут не по порядку, поэтому сравниваются url
            for url in temp:
                for el in list_ref:
                    if el['url'] == url:
                        temp_indx = list_ref.index(el) + 1
                        break

                q1 = db.query(Parent).filter(Parent.id==i+1).one()

                subq = db.query(Child).filter(Child.id == temp_indx).one()
                res = q1.__getattribute__(parent_attr)
                res.append(subq)
                db.commit()

# функция для поиска и вывода заданных данных (1 - люди с голубыми глазами; 2 - трое самых высоких; 3 - все люди выше 170см)
def output():
    with session as db:
        print('1--------------------')
        res = db.query(People).filter(People.eye_color == 'blue').all()
        for el in res:
            print(el.name)

        print('2--------------------')
        res = db.query(People).filter(People.height).order_by(People.height.desc()).limit(3).all()
        for el in res:
            print(el.name, ' - ', el.height)

        # unknown?
        print('3--------------------')
        res = db.query(People).filter(sqlalchemy.or_(People.gender == 'male', People.gender == 'female')).filter(People.height > 170).order_by(People.height.desc()).all()
        for el in res:
            print(el.name, el.gender, el.height, sep=', ')

def main():
    request_threads()

    for table, res in list(zip(db_tables, res_list)):
        fill_main_tables(table, res)

    categories = ['characters', 'planets', 'species', 'starships', 'vehicles']
    sub_tables = ['f_people', 'f_planets', 'f_species', 'f_starships', 'f_vehicles']
    
    for i in range(len(categories)):
        fill_assosiation_tables(films_full, categories[i], res_list[i], Films, db_tables[i], sub_tables[i])

    fill_assosiation_tables(people_full, 'starships', starships_full, People, Starships, 'pp_starships')
    fill_assosiation_tables(people_full, 'vehicles', vehicles_full, People, Vehicles, 'pp_vehicles')
    output()

if __name__ == '__main__':
    main()
    