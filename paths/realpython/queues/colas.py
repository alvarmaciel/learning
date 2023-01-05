from collections import deque

class Cola:
    def __init__(self, *elementos):
        self._elementos = deque(elementos)

    def __len__(self):
        return len(self._elementos)

    def __iter__(self):
        while len(self) > 0:
            yield self.dequeue()

    def enqueue(self, elemento):
        self._elementos.append(elemento)

    def dequeue(self):
        return self._elementos.popleft()
