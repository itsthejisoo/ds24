def insertionSort(A):
    for i in range(len(A)):
        loc = i - 1
        newItem = A[i]
        while A[loc] > newItem and loc >= 0:
            A[loc + 1] = A[loc]
            loc -= 1
        A[loc + 1] = newItem