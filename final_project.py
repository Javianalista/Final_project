import pandas as pd
import numpy as np
import pymysql
from sqlalchemy import create_engine
import getpass
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import requests
from skimage import io
import random
import re
import ssl
import cv2 as cv
import time
from sklearn import cluster, datasets
from sklearn.preprocessing import StandardScaler
from matplotlib.lines import Line2D
from sklearn.cluster import KMeans


cluster = pd.read_excel('./files_for_project/cluster.xlsx')
act = pd.read_excel('./files_for_project/act.xlsx')
top_100 = pd.read_excel('./files_for_project/top_100.xlsx')
actors = pd.read_excel('./files_for_project/actors.xlsx')
comparing_table = pd.read_excel('./files_for_project/cluster.xlsx')
final_data = pd.read_excel('./files_for_project/final_data.xlsx')

final_data = final_data.drop(['Unnamed: 0'], axis = 1)
numericals = final_data._get_numeric_data()
scaled_variables = StandardScaler().fit_transform(numericals)

# Now, all features will have the same weight.
pd.DataFrame(scaled_variables,columns=numericals.columns).head()

kmeans = KMeans(n_clusters=10, random_state=1234)
kmeans.fit(scaled_variables)

def directors1():
    print("Enter a director:")
    director = input()
    spaces = []
    for i in range(len(director)):
        if director[i] == ' ':
            spaces = spaces + [i]
    if len(spaces) == 0:
        url = "https://www.lahiguera.net/cinemania/buscapelis.php?nro_pagina=0&por=2&texto=" + director
    elif len(spaces) == 1:
        first_name = director[0:spaces[0]]
        second_name = director[spaces[0] +1:len(director)]
        url = "https://www.lahiguera.net/cinemania/buscapelis.php?nro_pagina=0&por=2&texto=" + first_name + "+" + second_name
    elif len(spaces) == 2:
        first_name = director[0:spaces[0]]
        second_name = director[spaces[0]+1:spaces[1]]
        third_name = director[spaces[1]+1:len(director)]
        url = "https://www.lahiguera.net/cinemania/buscapelis.php?nro_pagina=0&por=2&texto=" + first_name + "+" + second_name + "+" + third_name
    elif len(spaces) == 3:
        first_name = director[0:spaces[0]]
        second_name = director[spaces[0]+1:spaces[1]]
        third_name = director[spaces[1]+1:spaces[2]]
        fourth_name = director[spaces[2]+1:len(director)]
        url = "https://www.lahiguera.net/cinemania/buscapelis.php?nro_pagina=0&por=2&texto=" + first_name + "+" + second_name + "+" + third_name + "+" + fourth_name
    response = requests.get(url)
    response.status_code
    soup = BeautifulSoup(response.content, "html.parser")
    number_of_pages = soup.select("div.paginador")
    number_of_pages[0] = '''"'''  + str(number_of_pages[0]) + '''"'''
    pattern = '[0-9]+'
    pages_noint = re.findall(pattern,number_of_pages[0])
    url_list = []
    pages = []
    for l in range(len(pages_noint)):
        pages = pages + [int(pages_noint[l])]
    if len(pages) == 0:
        print("Sorry, I can't recommend any films for this director")
        print("Do you want to try again?(y/n)")
        answer = input()
        while (answer != 'y') and (answer != 'n'):
            print("That's not a valid answer")
            print("Do you want to try again?(y/n)")
            answer = input()
        if answer == 'y':
            directors1()
        elif answer == 'n':
            asking()
        return
    else:
        if max(pages) == pages[len(pages)-1]:
            definitive_number = int(pages[len(pages)-1])
        else:
            max_position = 0
            for m in range(len(pages)):
                if pages[m] == max(pages):
                    max_position = m
            definitive_number = pages[max_position]
        for i in range(definitive_number):
            url_ = url[0:62] + str(i) + url[63:len(url)]
            url_list = url_list + [url_]
        images = []
        film = []
        number_film = []
        for i in range(len(url_list)):
            url = url_list[i]
            response = requests.get(url)
            response.status_code
            soup = BeautifulSoup(response.content, "html.parser")
            all_images = soup.select("img")
            for j in range(len(all_images)):
                if all_images[j]['src'].count("jpg") >= 1:
                    images = images + ['https://www.lahiguera.net' + all_images[j]["src"]]
                    film = film + [all_images[j]["alt"]]
        for i in range(len(film)):
            patternn = 'cartel reducido'
            film[i] = re.sub(patternn, '',film[i])
            linktext = "'" + str(images[i]) + "'"
            number_of_the_film = re.findall(pattern,linktext)
            number_film = number_film + [number_of_the_film[0]]
        ssl._create_default_https_context = ssl._create_unverified_context
        numbers = []
        final_film = []
        if len(film) == 0:
            print("Sorry, I haven't any recommendations from " + director + ", try with another one.")
        elif len(film) == 1:
            print("I can recommend you this film from " + director + ":")
            print(film[0])
            plt.imshow(images[0],vmin=0,vmax=1)
        else:
            random_1 = random.randint(0, len(film)-1)
            random_2 = random.randint(0, len(film)-1)
            while random_1 == random_2:
                random_2 = random.randint(0, len(film))
            numbers = numbers + [random_1] + [random_2]
            if definitive_number > 4:
                print("I think you have introduced a common name, so i'm going to recommend you two films and their director:")
            else:
                print("I can recommend you this films from " + director + ":")
            final_film = final_film + [number_film[random_1]] + [number_film[random_2]]
            for i in range(len(numbers)):
                print(film[numbers[i]])
                url_film = "https://www.lahiguera.net/cinemania/pelicula/" + final_film[i] + "/"
                response = requests.get(url_film)
                response.status_code
                soup = BeautifulSoup(response.content, "html.parser")
                if definitive_number > 4:
                    position = []
                    director_film = soup.select("#principal > div.datos_foto > section.datos > p")
                    director_film1 = str(director_film[0])
                    for l in range(len(director_film1)):
                        if (director_film1[l] == '<') or (director_film1[l] == '>'):
                            position = position + [l]
                    print(director_film1[position[9] + 1 :position[10]])
                final_images = soup.select("img")
                for j in range(len(final_images)):
                    element = final_images[j]["src"]
                    if element.count("jpg") >= 1:
                        url_image = element
                big_image = url_film + url_image
                image = io.imread(big_image)/255.0
                my_dpi = 96
                plt.figure(figsize=(300/my_dpi, 300/my_dpi), dpi=my_dpi)
                plt.imshow(image,vmin=0,vmax=1)
                plt.show()
        print("Do you want to try again?(y/n)")
        answer = input()
        while (answer != 'y') and (answer != 'n'):
            print("That's not a valid answer")
            print("Do you want to try again?(y/n)")
            answer = input()
        if answer == 'y':
            directors1()
        elif answer == 'n':
            asking()
        return 


act = pd.read_excel('./files_for_project/act.xlsx', index_col=[0])
actors = pd.read_excel('./files_for_project/actors.xlsx', index_col=[0])


def actor_similar():
    finish = 'y'
    while finish == 'y':
        print('We are going to make you some questions.')
        print('Are you male or female?(M/F)')
        gender = input()
        while (gender != 'M') and (gender != 'F'):
            print('Sorry, this is not a valid value.')
            time.sleep(1)
            print('Are you male or female?(M/F)')
            gender = input()
        print('Which is the color of you hair?(1/2/3/4/5/6)')
        print('1. Brown')
        time.sleep(2)
        print('2. Blonde')
        time.sleep(1)
        print('3. Black')
        time.sleep(1)
        print('4. Gray')
        time.sleep(1)
        print('5. Red')
        time.sleep(1)
        print('6. Bald')
        time.sleep(1)
        color_number = input()
        while (color_number != '1') and (color_number != '2') and (color_number != '3') and (color_number != '4') and (color_number != '5') and (color_number != '6'):
            print('Sorry, this is not a valid value.')
            print('Which is the color of you hair?(1/2/3/4/5/6)')
            color_number = input()
        if color_number == '1':
            haircolor = 'brown'
        elif color_number == '2':
            haircolor = 'blonde'
        elif color_number == '3':
            haircolor = 'dark'
        elif color_number == '4':
            haircolor = 'gray'
        elif color_number == '5':
            haircolor = 'red'
        elif color_number == '6':
            haircolor = 'bald'
        print('How tall are you)(in cm)')
        height = input()
        isvalid = 0
        while isvalid == 0:
            try:
                height = int(height)
                if (height < 140) or (height > 220):
                    laa = laaa
                else:
                    isvalid = 1
            except:
                print('The value is not valid. Try again.')
                print('How tall are you)(in cm)')
                height = input()
        print('Which is your type of skin?(1/2/3)')
        print('1. White')
        time.sleep(2)
        print('2. Brown')
        time.sleep(1)
        print('3. Asian')
        time.sleep(1)
        skin = input()
        while (skin != '1') and (skin != '2') and (skin != '3'):
            print('Sorry, this is not a valid value.')
            print('Which is your type of skin?(1/2/3)')
            skin = input()
        if skin == '1':
            skincolor = 'white'
        elif skin == '2':
            skincolor = 'brown'
        elif skin == '3':
            skincolor = 'asian'
        print('Which is your type of hair?(1/2/3)')
        print('1. Straight')
        time.sleep(2)
        print('2. Wavy')
        time.sleep(1)
        print('3. Curly')
        time.sleep(1)
        hairst = input()
        while (hairst != '1') and (hairst != '2') and (hairst != '3'):
            print('Sorry, this is not a valid value.')
            print('Which is your type of hair?(1/2/3)')
            hairst = input()
        if hairst == '1':
            hairstyle = 'straight'
        elif hairst == '2':
            hairstyle = 'wavy'
        elif hairst == '3':
            hairstyle = 'curly'
        if gender == 'M':
            print('Have you got beard?(y/n)')
            beard_yn = input()
            while (beard_yn != 'y') and (beard_yn != 'n'):
                print('Sorry, this is not a valid value.')
                print('Have you got beard?(y/n)')
                beard_yn = input()
            if beard_yn == 'y':
                beard = 'yes'
            elif beard_yn == 'n':
                beard = 'no'
        else:
            beard = 'no'
        print('And the last... Which is the color of your eyes?(1/2/3/4)')
        print('1. Brown')
        time.sleep(2)
        print('2. Blue')
        time.sleep(1)
        print('3. Green')
        time.sleep(1)
        print('4. Gray')
        time.sleep(1)
        eyes_number = input()
        while (eyes_number != '1') and (eyes_number != '2') and (eyes_number != '3') and (eyes_number != '4'):
            print('Sorry, this is not a valid value.')
            print('Which is the color of your eyes?(1/2/3/4)')
            eyes_number = input()
        if eyes_number == '1':
            eyes = 'brown'
        elif eyes_number == '2':
            eyes = 'blue'
        elif eyes_number == '3':
            eyes = 'green'
        elif eyes_number == '4':
            eyes = 'gray'
        if gender == 'M':
            possible_candidates = act[act['gender'] == 'M']
            possible_candidates = possible_candidates.reset_index(drop = True)
            possible_candidates['score'] = 0
        elif gender == 'F':
            possible_candidates = act[act['gender'] == 'F']
            possible_candidates = possible_candidates.reset_index(drop = True)
            possible_candidates['score'] = 0
        for i in range(len(possible_candidates['score'])):
            score = 0
            if possible_candidates['skin'][i] == skincolor:
                score = score + 15
            if possible_candidates['height'][i] == height:
                score = score + 10
            elif ((possible_candidates['height'][i] + 3) > height) or ((possible_candidates['height'][i] - 3) < height):
                score = score + 5
            if possible_candidates['hair'][i] == haircolor:
                score = score + 15
            if possible_candidates['hairstyle'][i] == hairstyle:
                score = score + 10
            if possible_candidates['beard'][i] == beard:
                score = score + 10
            if possible_candidates['eyes'][i] == eyes:
                score = score + 15
            possible_candidates['score'][i] = score
        final_candidates = possible_candidates[possible_candidates['score'] == possible_candidates['score'].max()]
        final_candidates = final_candidates.reset_index(drop = True)
        if (len(final_candidates) == 1) and (gender == 'M'):
            print('The actor who looks more like u is: ' + final_candidates['name'][0])
            linkkk = final_candidates['img'][0]
            image = io.imread(linkkk)/255.0
            my_dpi = 96
            plt.figure(figsize=(300/my_dpi, 300/my_dpi), dpi=my_dpi)
            plt.imshow(image,vmin=0,vmax=1)
            plt.show()
        elif (len(final_candidates) == 1) and (gender == 'F'):
            print('The actress who looks more like u is: ' + final_candidates['name'][0])
            linkkk = final_candidates['img'][0]
            image = io.imread(linkkk)/255.0
            my_dpi = 96
            plt.figure(figsize=(300/my_dpi, 300/my_dpi), dpi=my_dpi)
            plt.imshow(image,vmin=0,vmax=1)
            plt.show()
        else:
            if (len(final_candidates) > 1) and (gender == 'M'):
                max_value = len(final_candidates) - 1
                random_number = random.randint(0,max_value)
                print('The actor who looks more like u is: ' + final_candidates['name'][random_number])
                linkkk = final_candidates['img'][random_number]
                image = io.imread(linkkk)/255.0
                my_dpi = 96
                plt.figure(figsize=(300/my_dpi, 300/my_dpi), dpi=my_dpi)
                plt.imshow(image,vmin=0,vmax=1)
                plt.show()
            elif (len(final_candidates) > 1) and (gender == 'F'):
                max_value = len(final_candidates) - 1
                random_number = random.randint(0,max_value)
                print('The actress who looks more like u is: ' + final_candidates['name'][random_number])
                linkkk = final_candidates['img'][random_number]
                image = io.imread(linkkk)/255.0
                my_dpi = 96
                plt.figure(figsize=(300/my_dpi, 300/my_dpi), dpi=my_dpi)
                plt.imshow(image,vmin=0,vmax=1)
                plt.show()
        print('Do you want to try again?(y/n)')
        finish = input()
        while (finish != 'y') and (finish != 'n'):
            print('Thats not valid. Please enter a valid value.')
            print('Do you want to try again?(y/n)')
            finish = input()        
    if finish == 'n':
        asking()        
    return


def actor_birthday():
    finish = 'y'
    while finish == 'y':
        print('Please, enter your birthday(format: dd/mm/yyyy)')
        birthday = input()
        isvalid = 0
        while isvalid == 0:
            try:
                day = int(birthday[0:2])
                month = int(birthday[3:5])
                year = int(birthday[6:10])
                if (day < 1) or (day>31):
                    la = lalaa # creating an error
                elif (month < 1) or (month>12):
                    la = lalaa # creating an error
                elif (year < 1920) or (year>2021):
                    la = lalaa # creating an error
                else:
                    isvalid = 1
            except:
                print('Sorry, this is not the correct format. Please, try again')
                birthday = input()
        only_day_selected = act[act['day'] == day]
        if len(only_day_selected['name']) >=1:
            only_day_selected = only_day_selected.reset_index(drop = True)
            day_month_selected = only_day_selected[only_day_selected['month'] == month]
            if len(day_month_selected['name']) >=1:
                day_month_selected = day_month_selected.reset_index(drop = True)
                all_selected = day_month_selected[day_month_selected['year'] == year]
                if len(all_selected['name']) >=1:
                    all_selected = all_selected.reset_index(drop = True)
        only_month_selected = act[act['month'] == month]
        if len(only_month_selected['name']) >=1:
            only_month_selected = only_month_selected.reset_index(drop = True)
            month_and_year = only_month_selected[only_month_selected['year'] == year]
            if len(month_and_year['name']) >=1:
                month_and_year = month_and_year.reset_index(drop = True)
        if len(all_selected['name']) == 1:
            print('Wow, you have the same date of birth than ' + str(all_selected['name'][0]) + ', whose birth of date is: ' + str(all_selected['day'][0]) + '-' + str(all_selected['month'][0]) +'-'+ str(all_selected['year'][0]))
            link = all_selected['img'][0]
            image = io.imread(link)/255.0
            my_dpi = 96
            plt.figure(figsize=(300/my_dpi, 300/my_dpi), dpi=my_dpi)
            plt.imshow(image,vmin=0,vmax=1)
            plt.show()
            print('Do you want to try again?(y/n)')
            finish = input()
            while (finish != 'y') and (finish != 'n'):
                print('Thats not valid. Please enter a valid value.')
                print('Do you want to try again?(y/n)')
                finish = input()
        elif len(all_selected['name']) >= 1:
            print('Wow, you have the same date of birth than:')
            for i in range(len(all_selected['name'])):
                print('-' + str(all_selected['name'][i]))
                link = all_selected['img'][i]
                image = io.imread(link)/255.0
                my_dpi = 96
                plt.figure(figsize=(300/my_dpi, 300/my_dpi), dpi=my_dpi)
                plt.imshow(image,vmin=0,vmax=1)
                plt.show()
            print('Do you want to try again?(y/n)')
            finish = input()
            while (finish != 'y') and (finish != 'n'):
                print('Thats not valid. Please enter a valid value.')
                print('Do you want to try again?(y/n)')
                finish = input()
        else:
            if len(day_month_selected['name']) >=1:
                print('Here we have not any actor with the same date of birth, but we have that actors with the same birthday:')
                for i in range(len(day_month_selected['name'])):
                    print('-' + str(day_month_selected['name'][i]) + ': ' + str(day_month_selected['day'][i]) + '-' + str(day_month_selected['month'][i]) +'-'+ str(day_month_selected['year'][i]))
                    linkk = day_month_selected['img'][i]
                    image = io.imread(linkk)/255.0
                    my_dpi = 96
                    plt.figure(figsize=(300/my_dpi, 300/my_dpi), dpi=my_dpi)
                    plt.imshow(image,vmin=0,vmax=1)
                    plt.show()
                print('Do you want to try again?(y/n)')
                finish = input()
                while (finish != 'y') and (finish != 'n'):
                    print('Thats not valid. Please enter a valid value.')
                    print('Do you want to try again?(y/n)')
                    finish = input()
            else:
                if len(month_and_year['name']) >=1:
                    print('Here we have not any actor with the same date of birth, but we have that actors that were born in the same month and year:')
                    for i in range(len(month_and_year['name'])):
                        print('-' + str(month_and_year['name'][i]) + ': ' + str(month_and_year['day'][i]) + '-' + str(month_and_year['month'][i]) +'-'+ str(month_and_year['year'][i]))
                        linkkk = month_and_year['img'][i]
                        image = io.imread(linkkk)/255.0
                        my_dpi = 96
                        plt.figure(figsize=(300/my_dpi, 300/my_dpi), dpi=my_dpi)
                        plt.imshow(image,vmin=0,vmax=1)
                        plt.show()
                    print('Do you want to try again?(y/n)')
                    finish = input()
                    while (finish != 'y') and (finish != 'n'):
                        print('Thats not valid. Please enter a valid value.')
                        print('Do you want to try again?(y/n)')
                        finish = input()
                else:
                    print('Sorry, for that date we have not any actor.')
                    print('Do you want to try again?(y/n)')
                    finish = input()
                    while (finish != 'y') and (finish != 'n'):
                        print('Thats not valid. Please enter a valid value.')
                        print('Do you want to try again?(y/n)')
                        finish = input()
    if finish == 'n':
        asking()
    return


def asking_actor():
    print('Welcome! Here we have two different parts:')
    time.sleep(2)
    print('1. Which actor-actress do you look like?')
    time.sleep(1)
    print('2. Which actor-actress has the most similar birthday to you?')
    time.sleep(1)
    print('3. Exit')
    time.sleep(1)
    print('Which function do you want to try?(1/2/3)')
    answer = input()
    while (answer != '1') and (answer != '2') and (answer != '3'):
        print('''Sorry, we haven't that fuction implemented yet, please, select a valid value(1/2)''')
        answer = input()
    if answer == '1':
        return actor_similar()
    elif answer == '2':
        return actor_birthday()
    elif answer == '3':
        return asking()

genres_list = []
for i in range(len(final_data['genres'])):
    element = final_data['genres'][i].split(sep = '|')
    for j in range(len(element)):
        if element[j] not in genres_list:
            genres_list = genres_list + [element[j]]

def asking():
    print('Hello! Here we have 3 different functions:')
    time.sleep(2)
    print('1. Movie recommender')
    time.sleep(1)
    print('2. Actor-actress like you')
    time.sleep(1)
    print('3. Search movies by director')
    time.sleep(1)
    print('4. Exit')
    print('Which function do you want to try?(1/2/3/4)')
    answerr = input()
    while (answerr != '1') and (answerr != '2') and (answerr != '3') and (answerr != '4'):
        print('''Sorry, we haven't that fuction implemented yet, please, select a valid value(1/2/3/4)''')
        answerr = input()
    if answerr == '1':
        return movies_recommender(genres_list)
    elif answerr == '2':
        return asking_actor()
    elif answerr == '3':
        return directors1()
    elif answerr == '4':
        return


def movies_recommender(genres_list):
    print('Welcome to the movie recommender')
    print('Please, choose a film:')
    film = input()
    listaa = []
    pos = []
    for i in range(len(top_100['film'])):
        if top_100['film'][i].count(film) >=1:
            listaa = listaa + [top_100['film'][i]]
            pos = pos + [i]
            break
    if len(listaa) > 0:
        print('Congrats! Your film is into the top 100 most viewed films, in the position ' + str(pos[0])) 
        random_number = random.randint(0,99)
        print('Here we give you another one in the top: ' + top_100['film'][random_number] + ')')
        print('Do you want to try again?(y/n)')
        answer = input()
        while (answer != 'y') and (answer != 'n'):
            print('Sorry, this film is not valid.')
            print('Do you want to try again?(y/n)')
            answer = input()
        if answer == 'y':
            return movies_recommender(genres_list)
        else:
            return asking()
    else:
        filmmm = film.replace(' ', '-')
        url1 = 'https://www.ecartelera.com/peliculas/' + filmmm + '/'
        response1 = requests.get(url1)
        valuee = response1.status_code
        if valuee == 200:
            try:
                soup1 = BeautifulSoup(response1.content, "html.parser")
                genres_films = soup1.select(' tr:nth-child(7) > td')
                genres_film = genres_films[0].get_text()
                if genres_film.count(',') > 0:
                    elementss = genres_film.split(sep = ',')
                else:
                    elementss = genres_film
                different_genres = []
                for i in range(len(genres_list)):
                    if genres_list[i] in elementss:
                        different_genres = different_genres + [1]
                    else:
                        different_genres = different_genres + [0]
                puntuationn = soup1.select('#newscores > div > div.fuentes > p > span')
                puntuation = puntuationn[0].get_text()
                puntuation = round((float(puntuation)/2),2)
                lista_definitiva = ['people_rating']
                values_dataframe = [puntuation]
                for i in range(len(genres_list)):
                    lista_definitiva = lista_definitiva + [genres_list[i]]
                    values_dataframe = values_dataframe + [different_genres[i]]
                data_features = pd.DataFrame([film], columns = ['film'])
                r = 0
                for elemento in lista_definitiva:
                    data_features[elemento] = values_dataframe[r]
                    r = r +1
                numeric_features = data_features._get_numeric_data()
                cluster_prediction = kmeans.predict(numeric_features)[0]
                similar_movies = comparing_table[comparing_table['cluster_type'] == cluster_prediction].sample(1)
                film_recommended = similar_movies['title'].values[0]
                print("Your song is not in the top 100, but we can recommend you this song from our database: " + film_recommended + "... Hope you like it!!!")
                print('Do you want to try again?(y/n)')
                answer = input()
                while (answer != 'y') and (answer != 'n'):
                    print('Sorry, this film is not valid.')
                    print('Do you want to try again?(y/n)')
                    answer = input()
                if answer == 'y':
                    return movies_recommender(genres_list)
                else:
                    return asking()
            except:
                print('Sorry, this film is not valid.')
                print('Do you want to try again?(y/n)')
                answer = input()
                while (answer != 'y') and (answer != 'n'):
                    print('Sorry, this film is not valid.')
                    print('Do you want to try again?(y/n)')
                    answer = input()
                if answer == 'y':
                    return movies_recommender(genres_list)
                else:
                    return asking()
        else:
            print('Sorry, this film is not valid.')
            print('Do you want to try again?(y/n)')
            answer = input()
            while (answer != 'y') and (answer != 'n'):
                print('Sorry, this film is not valid.')
                print('Do you want to try again?(y/n)')
                answer = input()
            if answer == 'y':
                return movies_recommender(genres_list)
            else:
                return asking()






asking()