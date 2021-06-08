class Node:
    def __init__(self, x_position1, y_position1, x_position2, y_position2, p_tag):
        self.xdis = x_position2 - x_position1
        self.ydis = y_position2 - y_position1
        self.x1 = x_position1
        self.y1 = y_position1
        self.x2 = x_position2
        self.y2 = y_position2
        self.isp = p_tag
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
        
    def insert(self, node):
        self.root = self._insert_value(self.root, node)
        return self.root is not None
           
    def _insert_value(self, sub_root, node):
        if sub_root is None:
            sub_root = node
        else:
            if sub_root.x1 < node.x1 and sub_root.x2  > node.x2 and sub_root.y1 < node.y1 and sub_root.y2 > node.y2:
                sub_root.left = self._insert_value(sub_root.left, node)            
            elif sub_root.x1 > node.x1 and sub_root.x2  < node.x2 and sub_root.y1 > node.y1 and sub_root.y2 < node.y2:
                node.left = self._insert_value(sub_root.left, sub_root)
                #node.right = self._insert_value(sub_root.right, sub_root)
                sub_root = node
            elif sub_root.x1 > node.x1 or sub_root.y1 > node.y1 :
                #node.left = self._insert_value(sub_root.left, sub_root)
                node.right = self._insert_value(sub_root.right, sub_root)
                sub_root = node
            else:
                sub_root.right = self._insert_value(sub_root.right, node)
            
        return sub_root
    
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
                if node.isp:
                    self.result = "<p style = \" width: " + str(node.xdis) +"px; height:" + str(node.ydis)+"px;\">" +node.isp + self.result + "</p>"
                else:
                    self.result = "<div style = \" border : 1px solid black; width: " + str(node.xdis) +"px; height:" + str(node.ydis)+"px;\">"  + self.result + "</div>"
            else:
                if node.isp:
                    self.result_temp = self.result + self.result_temp
                    self.result = ""
                    self.result = "<p style = \" width: " + str(node.xdis) +"px; height:" +str(node.ydis)+"px;\">" + node.isp + "</p>"
                else:   
                    self.result_temp = self.result + self.result_temp
                    self.result = ""
                    self.result = "<div style = \" border : 1px solid black; width: " + str(node.xdis) +"px; height:" +str(node.ydis)+"px;\">" + "</div>"
                    
        return self.result_temp             
                
    def height(self, root):
        if root == None:
            return 0
        return max(self.height(root.left), self.height(root.right)) +1


x_size = 907
y_size = 968   
    
tree = BinaryTree()
node1 = Node(0, 0, x_size, y_size, 0)
node2 = Node(100, 100, 800, 250, 0)
node3 = Node(600, 150, 700, 200, 0)
node4 = Node(100, 400, 800, 550, 0)
node5 = Node(600, 450, 700, 500, 0)
node6 = Node(100, 700, 800, 850, 0)
node7 = Node(600, 750, 700, 800, 0)
node8 = Node(100, 100, 800, 250, "asdf")

tree.insert(node1)
tree.insert(node2)
tree.insert(node3)
tree.insert(node4)
tree.insert(node5)
tree.insert(node6)
tree.insert(node7)
tree.insert(node8)


result_code = tree.postorder(tree.root_finder())
result_code = "<html>" + result_code + "</html>"
print(result_code)