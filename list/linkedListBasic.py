from listNode import ListNode

class LinkedList():
    def __init__(self):
        self.__head = ListNode('dummy', None)
        self.tail = None
        self.__numItems = 0

    def getNode(self, i:int) -> ListNode:
        curr = self.__head
        for index in range(i+1):
            curr = curr.next
        return curr

    def __findnode(self, x):
        prev = self.__head
        curr = prev.next
        while curr != None:
            if curr.item == x:
                return (prev, curr)
            else:
                prev = curr
                curr = curr.next
        return (None, None)

    def insert(self, i:int, newItem):
        if i >=0 and i <= self.__numItems:
            prev = self.getNode(i-1)
            newNode = ListNode(newItem, prev.next)
            prev.next = newNode
            self.__numItems += 1
            self.tail = self.getNode(self.__numItems-1)
        else:
            print("index", i, ": out of bound")
    
    def append(self, newItem):
        prev = self.getNode(self.__numItems - 1)
        newNode = ListNode(newItem, prev.next)
        prev.next = newNode
        self.__numItems += 1
        self.tail = newNode
    
    # i번 원소 삭제
    def pop(self, *args):
        if len(args) != 0:
            i = args[0]

        if len(args) == 0 or i == -1:
            i = self.__numItems -1

        if i >= 0 and i <= self.__numItems-1:
            prev = self.getNode(i-1)
            curr = prev.next # 삭제하고자하는 노드
            prev.next = curr.next # 삭제하고자 하는 노드 전과 후를 이어줌
            retItem = curr.item
            self.__numItems -= 1
            self.tail = self.getNode(self.__numItems-1)
            return retItem
        else:
            return None

    # x인 원소 삭제
    def remove(self, x):
        (prev, curr) = self.__findnode(x)
        if curr != None:
            prev.next = curr.next
            self.__numItems -= 1
            self.tail = self.getNode(self.__numItems-1)
            return x
        else:
            return None

    # i번 원소 알려주기
    def get(self, * args):
        if self.__numItems == 0:
            return "No Items"

        if len(args) != 0:
            i = args[0]

        if len(args) == 0 or i == -1:
            i = self.__numItems - 1

        if (i >= 0 and i <= self.__numItems - 1):
            return self.getNode(i).item
        else:
            return "Out of bound"
    
    def index(self, x) -> int:
        curr = self.__head.next
        for index in range(self.__numItems):
            if curr == x:
                return index
            else:
                curr = curr.next
        return -2 # 더미 헤드가 인덱스 -1 이므로 안쓰는 -2 인덱스를 return

    def size(self):
        return self.__numItems
    
    def clear(self):
        self.__head = ListNode("dummy", None)
        self.__numItems = 0
        self.tail = None

    def count(self, x):
        cnt = 0
        for element in self:
            if element == x:
                cnt += 1
        return cnt
    
    def extend(self, a):
        self.tail.next = a.__head.next
        self.__numItems += a.size()

    def reverse(self):
        prev = None
        curr = self.__head.next
        while curr != None:
            next = curr.next
            curr.next = prev
            prev = curr
            curr = next
        self.__head.next = prev
        self.tail = self.getNode(self.__numItems-1)
    
    def sort(self) -> None:
        a = []
        for index in range(self.__numItems):
            a.append(self.get(index))
        a.sort()
        self.clear()
        for index in range(len(a)):
            self.append(a[index])
        self.tail = self.getNode(self.__numItems)

    def printList(self):
        for item in self:
            print(item, end=' ')
        print()

    def __iter__(self):
        return LinkedListIterator(self)

class LinkedListIterator:
    def __init__(self, alist):
        self.__head = alist.getNode(-1)
        self.iterPosition = self.__head.next

    def __next__(self):
        if self.iterPosition == self.__head:
            raise StopIteration
        else:
            if self.iterPosition is None:
                raise StopIteration
            item = self.iterPosition.item
            self.iterPosition = self.iterPosition.next
            return item