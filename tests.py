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
