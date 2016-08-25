from itertools import zip_longest

list1default=[1,2,3,4,5,6]
list2default=["one","two","three","four","five"]

try:
    print("Leave empty for default")
    list1=input().split()
    if not list1:
        raise ValueError()
except ValueError:
    list1=list1default

try:
    list2=input().split()
    if not list2:
        raise ValueError()
except ValueError:
    list2=list2default

def dictionary(keys,values):
    diction=dict(zip_longest(keys, values[:len(keys)]))
    print(diction)

def dict_cyc(keys,values):
    diction={}
    for i in range(len(keys)):
        try:
            diction[keys[i]]=values[i]
        except:
            diction[keys[i]]=None
    print(diction)

dictionary(list1,list2)
dict_cyc(list1,list2)