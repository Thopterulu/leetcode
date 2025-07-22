#from preloaded import open
def open(*args, **kwargs):
    return "x"


class cell:
    def __init__(self, value :int, coord_x: int, coord_y: int) -> None:
        self.value = value
        self.x = coord_x
        self.y = coord_y

    def update_value(self,map):
        self.value = map[self.x][self.y]

    def return_question_mark_coords(self, map):
        coords = [(self.x + x, self.y+y) for x, y in [(-1,-1),(-1,-0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)] if (self.x + x)in range(len(map)) and (self.y+y) in range(len(map[self.x]))]
        vals = {(j,v):map[j][v] for j,v in coords}
        return [coords for coords,val in vals.items() if val=="?"]

def open_coords(coords:list, map):
    for a_coord in coords:
        map[a_coord[0]][a_coord[1]] = str(open(a_coord[0], a_coord[1]))
    return map



def solve_mine(map, n):
    map = [a_char.split(" ") for a_char in [a_line for a_line in map.split("\n")]]

    cells = []
    for coord_x in range(len(map)):
        for coord_y in range(len(map[coord_x])):
            cells.append(cell(map[coord_x][coord_y], coord_x, coord_y))
    print(len(cells))

    for i in range (3):
        for index, a_cell in enumerate(cells):
            if a_cell.return_question_mark_coords(map) == []:
                cells.pop(index)
                continue
            if a_cell.value == "0" or (a_cell.value == str(len(a_cell.return_question_mark_coords(map)))):
                map = open_coords(a_cell.return_question_mark_coords(map), map)
        for a_cell in cells:
            a_cell.update_value(map)
    print(len(cells))



    map = "\n".join([" ".join(a_row) for a_row in map])
    return map

if __name__ == "__main__":
    gamemap = """
? ? ? ? ? ?
? ? ? ? ? ?
? ? ? 0 ? ?
? ? ? ? ? ?
? ? ? ? ? ?
0 0 0 ? ? ?
""".strip()
    print(solve_mine(gamemap, 6))