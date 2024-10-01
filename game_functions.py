import random
from geopy import distance
import mysql.connector


connection = mysql.connector.connect(
    host='localhost',
    port=3306,
    database='treasure_chest',
    user='treasure',
    password='chest',
    autocommit=True,
    collation='utf8mb4_general_ci'
)


def get_game_countries(difficulty_level):
    sql = (f'select country_count, airports_in_treasure_land from difficulty '
           f'where level = "{difficulty_level}";')
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    # print(result)
    countries_for_difficulty_level = result[0]
    min_countries_in_treasure_land = int(int(result[1]) / 2)
    # print(f'{countries_for_difficulty_level}, {min_countries_in_treasure_land}')

    #sql = (f'SELECT name FROM country where continent = "EU" '
    #       f'order by rand() limit {countries_for_difficulty_level};')

    sql = (f'select country.name, count(*) from country '
           f'left join airport on airport.iso_country = country.iso_country '
           f'where country.continent = "EU" group by country.iso_country '
           f'having count(*) >= {min_countries_in_treasure_land} '
           f'order by rand() '
           f'limit {countries_for_difficulty_level};')

    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()

    results = []
    for item in result:
        results.append(item[0])
    return results


def get_biggest_airport_size_for_country(country_name):
    sql = (f'select airport.type from airport '
           f'inner join country on airport.iso_country = country.iso_country '
           f'where country.name = "{country_name}" group by type;')

    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()

    size = False

    # muuttaa listan monikoita listaksi
    result = [item[0] for item in result]

    # määrittää maan suurimman lentokentän koon.
    # lentokenttien koot monikossa suuruusjärjestyksessä suurimmasta pienimpään
    for airport_size in ('large_airport', 'medium_airport', 'small_airport', 'heliport'):
        if airport_size in result and not size:
            size = airport_size

    return size


def get_default_airport_for_country(country_name):
    # hae maan suurimman lentokentän koko
    biggest_airport_size = get_biggest_airport_size_for_country(country_name)

    # lopeta jos edellisestä tuli False eli maalla ei ole suurta, keskikokoista tai pientä lentokenttää
    # tai helikopterikenttää
    if not biggest_airport_size:
        return False

    sql = (f'SELECT airport.name from airport '
           f'inner join country on airport.iso_country = country.iso_country '
           f'where country.name = "{country_name}" and type like "{biggest_airport_size}" order by rand() limit 1;')

    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()

    # palauttaa tuloksen ensimmäisen arvon jos tulos on olemassa
    return result[0] if result else False


def get_default_money(difficulty_level):
    sql = f'select starting_money from difficulty where level = "{difficulty_level}";'
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    return result[0]


def get_treasure_land_airports(difficulty_level, country_name):
    sql = f'select airports_in_treasure_land from difficulty where level = "{difficulty_level}";'
    cursor = connection.cursor()
    cursor.execute(sql)
    airport_count = cursor.fetchone()[0]

    sql = (f'SELECT airport.name FROM airport inner join country on airport.iso_country = country.iso_country '
           f'where country.name = "{country_name}" order by rand() limit {airport_count};')
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()

    results = []
    for item in result:
        results.append(item[0])
    return results


def get_wise_man_count(difficulty_level):
    sql = (f'select wise_man_count from difficulty '
           f'where level = "{difficulty_level}";')
    cursor = connection.cursor()
    cursor.execute(sql)
    wise_man_count = cursor.fetchone()[0]
    return wise_man_count


def input_player_info(screen_name, money, home_airport, location, difficulty_level):
    sql = (f'insert into game(screen_name, money, home_airport, location, difficulty_level) '
           f'values("{screen_name}", "{money}", "{home_airport}", "{location}", "{difficulty_level}");')
    cursor = connection.cursor()
    cursor.execute(sql)


def get_airport_ident_from_name(airport_name):
    sql = f'select ident from airport where name = "{airport_name}";'
    cursor = connection.cursor(buffered=True)
    cursor.execute(sql)
    ident = cursor.fetchone()[0]
    return ident
