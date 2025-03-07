import timeit
import matplotlib.pyplot as plt
from functools import lru_cache

# ---- Splay Tree Implementation ----
class SplayNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None

class SplayTree:
    def __init__(self):
        self.root = None

    def _splay(self, root, key):
        if not root or root.key == key:
            return root

        if key < root.key:
            if not root.left:
                return root

            if key < root.left.key:
                root.left.left = self._splay(root.left.left, key)
                root = self._rotate_right(root)

            elif key > root.left.key:
                root.left.right = self._splay(root.left.right, key)
                if root.left.right:
                    root.left = self._rotate_left(root.left)

            return self._rotate_right(root) if root.left else root

        else:
            if not root.right:
                return root

            if key > root.right.key:
                root.right.right = self._splay(root.right.right, key)
                root = self._rotate_left(root)

            elif key < root.right.key:
                root.right.left = self._splay(root.right.left, key)
                if root.right.left:
                    root.right = self._rotate_right(root.right)

            return self._rotate_left(root) if root.right else root

    def _rotate_right(self, node):
        left = node.left
        node.left = left.right
        left.right = node
        return left

    def _rotate_left(self, node):
        right = node.right
        node.right = right.left
        right.left = node
        return right

    def insert(self, key, value):
        if not self.root:
            self.root = SplayNode(key, value)
            return

        self.root = self._splay(self.root, key)

        if self.root.key == key:
            return

        new_node = SplayNode(key, value)
        if key < self.root.key:
            new_node.right = self.root
            new_node.left = self.root.left
            self.root.left = None
        else:
            new_node.left = self.root
            new_node.right = self.root.right
            self.root.right = None

        self.root = new_node

    def search(self, key):
        if not self.root:
            return None

        self.root = self._splay(self.root, key)

        return self.root.value if self.root.key == key else None


# ---- Fibonacci with LRU Cache ----
@lru_cache(maxsize=None)
def fibonacci_lru(n):
    if n <= 1:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)


# ---- Fibonacci with Splay Tree ----
def fibonacci_splay(n, tree):
    if n <= 1:
        return n

    cached_value = tree.search(n)
    if cached_value is not None:
        return cached_value

    result = fibonacci_splay(n - 1, tree) + fibonacci_splay(n - 2, tree)
    tree.insert(n, result)
    return result


# ---- Performance Testing ----
n_values = list(range(0, 951, 50))  # 0, 50, 100, ..., 950
lru_times = []
splay_times = []

for n in n_values:
    tree = SplayTree()

    # Measure time for LRU Cache
    lru_time = timeit.timeit(lambda: fibonacci_lru(n), number=1)
    lru_times.append(lru_time)

    # Measure time for Splay Tree
    splay_time = timeit.timeit(lambda: fibonacci_splay(n, tree), number=1)
    splay_times.append(splay_time)

# ---- Print Table ----
print(f"{'n':<10}{'LRU Cache Time (s)':<25}{'Splay Tree Time (s)'}")
print("-" * 50)
for i in range(len(n_values)):
    print(f"{n_values[i]:<10}{lru_times[i]:<25.8f}{splay_times[i]:.8f}")

# ---- Plot Results ----
plt.figure(figsize=(10, 5))
plt.plot(n_values, lru_times, label="LRU Cache", marker="o")
plt.plot(n_values, splay_times, label="Splay Tree", marker="s")
plt.xlabel("n (номер числа Фібоначчі)")
plt.ylabel("Час виконання (секунди)")
plt.title("Порівняння продуктивності обчислення чисел Фібоначчі")
plt.legend()
plt.grid(True)
plt.show()
