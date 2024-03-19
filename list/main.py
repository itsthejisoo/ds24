from linkedListBasic import *
from circularLinkedList import *

if __name__ == "__main__":
    names = ["Amy", "Kevin", "Mary", "David"]

    name_list = LinkedList()
    name_list2 = CircularLinkedList()
    
    for name in names:
        name_list.append(name)
        name_list2.append(name)

    print("LinkedList")
    for name in name_list:
        print(name)
    
    name_list.pop(-1)
    name_list.insert(0, "Rose")
    name_list.sort()
    name_list.printList()
    
    print("\nCircularLinkedList")
    for name in name_list2:
        print(name)

    name_list2.pop(-1)
    name_list2.insert(0, "Rose")
    name_list2.sort()
    name_list2.printList()
