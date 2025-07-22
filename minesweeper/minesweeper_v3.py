TOTO = 0
MAP_X_LEN = 0
MAP_Y_LEN = 0
res_map = None


class cell:
    def __init__(self, value :int, coord_x: int, coord_y: int) -> None:
        self.value = value
        self.x = coord_x
        self.y = coord_y
        self.proba = 0
        self.neighboors = [(self.x + x, self.y+y) for x, y in [(-1,-1),(-1,-0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)] if (self.x + x)in range(MAP_X_LEN) and (self.y+y) in range(MAP_Y_LEN)]

    def __repr__(self):
        return f'The cell of value {self.value} is ({self.x},{self.y})'

    def update_value(self,map):
        self.value = map[self.x][self.y]

    def return_question_mark_coords(self, map):
        vals = {(j,v):map[j][v] for j,v in self.neighboors}
        return [coords for coords,val in vals.items() if val=="?"]

    def return_x_mark_coords(self, map):
        vals = {(j,v):map[j][v] for j,v in self.neighboors}
        return [coords for coords,val in vals.items() if val=="x"]

    def get_neighboors_coord(self):
        return self.neighboors

    def is_cell_in_range_of_active_cell(self, cells:list):
        # all_cords = []
        # for a_cell in cells:
        #     all_cords.extend(a_cell.get_neighboors_coord())
        #if all_cords.count((self.x,self.y)) == 1:
        tab = []
        for a_cell in cells:
            if (self.x,self.y) in a_cell.get_neighboors_coord():
                tab.append(a_cell)
        return tab
def open_coords(coords:list, map):
    for a_coord in coords:
        map[a_coord[0]][a_coord[1]] = str(open(a_coord[0], a_coord[1]))
    return map

def mark_coords(coords:list, map):
    for a_coord in coords:
        map[a_coord[0]][a_coord[1]] = "x"
    return map

def pick_one(cells:list, map, n):
    value_cells = [cell for cell in cells if cell.value not in ["?","x","0"]]
    for a_cell in value_cells:
        print(value_cells)
        next_cells = a_cell.is_cell_in_range_of_active_cell(value_cells)
        print("nxt :", next_cells)
        for next_cell in next_cells:
            if next_cell:
                first_val = int(a_cell.value) - len(a_cell.return_x_mark_coords(map)) # remove the "x" neighbors
                second_val = int(next_cell.value) - len(next_cell.return_x_mark_coords(map))
                setty_temp = set(a_cell.return_question_mark_coords(map)) - set(next_cell.return_question_mark_coords(map))
                if (first_val - second_val) == len(setty_temp):
                    print(setty_temp)
                    print(list(set(next_cell.return_question_mark_coords(map)) - set(a_cell.return_question_mark_coords(map))))
                    #exit()
                    #mark_coords([(cell[0],cell[1]) for cell in list(set.intersection(set(next_cell.return_question_mark_coords(map)), set(a_cell.return_question_mark_coords(map))))], map)
                    #print(list(set(next_cell.return_question_mark_coords(map)) - set(a_cell.return_question_mark_coords(map))))
                    open_coords([(cell[0],cell[1]) for cell in list(set(next_cell.return_question_mark_coords(map)) - set(a_cell.return_question_mark_coords(map)))], map)
                    return solve_mine(map, n)




def get_mines(cells:list):
    return [cell for cell in cells if cell.value == "x"]

def get_question_marks(cells:list):
    return [cell for cell in cells if cell.value == "?"]

def get_mines_on_map(map):
    res = []
    for coord_x in range(len(map)):
        for coord_y in range(len(map[coord_x])):
            if map[coord_x][coord_y] == "x":
                res.append((coord_x, coord_y))
    return res

def get_question_marks_on_map(map):
    res = []
    for coord_x in range(len(map)):
        for coord_y in range(len(map[coord_x])):
            if map[coord_x][coord_y] == "?":
                res.append((coord_x, coord_y))
    return res


def solve_mine(map, n):
    if isinstance(map, str):
        map = [a_char.split(" ") for a_char in [a_line for a_line in map.split("\n")]]
    global MAP_X_LEN, MAP_Y_LEN
    if MAP_X_LEN == 0:
        MAP_X_LEN = len(map)
        MAP_Y_LEN = len(map[0])

    print("\n".join([" ".join(a_row) for a_row in map]))


    prev_counter_question_marks = len(get_question_marks_on_map(map)) +1
    counter_question_marks = len(get_question_marks_on_map(map))

    while counter_question_marks < prev_counter_question_marks:
        cells = []
        for coord_x in range(len(map)):
            for coord_y in range(len(map[coord_x])):
                cells.append(cell(map[coord_x][coord_y], coord_x, coord_y))
        prev_counter_question_marks = counter_question_marks
        for index, a_cell in enumerate(cells):
            if a_cell.return_question_mark_coords(map) == []:
                cells.pop(index)
                continue
            if a_cell.value == "0":
                map = open_coords(a_cell.return_question_mark_coords(map), map)
                continue
            elif a_cell.value == "?":
                continue
            elif a_cell.value == str(len(a_cell.return_x_mark_coords(map)) + len(a_cell.return_question_mark_coords(map))):
                map = mark_coords(a_cell.return_question_mark_coords(map), map)
            elif a_cell.value == str(len(a_cell.return_x_mark_coords(map))):
                map = open_coords(a_cell.return_question_mark_coords(map), map)
            # else:
            #     print(a_cell.value)
            #     print(a_cell.x," " ,a_cell.y)
            #     print(a_cell.return_x_mark_coords(map))
            #     print(a_cell.return_question_mark_coords(map))
            #     print("\n".join([" ".join(a_row) for a_row in map]))


            for a_cell in cells:
                a_cell.update_value(map)
        counter_question_marks = len(get_question_marks_on_map(map))

    #kekw
    last_question_marks = [cell for cell in cells if cell.value == "?"]
    global TOTO


    # work with mine counter
    mines = get_mines_on_map(map)
    question_marks = get_question_marks_on_map(map)
    if (n - len(mines)) == 0:
        open_coords([(cell.x,cell.y) for cell in question_marks], map)
        return "\n".join([" ".join(a_row) for a_row in map])
    elif len(question_marks) == (n-len(mines)):
        mark_coords([(cell.x,cell.y) for cell in mines], map)
        return "\n".join([" ".join(a_row) for a_row in map])
    elif len(last_question_marks) > 1:
        if TOTO > 10:
            #return "\n".join([" ".join(a_row) for a_row in map])
            return "?"
    #else:
        #return "\n".join([" ".join(a_row) for a_row in map])
    pick_one(cells, map, n)
    map = "\n".join([" ".join(a_row) for a_row in map])
    return map

def open(coord_x, coord_y):
    return res_map[coord_x][coord_y]

if __name__ == "__main__":
    print("prout")
    gamemap = """
? ? ? ? ? ?
? ? ? ? ? ?
? ? ? 0 ? ?
? ? ? ? ? ?
? ? ? ? ? ?
0 0 0 ? ? ?
""".strip()
    result = """
1 x 1 1 x 1
2 2 2 1 2 2
2 x 2 0 1 x
2 x 2 1 2 2
1 1 1 1 x 1
0 0 0 1 1 1
""".strip()
    res_map = [a_char.split(" ") for a_char in [a_line for a_line in result.split("\n")]]

    if solve_mine(gamemap, 6) == result:
        print("level 1 done")
    else:
        print("ko")
        print(solve_mine(gamemap, 6))

#         gamemap = """
# 0 ? ?
# 0 ? ?
# """.strip()
#         result = """
# 0 1 x
# 0 1 1
# """.strip()
#         game.read(gamemap, result)
#         makeAssertion(solve_mine(gamemap, game.count), "?")

#         gamemap = """
# ? ? ? ? 0 0 0
# ? ? ? ? 0 ? ?
# ? ? ? 0 0 ? ?
# ? ? ? 0 0 ? ?
# 0 ? ? ? 0 0 0
# 0 ? ? ? 0 0 0
# 0 ? ? ? 0 ? ?
# 0 0 0 0 0 ? ?
# 0 0 0 0 0 ? ?
# """.strip()
#         result = """
# 1 x x 1 0 0 0
# 2 3 3 1 0 1 1
# 1 x 1 0 0 1 x
# 1 1 1 0 0 1 1
# 0 1 1 1 0 0 0
# 0 1 x 1 0 0 0
# 0 1 1 1 0 1 1
# 0 0 0 0 0 1 x
# 0 0 0 0 0 1 1
# """.strip()
#         game.read(gamemap, result)
#         makeAssertion(solve_mine(gamemap, game.count), result)

#         gamemap = """
# ? ? 0 ? ? ? 0 0 ? ? ? 0 0 0 0 ? ? ? 0
# ? ? 0 ? ? ? 0 0 ? ? ? 0 0 0 0 ? ? ? ?
# ? ? 0 ? ? ? ? ? ? ? ? 0 0 0 0 ? ? ? ?
# 0 ? ? ? ? ? ? ? ? ? ? 0 0 0 0 0 ? ? ?
# 0 ? ? ? ? ? ? ? ? ? 0 0 0 0 0 0 0 0 0
# 0 ? ? ? 0 0 0 ? ? ? 0 0 0 0 0 0 0 0 0
# 0 0 0 0 0 0 0 ? ? ? ? ? ? ? 0 0 0 0 0
# 0 0 0 0 0 0 0 0 0 0 ? ? ? ? 0 0 0 0 0
# 0 0 ? ? ? 0 ? ? ? 0 ? ? ? ? 0 0 0 0 0
# 0 0 ? ? ? ? ? ? ? 0 0 0 0 0 0 ? ? ? 0
# 0 0 ? ? ? ? ? ? ? ? ? 0 0 0 0 ? ? ? 0
# 0 0 0 0 ? ? ? ? ? ? ? 0 0 0 0 ? ? ? 0
# 0 0 0 0 0 ? ? ? ? ? ? 0 0 0 0 0 ? ? ?
# 0 0 ? ? ? ? ? ? 0 0 0 0 0 0 0 0 ? ? ?
# 0 0 ? ? ? ? ? ? ? 0 0 0 0 0 0 0 ? ? ?
# 0 0 ? ? ? ? ? ? ? ? 0 0 0 0 0 0 0 ? ?
# 0 0 0 0 0 0 ? ? ? ? 0 0 0 ? ? ? 0 ? ?
# 0 0 0 ? ? ? ? ? ? ? 0 0 0 ? ? ? ? ? ?
# 0 0 0 ? ? ? ? ? 0 0 0 ? ? ? ? ? ? ? ?
# 0 0 0 ? ? ? ? ? 0 0 0 ? ? ? 0 ? ? ? ?
# 0 0 0 0 ? ? ? ? ? ? ? ? ? ? 0 ? ? ? ?
# 0 0 0 0 ? ? ? ? ? ? ? ? ? ? 0 ? ? ? ?
# 0 0 0 0 ? ? ? ? ? ? ? ? ? ? 0 ? ? ? ?
# """.strip()
#         result = """
# 1 1 0 1 1 1 0 0 1 1 1 0 0 0 0 1 1 1 0
# x 1 0 1 x 1 0 0 2 x 2 0 0 0 0 1 x 2 1
# 1 1 0 2 3 3 1 1 3 x 2 0 0 0 0 1 2 x 1
# 0 1 1 2 x x 1 2 x 3 1 0 0 0 0 0 1 1 1
# 0 1 x 2 2 2 1 3 x 3 0 0 0 0 0 0 0 0 0
# 0 1 1 1 0 0 0 2 x 2 0 0 0 0 0 0 0 0 0
# 0 0 0 0 0 0 0 1 1 1 1 2 2 1 0 0 0 0 0
# 0 0 0 0 0 0 0 0 0 0 1 x x 1 0 0 0 0 0
# 0 0 1 1 1 0 1 1 1 0 1 2 2 1 0 0 0 0 0
# 0 0 1 x 2 1 3 x 2 0 0 0 0 0 0 1 1 1 0
# 0 0 1 1 2 x 3 x 3 1 1 0 0 0 0 1 x 1 0
# 0 0 0 0 1 2 3 2 2 x 1 0 0 0 0 1 1 1 0
# 0 0 0 0 0 1 x 1 1 1 1 0 0 0 0 0 1 1 1
# 0 0 1 1 2 2 2 1 0 0 0 0 0 0 0 0 1 x 1
# 0 0 1 x 2 x 2 1 1 0 0 0 0 0 0 0 1 1 1
# 0 0 1 1 2 1 3 x 3 1 0 0 0 0 0 0 0 1 1
# 0 0 0 0 0 0 2 x x 1 0 0 0 1 1 1 0 1 x
# 0 0 0 1 1 1 1 2 2 1 0 0 0 1 x 1 1 2 2
# 0 0 0 1 x 3 2 1 0 0 0 1 1 2 1 1 1 x 2
# 0 0 0 1 2 x x 1 0 0 0 1 x 1 0 1 2 3 x
# 0 0 0 0 1 2 2 1 1 1 1 1 1 1 0 1 x 3 2
# 0 0 0 0 1 1 1 1 2 x 1 1 1 1 0 2 3 x 2
# 0 0 0 0 1 x 1 1 x 2 1 1 x 1 0 1 x 3 x
# """.strip()
#         game.read(gamemap, result)
#         makeAssertion(solve_mine(gamemap, game.count), "?")

#         gamemap = """
# 0 0 0 0 0 0 0 0 ? ? ? ? ? 0 ? ? ? 0 ? ? ?
# 0 0 0 0 0 0 0 0 ? ? ? ? ? 0 ? ? ? ? ? ? ?
# 0 0 0 0 0 0 0 0 0 0 ? ? ? 0 ? ? ? ? ? ? ?
# 0 0 0 0 0 ? ? ? 0 0 ? ? ? 0 ? ? ? ? ? ? 0
# ? ? 0 0 0 ? ? ? 0 ? ? ? ? 0 0 ? ? ? ? ? ?
# ? ? 0 0 0 ? ? ? 0 ? ? ? 0 0 0 ? ? ? ? ? ?
# ? ? ? 0 0 0 0 0 0 ? ? ? 0 0 0 0 0 0 ? ? ?
# ? ? ? 0 0 0 0 0 0 0 ? ? ? ? 0 0 ? ? ? 0 0
# ? ? ? 0 0 0 0 0 0 0 ? ? ? ? 0 0 ? ? ? 0 0
# """.strip()
#         result = """
# 0 0 0 0 0 0 0 0 1 x x 2 1 0 1 x 1 0 1 2 x
# 0 0 0 0 0 0 0 0 1 2 3 x 1 0 2 2 2 1 2 x 2
# 0 0 0 0 0 0 0 0 0 0 2 2 2 0 1 x 1 1 x 2 1
# 0 0 0 0 0 1 1 1 0 0 1 x 1 0 1 2 2 2 1 1 0
# 1 1 0 0 0 1 x 1 0 1 2 2 1 0 0 1 x 1 1 1 1
# x 1 0 0 0 1 1 1 0 1 x 1 0 0 0 1 1 1 1 x 1
# 2 2 1 0 0 0 0 0 0 1 1 1 0 0 0 0 0 0 1 1 1
# 1 x 1 0 0 0 0 0 0 0 1 2 2 1 0 0 1 1 1 0 0
# 1 1 1 0 0 0 0 0 0 0 1 x x 1 0 0 1 x 1 0 0
# """.strip()
#         game.read(gamemap, result)
#         makeAssertion(solve_mine(gamemap, game.count), "?")

# """