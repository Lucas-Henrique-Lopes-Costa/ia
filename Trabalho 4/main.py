import tkinter as tk
from tkinter import ttk, messagebox
import collections
import heapq
import time
import threading
import queue

# Estado final do Jogo dos Oito
GOAL_STATE = (1, 2, 3, 8, 0, 4, 7, 6, 5)

# Estado inicial
INITIAL_BOARD = (2, 0, 3, 1, 7, 4, 6, 8, 5)

# Mapa de posições do objetivo para cálculo da heurística
GOAL_POSITIONS = {tile: i for i, tile in enumerate(GOAL_STATE) if tile != 0}


class PuzzleState:
    
    """Representa um estado do Jogo dos Oito."""

    def __init__(self, board, parent=None, action=None, cost=0, heuristic=0):
        self.board = board
        self.parent = parent
        self.action = action
        self.cost = cost
        self.heuristic = heuristic
        self.f_cost = cost + heuristic

    def __lt__(self, other):
        return self.f_cost < other.f_cost

    def __eq__(self, other):
        return self.board == other.board

    def __hash__(self):
        return hash(self.board)

    def get_blank_position(self):
        return self.board.index(0)

    def get_neighbors(self):
        i = self.get_blank_position()
        r, c = divmod(i, 3)
        possible_moves = []
        if r > 0:
            possible_moves.append(i - 3)
        if r < 2:
            possible_moves.append(i + 3)
        if c > 0:
            possible_moves.append(i - 1)
        if c < 2:
            possible_moves.append(i + 1)

        neighbors = []
        for move_pos in possible_moves:
            new_board_list = list(self.board)
            new_board_list[i], new_board_list[move_pos] = (
                new_board_list[move_pos],
                new_board_list[i],
            )
            new_board = tuple(new_board_list)
            action = self._get_action_name(i, move_pos)
            neighbors.append(PuzzleState(new_board, self, action, self.cost + 1))
        return neighbors

    def _get_action_name(self, old_pos, new_pos):
        if new_pos == old_pos - 3:
            return "Cima"
        if new_pos == old_pos + 3:
            return "Baixo"
        if new_pos == old_pos - 1:
            return "Esquerda"
        if new_pos == old_pos + 1:
            return "Direita"
        return "Desconhecida"

    @staticmethod
    def is_solvable(board):
        """Verifica se um estado inicial é solúvel (objetivo tem paridade ímpar)."""
        inversions = 0
        board_list = [i for i in board if i != 0]
        n = len(board_list)
        for i in range(n):
            for j in range(i + 1, n):
                if board_list[i] > board_list[j]:
                    inversions += 1
        return inversions % 2 != 0


def get_solution_path(state):
    path = []
    current = state
    while current:
        path.append(current)
        current = current.parent
    return path[::-1]


def bfs_search(initial_board):
    if not PuzzleState.is_solvable(initial_board):
        return None, 0, 0

    initial_state = PuzzleState(initial_board)
    if initial_state.board == GOAL_STATE:
        return get_solution_path(initial_state), 0, 1

    queue = collections.deque([initial_state])
    visited = {initial_state.board}
    nodes_explored = 0
    start_time = time.time()

    while queue:
        current_state = queue.popleft()
        nodes_explored += 1

        for neighbor in current_state.get_neighbors():
            if neighbor.board not in visited:
                if neighbor.board == GOAL_STATE:
                    end_time = time.time()
                    return (
                        get_solution_path(neighbor),
                        end_time - start_time,
                        nodes_explored + 1,
                    )

                visited.add(neighbor.board)
                queue.append(neighbor)
    end_time = time.time()
    return None, end_time - start_time, nodes_explored


def manhattan_distance(board):
    distance = 0
    for i in range(9):
        tile = board[i]
        if tile == 0:
            continue
        r_curr, c_curr = divmod(i, 3)
        goal_index = GOAL_POSITIONS[tile]
        r_goal, c_goal = divmod(goal_index, 3)
        distance += abs(r_curr - r_goal) + abs(c_curr - c_goal)
    return distance


def a_star_search(initial_board):
    if not PuzzleState.is_solvable(initial_board):
        return None, 0, 0

    h = manhattan_distance(initial_board)
    initial_state = PuzzleState(initial_board, cost=0, heuristic=h)

    priority_queue = [initial_state]
    g_costs = {initial_state.board: 0}
    nodes_explored = 0
    start_time = time.time()

    while priority_queue:
        current_state = heapq.heappop(priority_queue)
        nodes_explored += 1

        if current_state.board == GOAL_STATE:
            end_time = time.time()
            return (
                get_solution_path(current_state),
                end_time - start_time,
                nodes_explored,
            )

        for neighbor in current_state.get_neighbors():
            new_g_cost = current_state.cost + 1

            if neighbor.board in g_costs and new_g_cost >= g_costs[neighbor.board]:
                continue

            g_costs[neighbor.board] = new_g_cost
            h = manhattan_distance(neighbor.board)
            neighbor.cost = new_g_cost
            neighbor.heuristic = h
            neighbor.f_cost = new_g_cost + h
            heapq.heappush(priority_queue, neighbor)

    end_time = time.time()
    return None, end_time - start_time, nodes_explored


class PuzzleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Solucionador do Jogo dos Oito (GCC 128)")
        self.root.geometry("450x700")

        self.solution_path = []
        self.current_step = 0
        self.result_queue = queue.Queue()
        self.algorithm_var = tk.StringVar(value="a_star")

        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 12))
        self.style.configure("TRadiobutton", font=("Arial", 12))
        self.style.configure("TLabel", font=("Arial", 12))
        self.style.configure("Title.TLabel", font=("Arial", 16, "bold"))
        self.style.configure(
            "Status.TLabel", font=("Arial", 10), relief="sunken", anchor="w"
        )
        self.style.configure(
            "Grid.TLabel",
            font=("Arial", 48, "bold"),
            background="white",
            borderwidth=2,
            relief="solid",
            anchor="center",
        )
        self.style.configure(
            "Empty.Grid.TLabel",
            font=("Arial", 48, "bold"),
            background="#eee",
            borderwidth=2,
            relief="solid",
            anchor="center",
        )
        self.style.configure(
            "Stats.TLabel", font=("Arial", 11, "bold"), anchor="center"
        )

        self.create_widgets()
        self.reset_puzzle()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(
            main_frame, text="Jogo dos Oito - Solucionador", style="Title.TLabel"
        ).pack(pady=(0, 15))

        grid_frame = ttk.Frame(main_frame)
        grid_frame.pack(pady=10)
        self.grid_labels = []
        for i in range(9):
            label = ttk.Label(grid_frame, text="", width=4, style="Grid.TLabel")
            label.grid(row=i // 3, column=i % 3, sticky="nsew", ipadx=10, ipady=10)
            self.grid_labels.append(label)

        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=10)

        ttk.Label(control_frame, text="Escolha o Algoritmo:").pack(
            side=tk.LEFT, padx=(0, 10)
        )
        self.radio_a_star = ttk.Radiobutton(
            control_frame,
            text="A* (Informado)",
            variable=self.algorithm_var,
            value="a_star",
        )
        self.radio_a_star.pack(side=tk.LEFT, padx=5)
        self.radio_bfs = ttk.Radiobutton(
            control_frame, text="BFS (Cego)", variable=self.algorithm_var, value="bfs"
        )
        self.radio_bfs.pack(side=tk.LEFT, padx=5)

        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=5)

        self.solve_button = ttk.Button(
            action_frame,
            text="Resolver",
            command=self.start_solve_thread,
            style="TButton",
        )
        self.solve_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

        self.reset_button = ttk.Button(
            action_frame, text="Resetar", command=self.reset_puzzle, style="TButton"
        )
        self.reset_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

        nav_frame = ttk.Frame(main_frame)
        nav_frame.pack(fill=tk.X, pady=10)

        self.prev_button = ttk.Button(
            nav_frame, text="<< Anterior", command=self.prev_step, state="disabled"
        )
        self.prev_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

        stats_frame = ttk.Frame(nav_frame)
        stats_frame.pack(side=tk.LEFT, expand=True, fill=tk.X)

        self.step_label = ttk.Label(stats_frame, text="Passo: - / -", anchor="center")
        self.step_label.pack(fill=tk.X)

        self.nodes_label = ttk.Label(
            stats_frame, text="Nós Explorados: -", style="Stats.TLabel"
        )
        self.nodes_label.pack(fill=tk.X, pady=(5, 0))

        self.next_button = ttk.Button(
            nav_frame, text="Próximo >>", command=self.next_step, state="disabled"
        )
        self.next_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

        self.status_label = ttk.Label(
            self.root,
            text=" Pronto para resolver. Use A* (rápido) ou BFS (lento, mas ótimo).",
            style="Status.TLabel",
        )
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

    def update_grid(self, board_tuple):
        for i, val in enumerate(board_tuple):
            if val == 0:
                self.grid_labels[i].config(text="", style="Empty.Grid.TLabel")
            else:
                self.grid_labels[i].config(text=str(val), style="Grid.TLabel")

    def reset_puzzle(self):
        self.solution_path = []
        self.current_step = 0
        self.update_grid(INITIAL_BOARD)

        self.step_label.config(text="Passo: - / -")
        self.status_label.config(
            text=" Pronto. Tabuleiro resetado para o estado inicial."
        )
        self.nodes_label.config(text="Nós Explorados: -")

        self.prev_button.config(state="disabled")
        self.next_button.config(state="disabled")
        self.solve_button.config(state="normal")
        self.reset_button.config(state="normal")
        self.radio_a_star.config(state="normal")
        self.radio_bfs.config(state="normal")

    def start_solve_thread(self):
        if not PuzzleState.is_solvable(INITIAL_BOARD):
            messagebox.showerror(
                "Erro", "O estado inicial definido não é solúvel para este objetivo."
            )
            return

        self.solve_button.config(state="disabled")
        self.reset_button.config(state="disabled")
        self.radio_a_star.config(state="disabled")
        self.radio_bfs.config(state="disabled")
        self.status_label.config(text=" Resolvendo... Por favor, aguarde.")
        self.root.update_idletasks()

        alg_choice = self.algorithm_var.get()
        if alg_choice == "a_star":
            algorithm_func = a_star_search
            alg_name = "A*"
        else:
            algorithm_func = bfs_search
            alg_name = "BFS"

        self.solve_thread = threading.Thread(
            target=self.solve_puzzle_in_thread, args=(algorithm_func, alg_name)
        )
        self.solve_thread.start()
        self.check_result_queue()

    def solve_puzzle_in_thread(self, algorithm_func, alg_name):
        """Executa a busca em thread separada e coloca o resultado na fila."""
        try:
            solution_path, elapsed_time, nodes_explored = algorithm_func(INITIAL_BOARD)
            self.result_queue.put(
                (solution_path, elapsed_time, nodes_explored, alg_name)
            )
        except Exception as e:
            self.result_queue.put((None, 0, 0, str(e)))

    def check_result_queue(self):
        try:
            result = self.result_queue.get(block=False)
            self.process_solution(result)
        except queue.Empty:
            self.root.after(100, self.check_result_queue)

    def process_solution(self, result):
        solution_path, elapsed_time, nodes_explored, alg_name_or_error = result

        if solution_path:
            self.solution_path = solution_path
            self.current_step = 0
            self.update_solution_view()
            self.nodes_label.config(text=f"Nós Explorados: {nodes_explored}")
            self.status_label.config(
                text=f" Solução ({alg_name_or_error}) encontrada em {elapsed_time:.4f}s. Nós: {nodes_explored}."
            )
            self.prev_button.config(state="disabled")
            self.next_button.config(state="normal")
            self.reset_button.config(state="normal")
        else:
            self.status_label.config(text=" Erro ou nenhuma solução encontrada.")
            messagebox.showerror(
                "Erro",
                f"Não foi possível encontrar uma solução. Erro: {alg_name_or_error}",
            )
            self.reset_puzzle()

    def next_step(self):
        if self.current_step < len(self.solution_path) - 1:
            self.current_step += 1
            self.update_solution_view()

    def prev_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.update_solution_view()

    def update_solution_view(self):
        if not self.solution_path:
            return

        current_state = self.solution_path[self.current_step]
        self.update_grid(current_state.board)

        total_steps = len(self.solution_path) - 1
        self.step_label.config(text=f"Passo: {self.current_step} / {total_steps}")

        if self.current_step == 0:
            self.prev_button.config(state="disabled")
        else:
            self.prev_button.config(state="normal")

        if self.current_step == total_steps:
            self.next_button.config(state="disabled")
        else:
            self.next_button.config(state="normal")


if __name__ == "__main__":
    root = tk.Tk()
    app = PuzzleApp(root)
    root.mainloop()
