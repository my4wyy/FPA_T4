import heapq
import math
import sys 

pygame_available = False
try:
    import pygame
    pygame_available = True
    CELL_SIZE = 30
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)      # Obstacle
    GREEN = (0, 255, 0)    # End
    BLUE = (0, 0, 255)     # Start
    YELLOW = (255, 255, 0) # Path
    CYAN = (0, 255, 255)   # Open List
    MAGENTA = (255, 0, 255) # Closed List
    GREY = (200, 200, 200) # Grid lines
    ORANGE = (255, 165, 0) # Variable cost cell (example)
except ImportError:
    print("Aviso: Pygame não encontrado ou não pôde ser importado. A visualização gráfica será desativada.", file=sys.stderr)
  
class Node:
    """Representa um nó no grafo de busca A*."""
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent
        self.g = 0  # Custo do início até o nó atual
        self.h = 0  # Custo heurístico estimado do nó atual até o fim
        self.f = 0  # Custo total (g + h)

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        if self.f == other.f:
            return self.h < other.h
        return self.f < other.f

    def __hash__(self):
        return hash(self.position)

def manhattan_distance(a, b):
    """Calcula a distância de Manhattan."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def diagonal_distance(a, b):
    """Calcula a distância diagonal (Chebyshev distance). Melhor heurística com movimentos diagonais."""
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))

def read_maze(maze_lines):
    """Lê a representação do labirinto e retorna a grade (com custos), início e fim."""
    grid = []
    start_pos = None
    end_pos = None
    rows = len(maze_lines)
    cols = 0
    for r, row_str in enumerate(maze_lines):
        row = []
        elements = row_str.split()
        if r == 0:
            cols = len(elements)
        elif len(elements) != cols:
            raise ValueError(f"Linha {r+1} tem número diferente de colunas.")

        for c, char in enumerate(elements):
            if char == 'S':
                start_pos = (r, c)
                row.append(1)  # Custo padrão 1 para início
            elif char == 'E':
                end_pos = (r, c)
                row.append(1)  # Custo padrão 1 para fim
            elif char == '1':
                row.append(math.inf)  # Obstáculo representado por custo infinito
            else:
                try:
                    cost = int(char)
                    if cost < 0:
                         raise ValueError(f"Custo negativo 	'{char}'	 inválido na linha {r+1}, coluna {c+1}")
                 
                    row.append(max(1, cost)) # Custo da célula (mínimo 1)
                except ValueError:
                    raise ValueError(f"Caractere inválido 	'{char}'	 encontrado no labirinto na linha {r+1}, coluna {c+1}")
        grid.append(row)

    if start_pos is None:
        raise ValueError("Ponto inicial 'S' não encontrado no labirinto.")
    if end_pos is None:
        raise ValueError("Ponto final 'E' não encontrado no labirinto.")

    return grid, start_pos, end_pos

def is_valid(position, grid):
    """Verifica se uma posição está dentro dos limites do grid e não é um obstáculo."""
    rows, cols = len(grid), len(grid[0])
    r, c = position
    return 0 <= r < rows and 0 <= c < cols and grid[r][c] != math.inf

# --- A* Search Algorithm ---
def a_star_search(grid, start, end, allow_diagonal=True, heuristic_func=diagonal_distance, visualize=False):
    """Executa o algoritmo A* para encontrar o menor caminho."""

    if visualize and not pygame_available:
        print("Aviso: Visualização solicitada, mas Pygame não está disponível. Executando sem visualização.", file=sys.stderr)
        visualize = False

    start_node = Node(start)
    end_node = Node(end)

    open_list = []
    heapq.heappush(open_list, start_node)
    open_set = {start_node.position} # Para verificação rápida O(1)
    open_set_history = [] # Para visualização

    closed_set = set()

    came_from = {} # Para reconstruir o caminho

    g_score = { (r,c): math.inf for r in range(len(grid)) for c in range(len(grid[0])) }
    g_score[start] = 0

    start_node.g = 0
    start_node.h = heuristic_func(start, end)
    start_node.f = start_node.g + start_node.h

    screen = None
    clock = None
    if visualize:
        pygame.init()
        rows, cols = len(grid), len(grid[0])
        screen_width = cols * CELL_SIZE
        screen_height = rows * CELL_SIZE
        screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("A* Pathfinding Visualization")
        clock = pygame.time.Clock()
        open_set_history.append(set(open_set)) # Estado inicial

    # --- Main A* Loop ---
    path_found = False
    current_node = None # Initialize current_node
    while open_list:
        if visualize:
            try:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return None, set(), set() # Indicate quit
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE: # Sair com ESC
                            pygame.quit()
                            return None, set(), set() # Indicate quit
            except pygame.error as e:
                 print(f"Erro no loop de eventos Pygame: {e}. Desativando visualização.", file=sys.stderr)
                 visualize = False # Disable visualization if event loop fails

        current_node = heapq.heappop(open_list)

        if current_node.position in closed_set:
            continue

        closed_set.add(current_node.position)
        if current_node.position in open_set:
             open_set.remove(current_node.position)

        if current_node.position == end_node.position:
            path_found = True
            break 
        neighbors_data = [] # Store (neighbor_pos, move_cost, cell_cost)
        r, c = current_node.position
        possible_moves = []
        # Ortogonais
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            neighbor_pos = (r + dr, c + dc)
            if is_valid(neighbor_pos, grid):
                move_cost = 1
                cell_cost = grid[neighbor_pos[0]][neighbor_pos[1]]
                neighbors_data.append((neighbor_pos, move_cost, cell_cost))
        # Diagonais
        if allow_diagonal:
            for dr, dc in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                neighbor_pos = (r + dr, c + dc)
                if is_valid(neighbor_pos, grid):
                    if grid[r + dr][c] == math.inf and grid[r][c + dc] == math.inf:
                        continue # Bloqueado, não adiciona vizinho

                    move_cost = math.sqrt(2)
                    cell_cost = grid[neighbor_pos[0]][neighbor_pos[1]]
                    neighbors_data.append((neighbor_pos, move_cost, cell_cost))

        for neighbor_pos, move_cost, cell_cost in neighbors_data:
            # Ignora vizinhos já na closed_set
            if neighbor_pos in closed_set:
                continue

            total_move_cost = move_cost * cell_cost
            tentative_g = g_score[current_node.position] + total_move_cost

            if tentative_g < g_score.get(neighbor_pos, math.inf):
                came_from[neighbor_pos] = current_node.position
                g_score[neighbor_pos] = tentative_g
                h_score = heuristic_func(neighbor_pos, end)
                f_score = tentative_g + h_score

                neighbor_node = Node(neighbor_pos, parent=current_node)
                neighbor_node.g = tentative_g
                neighbor_node.h = h_score
                neighbor_node.f = f_score

                heapq.heappush(open_list, neighbor_node)
                open_set.add(neighbor_pos)
  
        if visualize:
            try:
                open_set_history.append(set(p for p in open_set)) # Captura estado atual do open_set positions
                draw_grid(screen, grid, None, start, end, open_set_history, closed_set, current_node.position)
                pygame.display.flip()
                clock.tick(15) # Controla a velocidade da visualização
            except pygame.error as e:
                 print(f"Erro durante atualização Pygame: {e}. Desativando visualização.", file=sys.stderr)
                 visualize = False # Disable visualization if drawing fails
   
    if path_found and current_node is not None:
        path = reconstruct_path(came_from, current_node)
        if visualize:
            try:
                open_set_history.append(set(p for p in open_set))
                draw_grid(screen, grid, path, start, end, open_set_history, closed_set, current_node.position)
                pygame.display.flip()
                wait_for_quit() # Mantém a janela final aberta
                pygame.quit()
            except pygame.error as e:
                 print(f"Erro ao finalizar Pygame: {e}", file=sys.stderr)
                 # pygame.quit() might have already been called or failed
        return path, open_set_history, closed_set
    else:      
        if visualize:
            try:
                print("Sem solução encontrada. Feche a janela para sair.")
                draw_grid(screen, grid, None, start, end, open_set_history, closed_set, None)
                pygame.display.flip()
                wait_for_quit()
                pygame.quit()
            except pygame.error as e:
                 print(f"Erro ao finalizar Pygame (sem solução): {e}", file=sys.stderr)
        return None, open_set_history, closed_set # Sem solução

def reconstruct_path(came_from, current_node):
    """Reconstrói o caminho do final para o início usando o dicionário came_from."""
    path = []
    current_pos = current_node.position
    while current_pos in came_from:
        path.append(current_pos)
        if came_from[current_pos] is None:
             break # Should not happen with proper came_from logic, but safety check
        current_pos = came_from[current_pos]
    if not path or path[-1] != current_pos:
         path.append(current_pos)

    return path[::-1] # Retorna o caminho do início para o fim

def print_path(path):
    """Imprime o caminho como uma lista de coordenadas."""
    if path:
        print("Menor caminho (em coordenadas):")
        path_str = [f"({r},{c})" for r, c in path]
        print(" -> ".join(path_str))
    else:
        print("Sem solução")

def print_maze_with_path(grid, path, start, end):
    """Imprime o labirinto com o caminho destacado por '*'"""
    if not path:
        print("\nLabirinto (sem solução):")
    else:
        print("\nLabirinto com o caminho destacado:")

    path_set = set(path) if path else set()
    rows, cols = len(grid), len(grid[0])
    for r in range(rows):
        row_str = []
        for c in range(cols):
            pos = (r, c)
            if pos == start:
                row_str.append('S')
            elif pos == end:
                row_str.append('E')
            elif pos in path_set:
                row_str.append('*')
            elif grid[r][c] == math.inf:
                row_str.append('█') # Bloco para obstáculo
            else:
                # Mostra custo se for > 1, senão '.' para livre
                cost = grid[r][c]
                row_str.append(str(int(cost)) if cost > 1 else '.')
        print(" ".join(row_str))

def draw_grid(screen, grid, path, start, end, open_set_history, closed_set, current_pos=None):
    """Desenha o labirinto, caminho e status da busca no Pygame."""
    if not pygame_available or screen is None: return # Não faz nada se pygame não estiver carregado ou screen não inicializado

    try:
        screen.fill(WHITE)
        rows, cols = len(grid), len(grid[0])

        current_open_set_pos = open_set_history[-1] if open_set_history else set()

        for r in range(rows):
            for c in range(cols):
                color = WHITE
                pos = (r, c)
                cost = grid[r][c]

                if cost == math.inf: # Obstáculo
                    color = RED
                elif pos in closed_set:
                    color = MAGENTA
                elif pos in current_open_set_pos: # Check against positions
                    color = CYAN
                elif cost > 1: # Célula com custo variável
                     intensity = max(50, 255 - int(cost) * 15)
                     color = (255, intensity, 0)

                pygame.draw.rect(screen, color, (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE))

                if cost != math.inf and cost > 1:
                     try:
                         font = pygame.font.Font(None, 18)
                         text = font.render(str(int(cost)), True, BLACK)
                         screen.blit(text, (c * CELL_SIZE + 5, r * CELL_SIZE + 5))
                     except Exception as e:
                         print(f"Erro ao renderizar fonte: {e}", file=sys.stderr)

                pygame.draw.rect(screen, GREY, (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

        if path:
            for i in range(len(path) - 1):
                 start_point = (path[i][1] * CELL_SIZE + CELL_SIZE // 2, path[i][0] * CELL_SIZE + CELL_SIZE // 2)
                 end_point = (path[i+1][1] * CELL_SIZE + CELL_SIZE // 2, path[i+1][0] * CELL_SIZE + CELL_SIZE // 2)
                 pygame.draw.line(screen, YELLOW, start_point, end_point, 3)

        pygame.draw.rect(screen, BLUE, (start[1] * CELL_SIZE, start[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, GREEN, (end[1] * CELL_SIZE, end[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    except pygame.error as e:
        print(f"Erro durante desenho Pygame: {e}. Visualização pode estar incompleta.", file=sys.stderr)

def wait_for_quit():
    """Mantém a janela Pygame aberta até o usuário fechar."""
    if not pygame_available: return
    waiting = True
    while waiting:
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                if event.type == pygame.KEYDOWN:
                     if event.key == pygame.K_ESCAPE:
                          waiting = False
        except pygame.error as e:
            print(f"Pygame error during wait: {e}", file=sys.stderr)
            waiting = False

def main():
    print("Digite o labirinto (uma linha por vez, com espaços entre os elementos).")
    print("Use: S para início, E para fim, 0 para livre, 1 para obstáculo, 2 para terreno difícil, 3 para muito difícil.")
    print("Digite 'fim' para terminar:")
    
    maze_lines = []
    while True:
        line = input().strip()
        if line.lower() == 'fim':
            break
        maze_lines.append(line)
    
    try:
        grid, start_pos, end_pos = read_maze(maze_lines)
        path, open_set, closed_set = a_star_search(grid, start_pos, end_pos, visualize=True)
        
        if path:
            print("Caminho encontrado:")
            print_path(path)
            print_maze_with_path(grid, path, start_pos, end_pos)
        else:
            print("Nenhum caminho encontrado!")
            
    except ValueError as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    main()

    print("--- Exemplo 1: Básico (Movimentos Ortogonais) ---")
    maze_basic_str = [
        "S 0 1 0 0",
        "0 0 1 0 1",
        "1 0 1 0 0",
        "1 0 0 E 1"
    ]
    print("Labirinto de Entrada:")
    for row in maze_basic_str: print(row)
    try:
        grid_b, start_b, end_b = read_maze(maze_basic_str)
        print(f"S: {start_b}, E: {end_b}")
        path_b, _, _ = a_star_search(grid_b, start_b, end_b, allow_diagonal=False, heuristic_func=manhattan_distance, visualize=False)
        print_path(path_b)
        print_maze_with_path(grid_b, path_b, start_b, end_b)
    except ValueError as e: print(f"Erro: {e}")
    print("="*30)

    print("\n--- Exemplo 2: Movimento Diagonal Permitido ---")
    maze_diag_str = [
        "S 0 0 0 0",
        "0 1 1 1 0",
        "0 1 0 0 0",
        "0 1 1 1 1",
        "0 0 0 0 E"
    ]
    print("Labirinto de Entrada:")
    for row in maze_diag_str: print(row)
    try:
        grid_d, start_d, end_d = read_maze(maze_diag_str)
        print(f"S: {start_d}, E: {end_d}")
        path_d, _, _ = a_star_search(grid_d, start_d, end_d, allow_diagonal=True, heuristic_func=diagonal_distance, visualize=False)
        print_path(path_d)
        print_maze_with_path(grid_d, path_d, start_d, end_d)
    except ValueError as e: print(f"Erro: {e}")
    print("="*30)

    print("\n--- Exemplo 3: Custos Variáveis (Diagonais Permitidas) ---")
    maze_cost_str = [
        "S 2 1 5 8",
        "2 1 1 1 5",
        "3 1 9 9 1",
        "4 1 1 1 1",
        "5 4 3 2 E"
    ]
    print("Labirinto de Entrada:")
    for row in maze_cost_str: print(row)
    try:
        grid_c, start_c, end_c = read_maze(maze_cost_str)
        print(f"S: {start_c}, E: {end_c}")
        path_c, _, _ = a_star_search(grid_c, start_c, end_c, allow_diagonal=True, heuristic_func=diagonal_distance, visualize=False)
        print_path(path_c)
        print_maze_with_path(grid_c, path_c, start_c, end_c)
    except ValueError as e: print(f"Erro: {e}")
    print("="*30)
 
    print("\n--- Exemplo 4: Visualização Gráfica (Tentativa) ---")
    print("Tentando executar busca com visualização Pygame...")
    if pygame_available:
        print("(Feche a janela do Pygame ou pressione ESC para continuar)")

    try:
        grid_v, start_v, end_v = read_maze(maze_cost_str)
        print(f"S: {start_v}, E: {end_v}")
        path_v, open_hist_v, closed_set_v = a_star_search(grid_v, start_v, end_v, allow_diagonal=True, heuristic_func=diagonal_distance, visualize=True)

        if path_v is not None:
             print("\nResultado da busca (Exemplo 4):")
             print_path(path_v)
             print_maze_with_path(grid_v, path_v, start_v, end_v)
        else:
             print("\nBusca (Exemplo 4) interrompida pelo usuário ou sem solução.")

    except ValueError as e:
        print(f"Erro no Exemplo 4: {e}")
    except Exception as e:
        print(f"Erro inesperado durante Exemplo 4: {e}")
        if not pygame_available:
             print("Isso pode estar relacionado à ausência do Pygame.")

    print("\nFim dos exemplos.")


