from colas import Cola

def test_Cola():
    # Given
    fifo = Cola()
    # When
    fifo.enqueue("1er elemento")
    fifo.enqueue("2do elemento")
    fifo.enqueue("3er elemento")

    # Then is a deque of three elemts
    assert len(fifo) == 3

    # When dequeue 1 element
    fifo.dequeue()

    # Then
    assert len(fifo) == 2

def test_cola_es_iterable():
    # Given
    fifo = Cola("primero", "segundo", "tercero")
    assert len(fifo) == 3

    # When
    for elemento in fifo:
        elemento

    # Then
    assert len(fifo) == 0
