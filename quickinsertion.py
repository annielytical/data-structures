"""This is a Quicksort / Insertion Sort hybrid

Call it by passing a list and partition limit to quick_insertion

Quicksort does the initial sorting; the partition limit specifies the
length at which insertion sort takes over on the segmented lists

Functions:
    quick_insertion: calls quicksort
    quicksort: recursively calls itself for lists segmented at the splitpoint
    partition: finds the pivot value, compares left/right marks, swaps values
    insertionsort: sorts the list, one value at a time
"""


def quick_insertion(alist, limit):
    """calls quicksort"""
    quicksort(alist, 0, len(alist) - 1, limit)
    return alist


def quicksort(alist, first, last, limit):
    """recursively calls itself for lists segmented at the splitpoint"""
    on = True

    if on:
        splitpoint = partition(alist, first, last, limit)

    if first + limit < last:
        quicksort(alist, first, splitpoint - 1, limit)
        quicksort(alist, splitpoint + 1, last, limit)

        if first + limit == last:
            on = False
    else:
        insertion_sort(alist, first, splitpoint)
        insertion_sort(alist, splitpoint, last)


def partition(alist, first, last, limit):
    """uses a median of three method to determine the pivot value; finds/compares
    rightmark and leftmark values, swapping values when needed
    """
    mid = (first + last) // 2

    if alist[first] <= alist[mid] and alist[first] >= alist[last]:
        pivotvalue = alist[first]
    elif alist[first] >= alist[mid] and alist[first] <= alist[last]:
        pivotvalue = alist[first]
    elif alist[mid] >= alist[first] and alist[mid] <= alist[last]:
        pivotvalue = alist[mid]
        alist[mid] = alist[first]
        alist[first] = pivotvalue
    elif alist[mid] <= alist[first] and alist[mid] >= alist[last]:
        pivotvalue = alist[mid]
        alist[mid] = alist[first]
        alist[first] = pivotvalue
    else:
        pivotvalue = alist[last]
        alist[last] = alist[first]
        alist[first] = pivotvalue

    leftmark = first + 1
    rightmark = last
    done = False

    while not done:

        while leftmark <= rightmark and alist[leftmark] <= pivotvalue:
            leftmark = leftmark + 1

        while alist[rightmark] >= pivotvalue and rightmark >= leftmark:
            rightmark = rightmark - 1

        if rightmark < leftmark:
            done = True
        else:
            temp = alist[leftmark]
            alist[leftmark] = alist[rightmark]
            alist[rightmark] = temp

    temp = alist[first]
    alist[first] = alist[rightmark]
    alist[rightmark] = temp
    return rightmark


def insertion_sort(alist, first, last):
    """sorts the list one value at a time"""
    for index in range(first, last + 1):
        currentvalue = alist[index]
        position = index

        while position > 0 and alist[position - 1] > currentvalue:
            alist[position] = alist[position - 1]
            position = position - 1

        alist[position] = currentvalue
