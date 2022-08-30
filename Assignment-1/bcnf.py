# Counts the number of steps required to decompose a relation into BCNF.

from fileinput import close
from relation import *
from functional_dependency import *

# You should implement the static function declared
# in the ImplementMe class and submit this (and only this!) file.
# You are welcome to add supporting classes and methods in this file.
class ImplementMe:
    # Returns the number of recursive steps required for BCNF decomposition
    #
    # The input is a set of relations and a set of functional dependencies.
    # The relations have *already* been decomposed.
    # This function determines how many recursive steps were required for that
    # decomposition or -1 if the relations are not a correct decomposition.
    @staticmethod
    def DecompositionSteps( relations, fds ):
        flag = 0
        r = relations.relations
        all_r = get_all_r(r)  
        for i in fds.functional_dependencies:
            closure = get_closure(i,fds)
            if(closure != all_r):
                if len(r) == 1:
                    return -1
                break
            else:
                for j in r:
                    if j.attributes != closure:             
                        flag = -1
        if len(r) != 1:
            flag = decompose(all_r,r,fds)   
        return flag
def decompose(r,relations,fds):
    """
    decomposing for the first time
    """
    for i in fds.functional_dependencies:
        closure = get_closure(i,fds)
        r1 = closure
        r2 = r-closure
        r2 = set.union(r2,i.left_hand_side)
        if check_relations_2(r1,r2,relations):
            if(is_vio(r1,fds) or is_vio(r2,fds)):
                flag = -1
            else:
                return 1
        elif(len(relations) == 2):
            flag = -1
        else:
            if (is_vio(r1,fds) and is_vio(r2,fds)) or (not is_vio(r1,fds) and not is_vio(r2,fds)):
                flag = -1
            else:
                vio_r = r1
                good_r = r2
                if is_vio(r2,fds):
                    vio_r = r2
                    good_r = r1
                flag = second_decompose(good_r, vio_r, relations, fds)
                if flag == 2:
                    return 2
    return flag

def second_decompose(r1,r2,relations,fds):
    """
    second decomposing for returning 2 or -1
    """
    set_k = find_possible_fd(r2, fds)
    for k in set_k:
        r21 = get_closure(k, fds)
        r22 = r2 - r21
        r22 = set.union(r22,k.left_hand_side)
        if check_relations_3(r1,r21,r22,relations):
            if(is_vio(r1,fds) or is_vio(r21,fds) or is_vio(r22,fds)):
                return -1
            return 2
    return -1
def is_vio(r1,fds):
    """
    Function checks if there are any violations in a specific relation set and all the functional dependencies
    """
    for i in fds.functional_dependencies:
        for right_elem in i.right_hand_side:
            if i.left_hand_side.issubset(r1) and right_elem in r1:
                closure = get_closure(i,fds) 
                if not r1.issubset(closure):
                    return True
    return False
def find_possible_fd(r2,fds):
    """
    checking which fd's are appicable to r2
    """
    set_k = set()
    for elem in fds.functional_dependencies:
        if elem.left_hand_side.issubset(r2) and elem.right_hand_side.issubset(r2):
            set_k.add(elem)
    return set_k
def check_relations_2(r1,r2,relations):
    cntr = 0
    for elem in relations:
        if r1 == elem.attributes or r2 == elem.attributes:
            cntr += 1
    return cntr == len(relations)
def check_relations_3(r1,r21,r22,relations):
    cntr = 0
    for elem in relations:
        if r1 == elem.attributes or r21 == elem.attributes or r22 == elem.attributes:
            cntr += 1
    return cntr == len(relations)
        
def get_closure(i,fds):
    """
    getting the closure of each functional dependencies
    """
    set1 = set.union(i.left_hand_side,i.right_hand_side)
    set2 = set()
    while (set1!=set2):
        set2=set.union(set1,set2)
        for j in fds.functional_dependencies:
            if check_all_left(j.left_hand_side, set1):
                set1 = set.union(set1,j.right_hand_side)
    return set1
def check_all_left(jlhs, set1):
    cntr = 0
    for elem in jlhs:
        if elem in set1:
            cntr += 1
    return cntr==len(jlhs) 
def get_all_r(r):
    """
    getting the relation do check if superkey or not (for returning 0)
    """
    all_r = set()
    for i in r:
        all_r = set.union(all_r,i.attributes)
    return all_r

