import math

import arcade
import enemy
from DataStructures.AbstractDataStructures import PriorityQueue

"""
Goes through the whole grid plotting all the barriers that enemy's path needs to avoid
"""


class GameBarriers:

    def __init__(self, enemy, walls, grid_size, top, left, right, bottom):

        self.enemy = enemy
        self.walls = walls
        self.grid_size = grid_size
        self.top = int(top // grid_size)
        self.bottom = int(bottom // grid_size)
        self.right = int(right // grid_size)
        self.left = int(left // grid_size)
        self.barriers = set()
        self.original_enemy_pos = self.enemy.position

        for y in range(self.bottom, self.top + 1):
            for x in range(self.left, self.right + 1):
                temp = x, y
                potential_pos = expand(temp, grid_size)
                self.enemy.position = potential_pos

                if len(arcade.check_for_collision_with_list(self.enemy, self.walls)) > 0:
                    self.barriers.add(temp)

        self.enemy.position = self.original_enemy_pos
        self.barriers = sorted(self.barriers)


class Graph:

    def __init__(self, barriers: GameBarriers):
        self.barriers = barriers
        self.left = barriers.left
        self.top = barriers.top
        self.bottom = barriers.bottom
        self.right = barriers.right
        self.moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    def cost_of_move(self, start, end):
        start = (int(start[0]),int(start[1]))
        end = (int(end[0]),int(end[1]))
        if end in self.barriers.barriers:
            return 100000

        if start[0] == end[0] or start[1] == end[1]:
            return 1
        else:
            return 1.42

    def get_list_of_neighbors(self, coordinate):

        list_of_neighbors = []

        for i in self.moves:
            newX = coordinate[0] + i[0]
            newY = coordinate[1] + i[1]
            if newX > self.right or newX < self.left or newY > self.top or newY < self.bottom:
                #print("in here")

                continue
            list_of_neighbors.append((newX, newY))
        return list_of_neighbors


def a_star_search(enemy, goal_location, barriers: GameBarriers):
    graph = Graph(barriers)
    temp = enemy.position
    node = (int(temp[0] // barriers.grid_size), int(temp[1] // barriers.grid_size))
    collapsed_goal = (int(goal_location[0] // barriers.grid_size), int(goal_location[1] // barriers.grid_size))

    if enemy.position == goal_location:
        return None

    frontier = PriorityQueue(reverse=True)

    frontier.enqueue((node, [], 0), 0)

    explored = []
    counter = 0
    while frontier.size > 0:
        counter += 1
        if counter == 100:
            return None
        node_state, node_actions, node_cost = frontier.dequeue()

        if collapsed_goal[0] == node_state[0] and collapsed_goal[1] == node_state[1]:
            path = [(x[0]*barriers.grid_size, x[1]*barriers.grid_size) for x in node_actions]
            return path

        explored.append(node_state)
        child_nodes = graph.get_list_of_neighbors(node_state)

        for child_node in child_nodes:
            if child_node not in explored:
                actions = node_actions + [child_node]
                cost = graph.cost_of_move(node_state, child_node)
                heuristic_cost = heuristic(child_node, collapsed_goal)
                total_cost = int(node_cost + cost + heuristic_cost)
                child_cost = int(cost + node_cost)
                frontier.enqueue((child_node, actions, child_cost), total_cost)


def heuristic(position, goal):
    "The Manhattan distance heuristic for a PositionSearchProblem"
    xy1 = position
    xy2 = goal
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])


def collapse(pos, grid_size):
    return int(pos[0] // grid_size), int(pos[1] // grid_size)


def expand(pos, grid_size):
    return int(pos[0] * grid_size), int(pos[1] * grid_size)