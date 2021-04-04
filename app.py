import time
import sys
import os
from typing import List, Callable

my_users = {'matkac98@gmail.com': 'Perla1998!', 'natjoz@gmail.com': 'byleco', 'a': 'b'}


class Movie:
    def __init__(self, id, title, year, rating, price):
        self._id = id
        self._title = title
        self._year = year
        self._rating = rating
        self._price = price

    @property
    def id(self):
        return int(self._id)

    @property
    def title(self):
        return self._title

    @property
    def year(self):
        return int(self._year)

    @property
    def rating(self):
        return float(self._rating)

    @property
    def price(self):
        return float(self._price)

    def __repr__(self):
        return f'{self._title} - {self._year}'


class User:
    def __init__(self, nickname, password, account):
        self._nickname = nickname
        self._password = password
        self._account = account
    @property
    def nickname(self):
        return self._nickname

    @property
    def password(self):
        return self._password

    @property
    def account(self):
        return self._account

    def __repr__(self):
        return f'{self._nickname} - {self._password} - {self._account}'


class RentalSystem:
    def __init__(self, movie_db, rent_db, user_db):
        self._rent_db = rent_db
        self._movie_db = movie_db
        self._user_db = user_db

    def get_movies(self, callback: Callable) -> List[Movie]:
        with open(self._movie_db) as read_handler:
            return list(filter(callback, [Movie(*line.split('|')) for line in read_handler]))

    def add(self, movie: Movie):
        with open(self._movie_db, 'a') as append_handler:
            append_handler.write(f'{movie.id}|{movie.title}|{movie.year}|{movie.rating}|{movie.price}\n')

    def remove(self, movie_id: int):
        with open(self._movie_db) as read_handler:
            movies = read_handler.readlines()
        with open(self._movie_db, 'w') as write_handler:
            for line in movies:
                if int(line.split('|')[0]) != movie_id:
                    write_handler.write(line)

    def exists(self, movie_id: int) -> bool:
        with open(self._movie_db) as read_handler:
            for line in read_handler:
                if int(line.split('|')[0]) == movie_id:
                    return True
        return False

    def is_rented(self, movie_id: int) -> bool:
        with open(self._rent_db) as read_handler:
            for line in read_handler:
                if int(line.split(":")[0]) == movie_id:
                    return True
        return False

    def give_back(self, movie_id):
        if not self.is_rented(movie_id):
            raise ValueError(f'Movie {movie_id} is not rented')
        with open(self._rent_db, 'r') as read_handler:
            rented_movies = read_handler.readlines()
        with open(self._rent_db, 'w') as write_handler:
            for line in rented_movies:
                if line.split(":")[0] != movie_id:
                    write_handler.write(" ")

    def rent(self, movie_id: int, person):
        if not self.exists(movie_id):
            raise ValueError(f'Movie {movie_id} does not exist')
        with open(self._rent_db) as append_handler:
            for line in append_handler:
                if int(line.split(":")[0]) == int(movie_id):
                    return f"This movie is actually rent by {line.split(':')[1]}"
        with open(self._rent_db,'a') as append_handler:
            append_handler.write(f'{movie_id}:{person}\n')

    def get_movie_price(self, movie_id:int)->float:
        with open(self._movie_db) as read_handler:
            for line in read_handler:
                if int(line.split("|")[0]) == movie_id:
                    return float(line.split("|")[4])
        return "System nie może znalezc filmu o podanym ID"



class UserSystem:
    def __init__(self, users_db, movie_db):
        self._users_db = users_db
        self._movie_db = movie_db

    def add(self, user: User):
        with open(self._users_db, 'a') as append_handler:
            append_handler.write(f'{user.nickname}|{user.password}|{user.account}\n')

    def remove(self, user_nickname):
        with open(self._users_db) as read_handler:
            users = read_handler.readlines()
        with open(self._users_db, 'w') as write_handler:
            for line in users:
                if line.split("|")[0] != user_nickname:
                    write_handler.write(line)
                else:
                    write_handler.write("")

    def exists(self, user_nickname):
        with open(self._users_db) as read_handler:
            for line in read_handler:
                if str(line.split('|')[0]) == user_nickname:
                    return True
        return False

    def correct_password(self, user_password):
        with open(self._users_db) as read_handler:
            for line in read_handler:
                if line.split("|")[1] == user_password:
                    return True
        return False

    def get_user_money(self, user_email):
        with open(self._users_db) as read_handler:
            for line in read_handler:
                if line.split("|")[0]==user_email:
                    return float(line.split("|")[2])
        return "Wystąpił błąd, system nie może znalezc usera o podanym emailu..."

def bad_login():
    print("Co chcesz zrobić ?")
    print("1.Próba ponownego logowania")
    print("2.Dodanie nowego użytkownika")
    print("3.Wyjście z programu")
    bad_login = int(input("Wybierz: "))
    if bad_login == 1:
        user_system = UserSystem('system_users.db')
        print(user_system.exists())
    if bad_login == 2:
        pass

    if bad_login == 3:
        print("ZAPRASZAMY PONOWNIE")
        sys.exit(0)


def menu(user:User):
    rental_system = RentalSystem('movies.db','rents.db','system_users.db')
    system = RentalSystem('movies.db','rents.db','system_users.db')
    user_system = UserSystem('system_users.db','movies.db')
    print("1.Wypożyczenie filmu")
    print("2.Oddanie filmu")
    print("3.Dodanie filmu do wypożyczalni")
    print("4.Usunięcie filmu z wypożyczalni")
    print("5.Powrót do filtrowanie")
    print("6.Sprawdzenie stanu konta")
    print("7.Wyjście z programu")

    your_choice = int(input("Wybór: "))
    if your_choice == 1:
        print("Wybierz 0 jeśli chcesz się cofnąć do menu")
        print(show())
        your_movie_number = int(input("Wpisz numer katalogu filmu jaki chcesz wypożyczyć: "))
        if your_movie_number == 0:
            print(menu(user))
        if your_movie_number != 0 and user_system.get_user_money(user.nickname)>=rental_system.get_movie_price(your_movie_number):
            system.rent(your_movie_number,user.nickname)
            with open('system_users.db') as read_handler:
                for line in read_handler:
                    if line.split("|")[0] == user.nickname:
                        new_user=User(line.split("|")[0],line.split("|")[1],round(user_system.get_user_money(user.nickname)-rental_system.get_movie_price(your_movie_number),2))
            user_system.remove(user.nickname)
            user_system.add(new_user)
            print(f'Film o numerze katalogowym {your_movie_number} został wypożyczony. Z konta znika {rental_system.get_movie_price(your_movie_number)}. Na koncie pozostało {round(user_system.get_user_money(user.nickname)-rental_system.get_movie_price(your_movie_number),2)}')
            print(menu(user))
        print (f"Brak wystarczających środków na koncie. Zasil konto kwotą {round(rental_system.get_movie_price(your_movie_number)-user_system.get_user_money(user.nickname),2)}")
        time.sleep(3)
        print(menu(user))
    if your_choice == 2:
        print("Wybierz 0 jeśli chcesz się cofnąć do menu")
        your_movie_number2 = int(input("Wpisz numer katalogu filmu jaki chcesz zwrócić: "))
        if your_movie_number2 == 0:
            print(menu(user))
        else:
            system.give_back(your_movie_number2)
            print (f'Film o numerze katalogowym {your_movie_number2} został zwrócony !')
            print (menu(user))
    if your_choice == 3:
        print("Wybierz 0 jeśli chcesz się cofnąć do menu")
        my_list_len=0
        with open('movies.db') as read_handler:
            for line in read_handler:
                my_list_len+=1
        your_movie_number = my_list_len+1
        if your_movie_number == 0:
            print(menu(user))
        else:
            movie_title = input("Wpisz tytuł filmu: ")
            movie_year = int(input("Wpisz rok produkcji filmu: "))
            movie_rating = float(input("Wpisz ocenę filmu: "))
            movie_price = float(input("Wpisz cenę filmu: "))
            new_movie = Movie(your_movie_number, movie_title, movie_year, movie_rating, movie_price)
            system.add(new_movie)
            print (f'Film {movie_title} został dodany do wypożyczalni')
            print(menu(user))
    if your_choice == 4:
        print("Wybierz 0 jeśli chcesz się cofnąć do menu")
        your_movie_number = int(input("Wpisz numer katalogu filmu jaki ma zostać usunięty: "))
        if your_movie_number == 0:
            print(menu(user))
        else:
            system.remove(your_movie_number)
            print (f'Film o numerze {your_movie_number} został usunięty ')
            print(menu(user))
    if your_choice == 5:
        print(show())
    if your_choice == 6:
        print (user_system.get_user_money(user.nickname))
        time.sleep(3)
        print(menu(user))
    if your_choice == 7:
        print("ZAPRASZAMY PONOWNIE")
        sys.exit(0)


def show():
    print("Czy chcesz użyć filtru")
    print("1-tak 2-nie")
    filtr = input("Odpowiedz: ")
    if filtr == "1" or filtr == "tak":
        print("Jaki rodzaj filtru")
        print("1.Filtrowanie przez rok produkcji")
        print("2.Filtrowanie przez oceny")
        print("3.Filtrowanie przez rok produkcji i oceny")
        print("4.Filtrowanie przez cene")
        your_filter = int(input("Wybierz swój rodzaj filtru: "))
        if your_filter == 1:
            oldest_year_of_movie = int(input("Wpisz najstarsy rok produkcji filmu: "))
            newest_year_of_movie = int(input("Wpisz najmłodszy rok produkcji filmu: "))
            list_of_movie = {}
            with open('movies.db', 'r') as read_handler:
                for line in read_handler:
                    movie_data = line.split("|")
                    if int(movie_data[2]) >= oldest_year_of_movie and int(movie_data[2]) <= newest_year_of_movie:
                        list_of_movie[movie_data[0]] = movie_data[1]
                return list_of_movie
        if your_filter == 2:
            lowest_note_of_movie = float(input("Wpisz najmniejszą ocenę filmu: "))
            highest_note_of_movie = float(input("Wpisz największą możliwę ocenę filmu: "))
            list_of_movie = {}
            with open('movies.db', 'r') as read_handler:
                for line in read_handler:
                    movie_data = line.split("|")
                    if float(movie_data[3]) >= lowest_note_of_movie and float(movie_data[3]) <= highest_note_of_movie:
                        list_of_movie[movie_data[0]] = movie_data[1]
                return list_of_movie
        if your_filter == 3:
            oldest_year_of_movie = int(input("Wpisz najstarsy rok produkcji filmu: "))
            newest_year_of_movie = int(input("Wpisz najmłodszy rok produkcji filmu: "))
            lowest_note_of_movie = float(input("Wpisz najmniejszą ocenę filmu: "))
            highest_note_of_movie = float(input("Wpisz największą możliwę ocenę filmu: "))
            list_of_movie = {}
            with open('movies.db', 'r') as read_handler:
                for line in read_handler:
                    movie_data = line.split("|")
                    if int(movie_data[2]) >= oldest_year_of_movie and int(
                            movie_data[2]) <= newest_year_of_movie and float(
                            movie_data[3]) >= lowest_note_of_movie and float(movie_data[3]) <= highest_note_of_movie:
                        list_of_movie[movie_data[0]] = movie_data[1]
                return list_of_movie
        if your_filter == 4:
            max_price = float(input("Wpisz cenę maksymalną: "))
            list_of_movie = {}
            with open('movies.db', 'r') as read_handler:
                for line in read_handler:
                    movie_data = line.split("|")
                    if float(movie_data[4]) <= max_price:
                        list_of_movie[movie_data[0]] = movie_data[1]
                return list_of_movie
        else:
            print('Nie ma takiego filtru')
            time.sleep(3)
            return show()
    if filtr == "2" or filtr == "nie":
        list_of_movie = []
        with open('movies.db', 'r') as read_handler:
            for line in read_handler:
                movie_data = line.split("|")
                list_of_movie.append(movie_data[1])
            return list_of_movie
    if filtr == "0":
        return menu(user.nickname)
    else:
        print("To jest za duży numer, spróbuj ponownie !")
        time.sleep(3)
        return show()


if __name__ == '__main__':
    user=User('matkac98@gmail.com','matkac98@gmail.com',98.32)
    ren_sys=RentalSystem('movies.db','rents.db','system_users.db')
    print(menu(user))