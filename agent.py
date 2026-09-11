from collections import deque
import heapq
import math


class SearchAgent:
    """Search-based agent for BFS, DFS and UCS."""

    def __init__(self, algorithm="BFS"):
        self.plan = []
        self.active_algo = algorithm

    def get_neighbors(self, position, percept):
        x, y = position

        width, height = percept["grid_size"]
        walls = set(percept["walls"])

        moves = [
            ("Up", (x, y + 1)),
            ("Down", (x, y - 1)),
            ("Left", (x - 1, y)),
            ("Right", (x + 1, y))
        ]

        neighbors = []

        for action, new_position in moves:
            nx, ny = new_position

            if (
                0 <= nx < width
                and 0 <= ny < height
                and new_position not in walls
            ):
                neighbors.append((action, new_position))

        return neighbors

    def manhattan_distance(self, pos, goal):
        x1, y1 = pos
        x2, y2 = goal
        return abs(x1 - x2) + abs(y1 - y2)

    def euclidean_distance(self, pos, goal):
        x1, y1 = pos
        x2, y2 = goal
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def bfs_search(self, start, goal, percept):
        queue = deque()
        queue.append((start, []))

        reached = {start}

        while queue:
            current, path = queue.popleft()

            if current == goal:
                return path

            for action, neighbor in self.get_neighbors(
                current,
                percept
            ):
                if neighbor not in reached:
                    reached.add(neighbor)

                    new_path = path + [action]

                    queue.append(
                        (neighbor, new_path)
                    )

        return []

    def dfs_search(self, start, goal, percept):
        stack = []
        stack.append((start, []))

        reached = {start}

        while stack:
            current, path = stack.pop()

            if current == goal:
                return path

            neighbors = self.get_neighbors(
                current,
                percept
            )

            for action, neighbor in reversed(neighbors):
                if neighbor not in reached:
                    reached.add(neighbor)

                    new_path = path + [action]

                    stack.append(
                        (neighbor, new_path)
                    )

        return []

    def ucs_search(self, start, goal, percept):
        priority_queue = []
        heapq.heappush(
            priority_queue,
            (0, start, [])
        )

        reached = {
            start: 0
        }

        while priority_queue:
            cost, current, path = heapq.heappop(
                priority_queue
            )

            if current == goal:
                return path

            for action, neighbor in self.get_neighbors(
                current,
                percept
            ):
                new_cost = cost + 1

                if (
                    neighbor not in reached
                    or new_cost < reached[neighbor]
                ):
                    reached[neighbor] = new_cost

                    new_path = path + [action]

                    heapq.heappush(
                        priority_queue,
                        (
                            new_cost,
                            neighbor,
                            new_path
                        )
                    )

        return []

    def astar_search(self, start_pos, goal_pos, walls, grid_size, heuristic_type='manhattan'):
        priority_queue = []
        reached_states = set()

        width, height = grid_size
        walls = set(walls)

        def heuristic(pos):
            if heuristic_type == 'manhattan':
                return self.manhattan_distance(pos, goal_pos)
            return self.euclidean_distance(pos, goal_pos)

        g_start = 0
        f_start = g_start + heuristic(start_pos)

        heapq.heappush(
            priority_queue,
            (f_start, g_start, start_pos, [])
        )

        while priority_queue:
            f_cost, g_cost, current_pos, path_taken = heapq.heappop(
                priority_queue
            )

            if current_pos == goal_pos:
                return path_taken

            if current_pos in reached_states:
                continue

            reached_states.add(current_pos)

            x, y = current_pos
            moves = [
                ("Up", (x, y + 1)),
                ("Down", (x, y - 1)),
                ("Left", (x - 1, y)),
                ("Right", (x + 1, y))
            ]

            for action, neighbor in moves:
                nx, ny = neighbor

                if (
                    0 <= nx < width
                    and 0 <= ny < height
                    and neighbor not in walls
                    and neighbor not in reached_states
                ):
                    g_new = g_cost + 1
                    h_new = heuristic(neighbor)
                    f_new = g_new + h_new

                    new_path = path_taken + [action]

                    heapq.heappush(
                        priority_queue,
                        (f_new, g_new, neighbor, new_path)
                    )

        return []

    def find_closest_food(self, start, percept):
        food_positions = percept["all_food"]

        if not food_positions:
            return None

        closest_food = None
        shortest_distance = None

        for food in food_positions:
            distance = abs(
                start[0] - food[0]
            ) + abs(
                start[1] - food[1]
            )

            if (
                shortest_distance is None
                or distance < shortest_distance
            ):
                shortest_distance = distance
                closest_food = food

        return closest_food

    def sense_and_act(self, percept):
        if not self.plan:

            start = percept["agent_pos"]

            goal = self.find_closest_food(
                start,
                percept
            )

            if goal is None:
                return "Stay"

            if self.active_algo == "BFS":
                self.plan = self.bfs_search(
                    start,
                    goal,
                    percept
                )

            elif self.active_algo == "DFS":
                self.plan = self.dfs_search(
                    start,
                    goal,
                    percept
                )

            elif self.active_algo == "UCS":
                self.plan = self.ucs_search(
                    start,
                    goal,
                    percept
                )

            elif self.active_algo == "AStar":
                walls = percept["walls"]
                grid_size = percept["grid_size"]

                self.plan = self.astar_search(
                    start,
                    goal,
                    walls,
                    grid_size,
                    heuristic_type='manhattan'
                )

            else:
                raise ValueError(
                    "Unknown search algorithm: "
                    + self.active_algo
                )

        if self.plan:
            return self.plan.pop(0)

        return "Stay"


if __name__ == "__main__":
    agent = SearchAgent()
    start = (0, 0)
    goal = (3, 4)

    print("Manhattan distance:", agent.manhattan_distance(start, goal))
    print("Euclidean distance:", agent.euclidean_distance(start, goal))