a = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
b = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

def pairs1(list1,list2):
    c=set(list1)
    c.intersection_update(set(list2))
    print(list(c))

pairs1(a,b)

def pairs_oldschool(list1,list2):
    d=[]
    for i in range(len(list1)):
        if list1[i] in list2:
            if list1[i] not in d:
                d.append(list1[i])
    print(d)

pairs_oldschool(a,b)