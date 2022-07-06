def get_three_points_average(points):
    x = 0
    y = 0
    l = len(points)
    for p in points:
        x += p[0]
        y += p[1]
    x /= l
    y /= l
    return x, y

def get_player_monster_midpoint(player, monster):
    return player[0] - monster[0], player[1] - monster[1]