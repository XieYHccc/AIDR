import queue

# create a queue
q = queue.Queue()

# add all elements of an array to the queue at once
arr = [1, 2, 3]
q.put(1, 2, 3)

# get the first item from the queue
while not q.empty():
    print(q.get())