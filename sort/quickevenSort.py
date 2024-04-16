def quickEvenSort(A:list, p:int, r:int):
    if p < r:
        q1, q2 = partition(A, p, r)
        quickEvenSort(A, p, q1-1)
        quickEvenSort(A, q2+1, r)

def partition(A:list, p:int, r:int) -> tuple:
    x = A[r]
    i = p - 1
    j = p - 1
    start = p
    end = r

    while start <= end:
        if A[start] < x:
            i += 1
            j += 1
            A[i], A[start] = A[start], A[i]
        if A[start] == x:
            j += 1
            A[j], A[start] = A[start], A[j]
        start += 1
        
    return i, j