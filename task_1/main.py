import random
import time
from functools import lru_cache

# Генерація масиву розміром 100 000 елементів
N = 100_000
array = [random.randint(1, 1000) for _ in range(N)]

# Генерація 50 000 випадкових запитів
Q = 50_000
queries = []
for _ in range(Q):
    if random.random() < 0.7:  # 70% - Range запити, 30% - Update запити
        L = random.randint(0, N - 1)
        R = random.randint(L, N - 1)
        queries.append(('Range', L, R))
    else:
        index = random.randint(0, N - 1)
        value = random.randint(1, 1000)
        queries.append(('Update', index, value))


# --- ФУНКЦІЇ БЕЗ КЕШУ ---
def range_sum_no_cache(array, L, R):
    """Обчислення суми елементів без кешування."""
    return sum(array[L:R + 1])


def update_no_cache(array, index, value):
    """Оновлення значення без кешування."""
    array[index] = value


# --- ФУНКЦІЇ З LRU-КЕШЕМ ---
cache_size = 1000


@lru_cache(maxsize=cache_size)
def range_sum_with_cache(L, R):
    """Обчислення суми елементів із використанням LRU-кешу."""
    return sum(array[L:R + 1])


def update_with_cache(index, value):
    """Оновлення значення та очищення кешу, якщо масив змінено."""
    array[index] = value
    range_sum_with_cache.cache_clear()  # Очищення кешу після оновлення


# --- ТЕСТУВАННЯ ПРОДУКТИВНОСТІ ---
print("Виконання тестів...")

# --- Тестування без кешу ---
start_no_cache = time.time()
for query in queries:
    if query[0] == 'Range':
        range_sum_no_cache(array, query[1], query[2])
    else:
        update_no_cache(array, query[1], query[2])
end_no_cache = time.time()
print(f"Час виконання без кешування: {end_no_cache - start_no_cache:.2f} секунд")

# --- Тестування з кешем ---
start_with_cache = time.time()
for query in queries:
    if query[0] == 'Range':
        range_sum_with_cache(query[1], query[2])
    else:
        update_with_cache(query[1], query[2])
end_with_cache = time.time()
print(f"Час виконання з LRU-кешем: {end_with_cache - start_with_cache:.2f} секунд")
