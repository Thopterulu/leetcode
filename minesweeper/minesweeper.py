from preloaded import open

def get_the_hmm(map):
    confiance_hmm = {}
    for e in range(len(map)):
        for f in range(len(map[e])):
            if map[e][f]=="?":
                confiance_hmm[(e,f)] = 0
    return confiance_hmm

def count_neighbors(coord_x,coord_y,map):
    coords = [(coord_x + x, coord_y+y) for x, y in [(-1,-1),(-1,-0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)] if (coord_x + x)in range(len(map)) and (coord_y+y) in range(len(map[coord_x]))]
    vals = {(j,v):map[j][v] for j,v in coords}
    count_hmm = list(vals.values()).count("?")
    return count_hmm

def return_hmm_coords(coord_x,coord_y,map):
    coords = [(coord_x + x, coord_y+y) for x, y in [(-1,-1),(-1,-0),(-1,1),(0,-1),(0,0),(0,1),(1,-1),(1,0),(1,1)] if (coord_x + x)in range(len(map)) and (coord_y+y) in range(len(map[coord_x]))]
    vals = {(j,v):map[j][v] for j,v in coords}
    return [coords for coords,val in vals.items() if val=="?"]



def solve_mine(map, n):
    #print(n)
    map = [a_char.split(" ") for a_char in [a_line for a_line in map.split("\n")]]
    hmmmm = (len(map)* len(map[0]))**2
    original_sum = sum([a_line.count("?") for a_line in map])

    # getting all question marks on map
    while hmmmm > sum([a_line.count("?") for a_line in map]):
        hmmmm = sum([a_line.count("?") for a_line in map])
        confiance_hmm = get_the_hmm(map)
        for coord_x in range(len(map)):
            for coord_y in range(len(map[coord_x])):
                coords = [(coord_x + x, coord_y+y) for x, y in [(-1,-1),(-1,-0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)] if (coord_x + x)in range(len(map)) and (coord_y+y) in range(len(map[coord_x]))]
                match map[coord_x][coord_y]:
                    case "0":
                        map[coord_x][coord_y] = str(open(coord_x, coord_y))
                        if map[coord_x][coord_y] != "0":
                            continue
                        for x, y in coords:
                            map[x][y] = str(open(x, y))
                        confiance_hmm.pop((coord_x, coord_y), None)
                    case "?":
                        if hmmmm == n:
                            map[coord_x][coord_y] = "x"
                    case "x":
                        confiance_hmm.pop((coord_x, coord_y), None)
                    case _:
                        confiance_hmm.pop((coord_x, coord_y), None)
                        map[coord_x][coord_y] = str(open(coord_x, coord_y))
                        vals = {(j,v):map[j][v] for j,v in coords}
                        count_hmm = list(vals.values()).count("?")
                        count_x = list(vals.values()).count("x")
                        if str(count_hmm + count_x) == map[coord_x][coord_y]:
                            lmao_mines = [coords for coords,val in vals.items() if val=="?"]
                            for a_mine in lmao_mines:
                                map[a_mine[0]][a_mine[1]] = "x"
                                n -= 1
                        elif str(count_x) == map[coord_x][coord_y]:
                            lmao_open = [coords for coords,val in vals.items() if val=="?"]
                            for open_it in lmao_open:
                                map[open_it[0]][open_it[1]] = str(open(x, y))
                        elif len(set(confiance_hmm.keys()).intersection(set([coords for coords,val in vals.items() if val=="?"]))) > 0:
                            for a_coord in [coords for coords,val in vals.items() if val=="?"]:
                                confiance_hmm[a_coord] = confiance_hmm[a_coord] + (int(map[coord_x][coord_y])- len([coords for coords,val in vals.items() if val=="x"]))/len([coords for coords,val in vals.items() if val=="?"])
        # si à la fin d'un passage ils ont tous les mm chances alors impossible, sinon on ouvre la case et on reset les hmm
        # on ouvre un trésor au hasard mdr
        alicia = {k:v for k,v in confiance_hmm.items() if v}# si le score est à 0, on est jamais passé dessus, on enlève
        # si tous les voisins ont la même valeur proba alors on retourne "?"
        list_of_all_hmm = []
        for k in alicia.keys():
            list_of_all_hmm.append(return_hmm_coords(k[0], k[1], map))
        list_of_all_hmm.sort(key=len, reverse=True)
        try:
            if hmmmm == sum([a_line.count("?") for a_line in map]):
                print(list_of_all_hmm)
                print(alicia)
                res_list = []
                all_val_in_line = []
                for a_list in list_of_all_hmm:
                    temp_list = []
                    for a_val in a_list:
                        temp_list.append(alicia[a_val[0],a_val[1]])
                    res_list.append(temp_list)
                    all_val_in_line.extend(temp_list)
                print(list_of_all_hmm)
                print(res_list)
                print(min(all_val_in_line))
                #if min(alicia, key=a   licia.get) != max(alicia, key=alicia.get) and alicia.values().count(min(alicia, key=alicia.get)) == 1:
                if min(res_list[0]) != max(res_list[0]):# and alicia.values().count(min(alicia, key=alicia.get)) == 1:
                    kboom =  list_of_all_hmm[0][res_list[0].index(min(res_list[0]))]
                    print(kboom)
                    map[kboom[0]][kboom[1]] = str(open(kboom[0], kboom[1]))
                else:
                    pass
        except Exception as e:
            print(e)

    print(list_of_all_hmm)
    if sum([a_line.count("?") for a_line in map]) > 0 or (n > 0) :
        return "?"

    #print(f"mines {n}")
    #print(f"yo wtf {sum([a_line.count('x') for a_line in map])}")
    map = "\n".join([" ".join(a_row) for a_row in map])
    return map