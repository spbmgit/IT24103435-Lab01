from collections import deque
import heapq


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

            else:
                raise ValueError(
                    "Unknown search algorithm: "
                    + self.active_algo
                )

        if self.plan:
            return self.plan.pop(0)

        return "Stay"