import random

def quickrandom(A, p, r):
    if p < r:
        q = partition(A, p, r)
        quickrandom(A, p, q-1)
        quickrandom(A, q+1, r)
    
def partition(A, p, r):
    pivot = random.randrange(p, r)
    x = A[pivot]
    i = p - 1
    for j in range(p, r):
        if A[j] < x:
            i += 1
            A[i], A[j] = A[j], A[i]
    A[i+1], A[pivot] = A[pivot], A[i+1] 

    return i + 1