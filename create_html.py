class Node:
    def __init__(self, item , x_position, y_position):
        self.item = item
        self.x = x_position
        self.y = y_position
        self.left = None
        self.right = None
        
class BinaryTree():
    #트리 생성
    def __init__(self):
        self.root = None
        self.result = ""
        self.result_temp = ""
        self.right_end = 0
        
    def root_finder(self):
        return self.root
        
    #후위 순회
    def postorder(self, node):
        if node != None:
            #오른쪽 서브트리 순회
            if node.right:
                self.postorder(node.right)
                self.right_end = 1
                
            #왼쪽 서브트리 순회
            if node.left:
                self.postorder(node.left)
                self.right_end = 0
            
            #노드 방문
            if node == self.root_finder():
                self.result_temp = self.result + self.result_temp
                
            if not self.right_end:
                self.result = "<div>" + node.item + self.result + "</div>"
            else:
                self.result_temp = self.result + self.result_temp
                self.result = ""
                self.result = "<div>" + node.item +"</div>"
                    
        return self.result_temp             
                
    def height(self, root):
        if root == None:
            return 0
        return max(self.height(root.left), self.height(root.right)) +1
    
tree = BinaryTree()
node1 = Node("10", 0, 0)
node2 = Node("20", 0, 0)
node3 = Node("30", 0 , 30)
node4 = Node("40", 50, 0)
node5 = Node("50", 0 , 0)
node6 = Node("60", 55, 10)
node7 = Node("70", 55, 20) 

tree.root = node1
node1.left = node2
node2.left = node3
node2.right = node4
node4.left = node5
node4.right = node6
node6.left = node7

result_code = tree.postorder(tree.root_finder())
result_code = "<html>" + result_code + "</html>"
print(result_code)