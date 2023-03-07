import heapq

h = [(1, 'a'), (2, 'c'), (2, 'c'), (3, 'd'), (4, 'e')]
heapq.heapify(h)


while h:
    print(heapq.heappop(h))