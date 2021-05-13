from django.shortcuts import redirect
from django.urls import reverse
import numpy as np
import pandas as pd
from collections import Counter

import os

import deepzoom
import PIL.Image as Image
import piexif
import zipfile

def transpose_img(path):
    #img = Image.open(path)

    #file_name, file_type = os.path.splitext(src_file.filename)
    exif_dict = piexif.load(path)

    flag = 1
    if piexif.ImageIFD.Orientation in exif_dict["0th"]:
        orientation = exif_dict["0th"].pop(piexif.ImageIFD.Orientation)
        #print(orientation)
        exif_bytes = piexif.dump(exif_dict)
        if orientation == 1:
            flag = 0
        else:
            img = Image.open(path)
            if orientation == 2:
                img = img.transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 3:
                img = img.rotate(180)
            elif orientation == 4:
                img = img.rotate(180).transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 5:
                img = img.rotate(-90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 6:
                img = img.rotate(-90, expand=True)
            elif orientation == 7:
                img = img.rotate(90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 8:
                img = img.rotate(90, expand=True)
    if flag == 1:
        #print(path)
        img.save(path, quality=95, exif=exif_bytes)

def unzip_file(src_file, dest_dir):
    with open(src_file, 'rb') as src_file:
        zip_file = zipfile.ZipFile(src_file)
        for names in zip_file.namelist():
            zip_file.extract(names, dest_dir)
        zip_file.close()



#装饰器函数
def login_decorator(session_item = 'is_login_manager', redirect_url = 'manager_login'):
    def decorator(func):
        def wrapper(request, *args, **kargs):
            if request.session.get(session_item,None):
                return func(request, *args, **kargs)
            else:
                return redirect(reverse(redirect_url))
        return wrapper
    return decorator


#获取排名
def extract_pair_data(pair_list):
    pair_data = []
    for pair in pair_list:
        line = [pair[0], pair[1], 1, 0]
        pair_data.append(line)
        
    columns = ["Player A", "Player B", "Wins A", "Wins B"]

    df = pd.DataFrame(pair_data, columns=columns)
    #assert all(c in df.columns for c in ['Date', 'Player A', 'Player B', 'Wins A', 'Wins B']), \
    #    'Expecting columns Date, Player A, Player B, Wins A, Wins B'

    df['Wins A'] = df['Wins A'].astype(int)
    df['Wins B'] = df['Wins B'].astype(int)

    return df

def compute_rank_scores(game_data, max_iters=1000, error_tol=1e-3):
    winsA = game_data.groupby('Player A').agg(sum)['Wins A'].reset_index()
    winsA = winsA[winsA['Wins A'] > 0]
    winsA.columns = ['Player', 'Wins']
    winsB = game_data.groupby('Player B').agg(sum)['Wins B'].reset_index()
    winsB = winsB[winsB['Wins B'] > 0]
    winsB.columns = ['Player', 'Wins']
    wins = pd.concat([winsA, winsB]).groupby('Player').agg(sum)['Wins']

    # Total games played between pairs
    num_games = Counter()
    for index, row in game_data.iterrows():
        key = tuple(sorted([row['Player A'], row['Player B']]))
        total = sum([row['Wins A'], row['Wins B']])
        num_games[key] += total

    # Iteratively update 'ranks' scores
    players = sorted(list(set(game_data['Player A']) | set(game_data['Player B'])))
    ranks = pd.Series(np.ones(len(players)) / len(players), index=players)
    for iters in range(max_iters):
        oldranks = ranks.copy()
        for player in ranks.index:
            denom = np.sum(num_games[tuple(sorted([player, p]))]
                           / (ranks[p] + ranks[player])
                           for p in ranks.index if p != player)
            ranks[player] = 1.0 * wins[player] / denom

        ranks /= sum(ranks)

        if np.sum((ranks - oldranks).abs()) < error_tol:
            break

    #if np.sum((ranks - oldranks).abs()) < error_tol:
    #    print(" * Converged after %d iterations.", iters)
    #else:
    #    print(" * Max iterations reached (%d iters).", max_iters)

    #print(ranks)
    # Scale logarithm of score to be between 1 and 1000
    ranks = ranks.sort_values(ascending=False) \
                 .apply(lambda x: np.log1p(1000 * x) / np.log1p(1000) * 100) \
                 #.astype(int) \
                 #.clip(1)
    rankList = []
    for value in ranks.keys():
        rankList.append((value, ranks[value]))

    return rankList
