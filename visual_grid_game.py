import random
import tkinter as tk


class VisualGridHuntGame:
    """Grid environment used for the practical."""

    def __init__(
        self,
        width=10,
        height=10,
        num_food=10,
        num_opponents=0,
        custom_walls=None
    ):
        self.width = width
        self.height = height
        self.agent_pos = [0, 0]

        if custom_walls is not None:
            self.walls = set(custom_walls)
        else:
            self.walls = {
                (2, 2),
                (2, 3),
                (5, 5),
                (6, 5),
                (3, 7)
            }

        self.food_positions = set()

        while len(self.food_positions) < num_food:
            fx = random.randint(0, self.width - 1)
            fy = random.randint(0, self.height - 1)

            position = (fx, fy)

            if position != (0, 0) and position not in self.walls:
                self.food_positions.add(position)

        self.opponents = []

        while len(self.opponents) < num_opponents:
            ox = random.randint(0, self.width - 1)
            oy = random.randint(0, self.height - 1)

            opponent = [ox, oy]

            if (
                tuple(opponent) != (0, 0)
                and tuple(opponent) not in self.walls
                and tuple(opponent) not in self.food_positions
            ):
                self.opponents.append(opponent)

        self.score = 0
        self.steps = 0
        self.collision = False

    def get_percept(self) -> dict:
        return {
            "agent_pos": tuple(self.agent_pos),
            "grid_size": (self.width, self.height),
            "walls": list(self.walls),
            "all_food": list(self.food_positions),
            "opponent_positions": [
                tuple(opponent) for opponent in self.opponents
            ],
            "score": self.score,
            "remaining_food": len(self.food_positions),
            "collision": self.collision
        }

    def execute_action(self, action: str):
        self.steps += 1

        new_pos = list(self.agent_pos)

        if action == "Up":
            new_pos[1] = min(
                self.height - 1,
                new_pos[1] + 1
            )

        elif action == "Down":
            new_pos[1] = max(
                0,
                new_pos[1] - 1
            )

        elif action == "Left":
            new_pos[0] = max(
                0,
                new_pos[0] - 1
            )

        elif action == "Right":
            new_pos[0] = min(
                self.width - 1,
                new_pos[0] + 1
            )

        if tuple(new_pos) in self.walls:
            self.score -= 5
        else:
            self.agent_pos = new_pos

        current_position = tuple(self.agent_pos)

        if current_position in self.food_positions:
            self.food_positions.remove(current_position)
            self.score += 20

        for opponent in self.opponents:
            move = random.choice(
                ["Up", "Down", "Left", "Right", "Stay"]
            )

            if move == "Up" and opponent[1] < self.height - 1:
                opponent[1] += 1

            elif move == "Down" and opponent[1] > 0:
                opponent[1] -= 1

            elif move == "Left" and opponent[0] > 0:
                opponent[0] -= 1

            elif move == "Right" and opponent[0] < self.width - 1:
                opponent[0] += 1

            if opponent == self.agent_pos:
                self.score -= 50
                self.collision = True

    def is_done(self) -> bool:
        return (
            len(self.food_positions) == 0
            or self.steps >= 60
            or self.collision
        )


class GridGameGUI:
    """Tkinter interface for the grid environment."""

    def __init__(
        self,
        root,
        width=12,
        height=12,
        num_food=15,
        num_opponents=0,
        walls=None
    ):
        self.root = root
        self.root.title(
            "IT3012 - Practical 03"
        )

        self.env = VisualGridHuntGame(
            width=width,
            height=height,
            num_food=num_food,
            num_opponents=num_opponents,
            custom_walls=walls
        )

        max_canvas_dim = 600

        self.cell_size = max(
            20,
            min(
                max_canvas_dim // self.env.width,
                max_canvas_dim // self.env.height
            )
        )

        canvas_width = self.env.width * self.cell_size
        canvas_height = self.env.height * self.cell_size

        self.canvas = tk.Canvas(
            root,
            width=canvas_width,
            height=canvas_height,
            bg="white"
        )

        self.canvas.pack()

        self.label = tk.Label(
            root,
            text="Score: 0 | Steps: 0",
            font=("Arial", 14)
        )

        self.label.pack(pady=10)

        self.btn = tk.Button(
            root,
            text="Start Simulation",
            command=self.run_loop,
            font=("Arial", 12)
        )

        self.btn.pack(pady=5)

        self.draw_grid()

    def draw_grid(self):
        self.canvas.delete("all")

        for x in range(self.env.width):
            for y in range(self.env.height):

                x1 = x * self.cell_size
                y1 = (
                    self.env.height - 1 - y
                ) * self.cell_size

                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                if (x, y) in self.env.walls:
                    color = "#64748b"
                else:
                    color = "#f1f5f9"

                self.canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill=color,
                    outline="#cbd5e1"
                )

        for fx, fy in self.env.food_positions:

            offset = self.cell_size * 0.25

            x1 = (
                fx * self.cell_size
                + offset
            )

            y1 = (
                (self.env.height - 1 - fy)
                * self.cell_size
                + offset
            )

            self.canvas.create_oval(
                x1,
                y1,
                x1 + self.cell_size * 0.5,
                y1 + self.cell_size * 0.5,
                fill="#f59e0b",
                outline="#d97706"
            )

        for ox, oy in self.env.opponents:

            offset = self.cell_size * 0.2

            x1 = (
                ox * self.cell_size
                + offset
            )

            y1 = (
                (self.env.height - 1 - oy)
                * self.cell_size
                + offset
            )

            self.canvas.create_rectangle(
                x1,
                y1,
                x1 + self.cell_size * 0.6,
                y1 + self.cell_size * 0.6,
                fill="#990000",
                outline="#7a0000"
            )

        ax, ay = self.env.agent_pos

        offset = self.cell_size * 0.15

        x1 = (
            ax * self.cell_size
            + offset
        )

        y1 = (
            (self.env.height - 1 - ay)
            * self.cell_size
            + offset
        )

        self.canvas.create_oval(
            x1,
            y1,
            x1 + self.cell_size * 0.7,
            y1 + self.cell_size * 0.7,
            fill="#000066",
            outline="#1e3a8a"
        )

    def run_loop(self):
        self.btn.config(state="disabled")

        def step():
            if not self.env.is_done():

                percept = self.env.get_percept()

                action = random.choice(
                    ["Up", "Down", "Left", "Right"]
                )

                self.env.execute_action(action)

                self.draw_grid()

                self.label.config(
                    text=(
                        f"Score: {self.env.score} | "
                        f"Steps: {self.env.steps} | "
                        f"Action: {action}"
                    )
                )

                self.root.after(
                    250,
                    step
                )

            else:
                if self.env.collision:
                    end_text = (
                        "Collision! Game Over! "
                        f"Final Score: {self.env.score}"
                    )
                else:
                    end_text = (
                        "Finished! "
                        f"Final Score: {self.env.score}"
                    )

                self.label.config(
                    text=end_text
                )

                self.btn.config(
                    state="normal"
                )

        step()


if __name__ == "__main__":
    root = tk.Tk()

    app = GridGameGUI(
        root,
        width=12,
        height=12,
        num_food=15,
        num_opponents=0
    )

    root.mainloop()