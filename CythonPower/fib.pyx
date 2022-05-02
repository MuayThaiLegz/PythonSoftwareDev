# Cython
cdef Cyfib(int n):
    cdef int int
    cdef double a=0.0, b=1.0
    for i in range(n):
        a, b = a + b, a
    return a