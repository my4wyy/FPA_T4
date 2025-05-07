# Resolvendo o Labirinto 2D com o Algoritmo A*

**Alunos:** Gabriel Faria, João Victor Salim, Lucas Garcia, Maísa Pires

## Descrição do Projeto

Este projeto implementa o algoritmo de busca A* para encontrar o caminho de menor custo entre um ponto inicial (S) e um ponto final (E) em um labirinto bidimensional (2D). O labirinto é representado por uma grade onde:

*   Células podem ter **custos de movimento variáveis** (representados por números inteiros >= 1).
*   Existem **obstáculos intransponíveis** (representados por `1` na entrada, tratados como custo infinito internamente).
*   Pontos específicos de início (`S`) e fim (`E`) são definidos.

O objetivo é que um agente navegue do ponto S ao ponto E da forma mais eficiente (menor custo total), evitando os obstáculos. Esta versão inclui funcionalidades extras:

1.  **Movimentos Diagonais:** O agente pode se mover nas 8 direções adjacentes (ortogonais e diagonais).
2.  **Custos Variáveis:** Diferentes células livres podem ter custos diferentes para atravessar (simulando terrenos variados).
3.  **Visualização Gráfica:** Uma interface gráfica simples usando Pygame permite visualizar o processo de busca do algoritmo A* em tempo real.

## Introdução ao Problema

Encontrar o caminho ótimo em ambientes complexos é fundamental em áreas como robótica, logística e jogos. O algoritmo A* é ideal para isso, pois equilibra o custo já percorrido (`g`) com uma estimativa heurística do custo restante (`h`).

A adição de movimentos diagonais e custos variáveis torna o problema mais realista. Movimentos diagonais oferecem rotas potencialmente mais curtas, enquanto custos variáveis simulam terrenos com diferentes dificuldades (areia, água, estrada), influenciando a escolha do caminho ótimo para além da simples distância geométrica.

## Instruções de Configuração e Execução

### Pré-requisitos

*   Python 3.x
*   Pygame: Biblioteca para a visualização gráfica.

### Instalação

1.  **Clone o repositório (ou baixe os arquivos):**
    ```bash
    git clone <https://github.com/my4wyy/FPA_T4.git>
    ```
2.  **Instale o Pygame:**
    ```bash
    pip install pygame
    # Ou, se encontrar problemas de permissão:
    pip install --user pygame
    ```

### Execução

Execute o script Python `main.py`:
```bash
python main.py
```
O script executará automaticamente os exemplos definidos no bloco `if __name__ == "__main__":`:

*   Imprimirá no console a entrada, o caminho encontrado (coordenadas e custo) e o labirinto com o caminho destacado para os exemplos sem visualização.
*   Para o exemplo de visualização, uma janela Pygame será aberta mostrando o algoritmo explorando o labirinto. As cores indicam:
    *   Azul: Início (S)
    *   Verde: Fim (E)
    *   Vermelho: Obstáculo
    *   Branco: Célula livre (custo 1)
    *   Laranja/Amarelo: Célula com custo > 1 (mais escura para custo maior)
    *   Ciano: Nós na Lista Aberta (Open List)
    *   Magenta: Nós na Lista Fechada (Closed List)
    *   Amarelo (no final): Caminho encontrado
*   **Feche a janela do Pygame** (clicando no botão de fechar ou pressionando ESC) para que o script continue e imprima o resultado final do exemplo visualizado no console.

### Modificando o Labirinto

Para testar com um labirinto diferente, modifique as listas de strings (como `maze_basic_str`, `maze_diag_str`, `maze_cost_str`) dentro do bloco `if __name__ == "__main__":` no arquivo `pathfinder_a_star_v2.py`. Siga o formato:

*   Cada linha do labirinto é uma string.
*   Os elementos em cada linha são separados por espaços.
*   Use `S` para o início.
*   Use `E` para o fim.
*   Use `1` para representar um obstáculo intransponível.
*   Use números inteiros `>= 0` para células livres, representando o **custo** para entrar naquela célula (custo 0 será tratado como 1).

Exemplo com custos variáveis:
```python
    maze_custom_str = [
        "S 2 1 5", # Célula (0,1) tem custo 2, (0,3) tem custo 5
        "1 1 1 1", # Obstáculo na (1,0), resto custo 1
        "0 0 3 E"  # Célula (2,2) tem custo 3
    ]
    # Chamar as funções read_maze, a_star_search, etc. com maze_custom_str
```

## Estrutura do Código

### Classes Principais
- **`Node`**: Representa um nó na busca com:
  - `position`: Coordenadas (x,y) no labirinto
  - `parent`: Nó predecessor no caminho
  - `g`: Custo acumulado desde o início
  - `h`: Valor heurístico estimado
  - `f`: Custo total (g + h)

### Funções Chave
- **`read_maze`**: Valida e converte a entrada em matriz de custos
- **`a_star_search`**: Implementação principal do algoritmo A*
- **`reconstruct_path`**: Reconstrói o caminho ótimo
- **`draw_grid`**: Renderiza a visualização gráfica
- **`print_maze_with_path`**: Exibe o labirinto com caminho no console

```
```



## Explicação do Algoritmo A* Implementado (v2)

### **Funcionamento do Algoritmo A**

O algoritmo A* mantém a lógica central de explorar nós com base no custo **f(n) = g(n) + h(n)**, onde:
- **g(n)**: Custo acumulado do caminho desde o nó inicial até o nó atual.
- **h(n)**: Estimativa heurística do custo do nó atual até o destino.
- **f(n)**: Custo total utilizado para priorizar a exploração dos nós.

#### **Principais Modificações e Recursos:**
1. **Movimentos:**
   - O algoritmo considera **8 movimentos possíveis** a partir de um nó:
     - **4 ortogonais** (cima, baixo, esquerda, direita) com custo de movimento = `1 * custo da célula`.
     - **4 diagonais** com custo de movimento = `√2 * custo da célula`.
   - Exemplo: Se o robô se move diagonalmente para uma célula com custo 2, o custo do movimento será `√2 * 2 ≈ 2.828`.

2. **Cálculo do Custo g(n):**
   - O custo acumulado para chegar a um vizinho `m` a partir do nó atual `n` é calculado como:
     ```
     tentative_g = g(n) + custo_movimento * custo_celula(m)
     ```
     - `custo_movimento`: `1` (movimento ortogonal) ou `√2` (movimento diagonal).
     - `custo_celula(m)`: Valor definido na grade para a célula `m` (exemplo: 2 para terreno difícil).

3. **Heurística h(n):**
   - **Movimentos ortogonais:** Usa a **Distância de Manhattan**:
     ```
     h(n) = |x_atual – x_final| + |y_atual – y_final|
     ```
   - **Movimentos diagonais:** Usa a **Distância de Chebyshev** (mais precisa para diagonais):
     ```
     h(n) = max(|x_atual – x_final|, |y_atual – y_final|)
     ```
   - **Por que Chebyshev?**  
     Essa heurística é **admissível** (nunca superestima o custo real) e **consistente**, garantindo que o A* encontre o caminho ótimo quando movimentos diagonais são permitidos.

4. **Leitura do Labirinto:**
   - A função `read_maze` interpreta:
     - `S` como ponto inicial (custo 1).
     - `E` como ponto final (custo 1).
     - `1` como obstáculo (custo `math.inf`).
     - Números `>= 0` como custos das células livres (exemplo: `2` para terreno difícil).

5. **Visualização (Pygame):**
   - Ativada com `visualize=True`, mostra em tempo real:
     - **Cores:**
       - Azul: Ponto inicial (`S`).
       - Verde: Ponto final (`E`).
       - Vermelho: Obstáculos.
       - Ciano: Nós na lista aberta (em exploração).
       - Magenta: Nós na lista fechada (já explorados).
       - Amarelo: Caminho final encontrado.
     - **Controle de velocidade:** Ajustado por `clock.tick(15)`.

6. **Exemplo Numérico:**
   - Suponha:
     - Nó atual: `(1, 1)` com `g(n) = 2`.
     - Destino: `(3, 3)`.
     - Célula `(2, 2)` tem custo `3`.
   - Cálculo para movimento diagonal:
     ```
     tentative_g = 2 + (√2 * 3) ≈ 2 + 4.242 = 6.242
     h(n) = max(|3-1|, |3-1|) = 2
     f(n) = 6.242 + 2 = 8.242
     ```

7. **Garantia de Otimalidade:**
   - O A* sempre encontra o caminho mais curto se:
     - A heurística for **admissível** (nunca superestima o custo real).
     - A heurística for **consistente** (satisfaz a desigualdade triangular).

---

**Estrutura de Dados:**

*   **Lista Aberta:** Mantida como uma min-heap (`heapq`) para acesso eficiente ao nó com menor `f`.
*   **Conjunto Aberto:** Um `set` (`open_set`) para verificar rapidamente se um nó está na lista aberta.
*   **Conjunto Fechado:** Um `set` (`closed_set`) para nós já explorados.
*   **`came_from`:** Dicionário para reconstruir o caminho.
*   **`g_score`:** Dicionário para armazenar o menor custo `g` conhecido para cada nó.

## Exemplos de Entrada e Saída (v2)

(Os exemplos são executados automaticamente ao rodar `main.py`)

### Exemplo 1: Básico (Ortogonal, Custo Uniforme)

(Similar ao original, mas interpretando 0 como custo 1)

**Entrada:**
```
S 0 1 0 0
0 0 1 0 1
1 0 1 0 0
1 0 0 E 1
```
**Saída (Console):**
```
Menor caminho (em coordenadas):
(0,0) -> (0,1) -> (1,1) -> (2,1) -> (3,1) -> (3,2) -> (3,3)

Labirinto com o caminho destacado:
S * █ . .
. * █ . █
█ * █ . .
█ * * E █
```
*(Nota: Obstáculos são mostrados como '█', células livres de custo 1 como '.')*

### Exemplo 2: Movimento Diagonal

**Entrada:**
```
S 0 0 0 0
0 1 1 1 0
0 1 0 0 0
0 1 1 1 1
0 0 0 0 E
```
**Saída (Console):**
```
Menor caminho (em coordenadas):
(0,0) -> (1,0) -> (2,0) -> (3,0) -> (4,1) -> (4,2) -> (4,3) -> (4,4)

Labirinto com o caminho destacado:
S . . . .
* █ █ █ .
* █ . . .
* █ █ █ █
. * * * E
```

### Exemplo 3: Custos Variáveis (Diagonais Permitidas)

**Entrada:**
```
S 2 1 5 8
2 1 1 1 5
3 1 9 9 1
4 1 1 1 1
5 4 3 2 E
```
**Saída (Console):**
```
Menor caminho (em coordenadas):
(0,0) -> (1,1) -> (2,1) -> (3,1) -> (3,2) -> (3,3) -> (4,4)

Labirinto com o caminho destacado:
S 2 . 5 8
2 * . . 5
3 * 9 9 .
4 * * * .
5 4 3 2 E
```
*(Nota: Custos > 1 são mostrados no labirinto final)*

---


## Guia de Uso Avançado

### Personalizando a Busca
```python
# Desativar diagonais e usar Manhattan
path = a_star_search(grid, start, end, 
                    allow_diagonal=False, 
                    heuristic_func=manhattan_distance)

# Ativar visualização gráfica
path = a_star_search(grid, start, end, 
                    visualize=True)
```


### Exemplo 4: Labirinto Sem Solução
**Entrada**:
```
S 1 0
1 1 0
0 1 E
```
**Saída Esperada**:
```
Nenhum caminho encontrado!
```



---

## Código Auxiliar (tests.py)

```python
import unittest
from main import read_maze, a_star_search, manhattan_distance

class TestPathFinder(unittest.TestCase):
    def test_read_maze_valid(self):
        maze = ["S 0 1", "0 0 E"]
        grid, start, end = read_maze(maze)
        self.assertEqual(start, (0, 0))
        self.assertEqual(end, (1, 2))
    
    def test_no_solution(self):
        maze = ["S 1", "1 E"]
        grid, start, end = read_maze(maze)
        path, _, _ = a_star_search(grid, start, end)
        self.assertIsNone(path)

    def test_heuristics(self):
        a = (0, 0)
        b = (3, 4)
        self.assertEqual(manhattan_distance(a, b), 7)

if __name__ == "__main__":
    unittest.main()
```

---

## Estrutura do projeto

```
/pathfinder/
│   README.md           # Documentação completa
│   main.py             # Código principal 
│   tests.py            # Testes unitários
```


