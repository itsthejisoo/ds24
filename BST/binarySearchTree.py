class TreeNode:
    def __init__(self, newItem, left, right):
        self.item = newItem
        self.left = left
        self.right = right

class BinarySearchTree:
    def __init__(self):
        self.__root = None

    def search(self, x) -> TreeNode:
        return self.__searchItem(self.__root, x)

    def __searchItem(self, tNode:TreeNode, x) -> TreeNode:
        if tNode == None:
            return None
        elif x == tNode.item:
            return tNode
        elif x < tNode.item:
            return self.__searchItem(tNode.left, x)
        else:
            return self.__searchItem(tNode.right, x)

    def insert(self, newItem):
        self.__root = self.__insertItem(self.__root, newItem)

    def __insertItem(self, tNode:TreeNode, newItem) ->TreeNode:
        if tNode == None:
            tNode = TreeNode(newItem, None, None)
        elif newItem < tNode.item:
            tNode.left = self.__insertItem(tNode.left, newItem)
        else:
            tNode.right = self.__insertItem(tNode.right, newItem)
        return tNode

    def delete(self, x):
        self.__root = self.__deleteItem(self.__root, x)

    def __deleteItem(self, tNode:TreeNode, x) -> TreeNode:
        if tNode == None:
            return None
        elif x == tNode.item:
            tNode = self.__deleteNode(tNode)
        elif x < tNode.item:
            tNode.left = self.__deleteItem(tNode.left, x)
        else:
            tNode.right = self.__deleteItem(tNode.right, x)
        return tNode

    def __deleteNode(self, tNode:TreeNode) -> TreeNode:
        if tNode.left == None and tNode.right == None:
            return None
        elif tNode.left == None:
            return tNode.right
        elif tNode.right == None:
            return tNode.left
        else:
            (rtnItem, rtnNode) = self.__deleteMinItem(tNode.right)
            tNode.item = rtnItem
            tNode.right = rtnNode
            return tNode
        
    def __deleteMinItem(self, tNode:TreeNode) -> tuple:
        if tNode.left == None:
            return (tNode.item, tNode.right)
        else:
            (rtnItem, rtnNode) = self.__deleteMinItem(tNode.left)
            tNode.left = rtnNode
            return (rtnItem, tNode)

    def isEmpty(self) -> bool:
        return self.__root == self.NIL

    def clear(self):
        self.__root = self.NIL

    def getRoot(self):
        return self.__root

    def lca(self, a, b):
        lca_item = self.__lca(self.__root, a, b)
        print(lca_item.item)

    def __lca(self, tNode:TreeNode, a, b):
        if tNode == None or tNode.item == a or tNode.item == b:
            return tNode
        
        left = self.__lca(tNode.left, a, b)
        right = self.__lca(tNode.right, a, b)

        if left and right: # left와 right 모두 노드 값이 있을 경우
            return tNode
        
        # left와 right 중에서 left만 노드를 찾은 경우 (left가 더 상위 노드라는 뜻), 반대로도 같은 상황
        return left if left is not None else right 

# 전위 순회 (루트 노드에서 가장 아래의 왼쪽 노드까지 다 탐색한 후에 오른쪽 노드 탐색)
    def preorder(self, r:TreeNode):
        if r != None:
            print(r.item, end=" ")
            self.preorder(r.left)
            self.preorder(r.right)

# 중위 순회 (맨 밑에 자식 노드 -> 그의 부모 노드 -> 오른쪽 자식 노드 탐색하여 올라감. 후에 오른쪽 노드 탐색)
    def inorder(self, r:TreeNode):
        if r != None:
            self.inorder(r.left)
            print(r.item, end=" ")
            self.inorder(r.right)

# 후위 순회 (맨 밑에 자식 노드부터 탐색하여 올라감)
    def postorder(self, r:TreeNode):
        if r != None:
            self.postorder(r.left)
            self.postorder(r.right)
            print(r.item, end=" ")
