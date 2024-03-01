
outputdebug = True 

def debug(msg):
    if outputdebug:
        print (msg)

class Node():
    def __init__(self, key):
        self.key = key
        self.left = None 
        self.right = None 




class AVLTree():
    def __init__(self, *args):
        self.node = None 
        self.root = None
        self.height = -1  
        self.balance = 0; 
        
        if len(args) == 1: 
            for i in args[0]: 
                self.insert(i)
                
    def height(self):
        if self.node: 
            return self.node.height 
        else: 
            return 0 
    
    def is_leaf(self):
        return (self.height == 0) 
    
    def insert(self, key):
        tree = self.node
        
        newnode = Node(key)
        
        if tree == None:
            self.node = newnode 
            self.node.left = AVLTree() 
            self.node.right = AVLTree()
        
        elif key < tree.key: 
            self.node.left.insert(key)
            
        elif key > tree.key: 
            self.node.right.insert(key)

            
        self.rebalance() 
        
    def rebalance(self):
        # key inserted. Let's check if we're balanced
        self.update_heights(False)
        self.update_balances(False)
        while self.balance < -1 or self.balance > 1: 
            if self.balance > 1:
                if self.node.left.balance < 0:  
                    self.node.left.lrotate() # we're in case II
                    self.update_heights()
                    self.update_balances()
                self.rrotate()
                self.update_heights()
                self.update_balances()
                
            if self.balance < -1:
                if self.node.right.balance > 0:  
                    self.node.right.rrotate() # we're in case III
                    self.update_heights()
                    self.update_balances()
                self.lrotate()
                self.update_heights()
                self.update_balances()


            
    def rrotate(self):
        # Rotate left pivoting on self
        A = self.node 
        B = self.node.left.node 
        T = B.right.node 
        
        self.node = B 
        B.right.node = A 
        A.left.node = T 

    
    def lrotate(self):
        # Rotate left pivoting on self
        A = self.node 
        B = self.node.right.node 
        T = B.left.node 
        
        self.node = B 
        B.left.node = A 
        A.right.node = T 
        
    def delete_(self, key):
        if self.node != None:
            if self.node.key == key:
                if self.node.left.node == None and self.node.right.node == None:
                    # A leaf node, just remove it
                    self.node = None
                elif self.node.left.node == None: 
                    # Node to be deleted has only right child, replace node by its right child
                    self.node = self.node.right.node
                elif self.node.right.node == None:
                    # Node to be deleted has only left child, replace node by its left child
                    self.node = self.node.left.node
                else:
                    # Node to be deleted has two children
                    # Replacement node can either be the biggest in the left subtree (logical predecessor)
                    # or the smallest in the right subtree (logical successor)
                    # Here, we use the logical predecessor
                    if self.node.left.node != None: 
                        replacement = self.logical_predecessor(self.node)
                        self.node.key = replacement.key
                        # Remove the logical predecessor we've just used
                        self.node.left.delete_(replacement.key)  
                    else: 
                        replacement = self.logical_successor(self.node)
                        self.node.key = replacement.key
                        # Remove the logical successor we've just used
                        self.node.right.delete_(replacement.key)

                self.rebalance()
                return  
            elif key < self.node.key:
                self.node.left.delete_(key)  
            elif key > self.node.key:
                self.node.right.delete_(key)
            self.rebalance()
        else:
            return 

    def update_heights(self, recurse=True):
        if not self.node == None: 
            if recurse: 
                if self.node.left != None: 
                    self.node.left.update_heights()
                if self.node.right != None:
                    self.node.right.update_heights()
            
            self.height = max(self.node.left.height,
                              self.node.right.height) + 1 
        else: 
            self.height = -1 
            
    def update_balances(self, recurse=True):
        if not self.node == None: 
            if recurse: 
                if self.node.left != None: 
                    self.node.left.update_balances()
                if self.node.right != None:
                    self.node.right.update_balances()

            self.balance = self.node.left.height - self.node.right.height 
        else: 
            self.balance = 0 


    def logical_predecessor(self, node):
        node = node.left.node 
        if node != None: 
            while node.right != None:
                if node.right.node == None: 
                    return node 
                else: 
                    node = node.right.node  
        return node 
    
    def logical_successor(self, node):
        node = node.right.node  
        if node != None: # just a sanity check  
            
            while node.left != None:
                if node.left.node == None: 
                    return node 
                else: 
                    node = node.left.node  
        return node 

    def check_balanced(self):
        if self == None or self.node == None: 
            return True
        
        # We always need to make sure we are balanced 
        self.update_heights()
        self.update_balances()
        return ((abs(self.balance) < 2) and self.node.left.check_balanced() and self.node.right.check_balanced())  
        
    def inorder_traverse(self):
        if self.node == None:
            return [] 
        
        inlist = [] 
        l = self.node.left.inorder_traverse()
        for i in l: 
            inlist.append(i) 

        inlist.append(self.node.key)

        l = self.node.right.inorder_traverse()
        for i in l: 
            inlist.append(i) 
    
        return inlist 

    def display(self, level=0, pref=''):    
        self.update_heights()  
        self.update_balances()  
        if(self.node != None): 
            if self.node.left != None:
                self.node.right.display(level + 2, '>')
            print (' ' * level * 2, pref, self.node.key, "[" + str(self.height) + ":" + str(self.balance) + "]", 'L' if self.is_leaf() else ' ')    
            if self.node.left != None: 
                self.node.left.display(level + 2, '<')

         
    def printTreeNoHB(self):           
        def display(root):              
            #   No child.
            if root.node.right.node is None and root.node.left.node is None:
                line = str(root.node.key)
                width = len(line)
                height = 1
                middle = width // 2
                return [line], width, height, middle

            #   Only left child.
            if root.node.right.node is None:
                lines, n, p, x = display(root.node.left)
                nodeOutput = (str(root.node.key) )
                keyLength = len(nodeOutput)
                first_line = (x + 1) * ' ' + (n - x - 1) * '_' + nodeOutput
                second_line = x * ' ' + '/' + (n - x - 1 + keyLength) * ' '
                shifted_lines = [line + keyLength * ' ' for line in lines]
                return [first_line, second_line] + shifted_lines, n + keyLength, p + 2, n + keyLength // 2

            #   Only right child.
            if root.node.left.node is None:
                lines, n, p, x = display(root.node.right)
                nodeOutput = str(root.node.key)
                keyLength = len(nodeOutput)
                first_line = nodeOutput + x * '_' + (n - x) * ' '
                second_line = (keyLength + x) * ' ' + '\\' + (n - x - 1) * ' '
                shifted_lines = [keyLength * ' ' + line for line in lines]
                return [first_line, second_line] + shifted_lines, n + keyLength, p + 2, keyLength // 2

            #   Two children.
            left, n, p, x = display(root.node.left)
            right, m, q, y = display(root.node.right)
            nodeOutput = str(root.node.key)
            keyLength = len(nodeOutput)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + nodeOutput + y * '_' + (m - y) * ' '
            second_line = x * ' ' + '/' + (n - x - 1 + keyLength + y) * ' ' + '\\' + (m - y - 1) * ' '
            if p < q:
                left += [n * ' '] * (q - p)
            elif q < p:
                right += [m * ' '] * (p - q)
            zipped_lines = zip(left, right)
            lines = [first_line, second_line] + [a + keyLength * ' ' + b for a, b in zipped_lines]
            return lines, n + m + keyLength, max(p, q) + 2, n + keyLength // 2

        lines = []
        if self.node != None:
            lines, *_ = display(self)
            print("\t\t== AVL Tree ==")
            print()
        if lines == []:
            print("No tree found, please rebuild a new Tree.\n")
            return -1
        for line in lines:
            print(line)
        print()  
    

    # Postorder traversal from the root
    def postorder(self):
      self.postorderHelper(self.node)

    # Postorder traversal from a subtree
    def postorderHelper(self, root):
      if root != None:
        self.postorderHelper(root.left.node)
        self.postorderHelper(root.right.node)
        print(root.key, end = " ")

    # Preorder traversal from the root
    def preorder(self):
      self.preorderHelper(self.node)

    # Preorder traversal from a subtree
    def preorderHelper(self, root):
      if root != None:
        print(root.key, end = " ")
        self.preorderHelper(root.left.node)
        self.preorderHelper(root.right.node)
    
    # Added function for printing leaf nodes
    def leaf_nodes(self):
        self.leaf_nodes_helper(self.node)

    def leaf_nodes_helper(self, root):
        if root is not None:
            # If a node is a leaf (has no children)
            if root.left.node is None and root.right.node is None:
                print(root.key, end = " ")
            else:
                self.leaf_nodes_helper(root.left.node)
                self.leaf_nodes_helper(root.right.node)
    
    # Added function for printing non-leaf nodes
    def non_leaf_nodes(self):
        self.non_leaf_nodes_helper(self.node)

    def non_leaf_nodes_helper(self, root):
        if root is not None:
            # If a node is not a leaf (has at least one child)
            if root.left.node is not None or root.right.node is not None:
                print(root.key, end = " ")
                self.non_leaf_nodes_helper(root.left.node)
                self.non_leaf_nodes_helper(root.right.node)

############################################## Main Application #####################################################################
def main():
    avl_tree = AVLTree()
    while True:
        print("\nLevel-1 Menu")
        print("1. Pre-load a sequence of integers to build an AVL tree")
        print("2. Manually enter integer values/one by one, to build an AVL tree")
        print("3. Exit")
        option = input("Please choose an option: ")

        if option == "1":
            preloaded_data = [58, 82, -55, 20, 35, 79, 23, 14, 0, -21, 103, 92, 44, 84, 50, 46, 47, 49, 45, 72, 89]
            for data in preloaded_data:
                avl_tree.insert(data)
            level_2_menu(avl_tree)
        elif option == "2":
            while True:
                data = input("Enter an integer (or type 'exit' to stop): ")
                if data == 'exit':
                    break
                avl_tree.insert(int(data))
            level_2_menu(avl_tree)
        elif option == "3":
            print("Exiting the application...")
            break
        else:
            print("Invalid option, please choose again.")

def level_2_menu(avl_tree):
    while True:
        print("\nLevel-2 Menu")
        print("1. Display the AVL tree, showing the height and balance factor for each node.")
        print("2. Print the pre-order, in-order, and post-order traversal sequences of the AVL tree.")
        print("3. Print all leaf nodes of the AVL tree, and all non-leaf nodes (separately).")
        print("4. Insert a new integer key into the AVL tree.")
        print("5. Delete an integer key from the AVL tree.")
        print("6. Exit")
        option = int(input("Please choose an option: "))

        if option == 1:
            print("\n == AVL tree (printed left-side down, with [hights, balance_factors] & an \'L\' for each leaf node) ==\n")     
            avl_tree.display()
            print("\n == AVL tree shape ==\n")
            avl_tree.printTreeNoHB()
        elif option == 2:
            print("\nPre-order traversal: ", end="")
            avl_tree.preorder()
            print("\nPost-order traversal: ", end="")
            avl_tree.postorder()
            print("\nIn-order traversal: ", avl_tree.inorder_traverse(), end="")
        elif option == 3:
            print("\nLeaf nodes: ", end="")
            avl_tree.leaf_nodes()
            print("\nNon-leaf nodes: ", end="")
            avl_tree.non_leaf_nodes()
        elif option == 4:
            key = int(input("Enter the key to insert: "))
            avl_tree.insert(key)
        elif option == 5:
            key = int(input("Enter the key to delete: "))
            avl_tree.delete_(key)
        elif option == 6:
            print("Exiting the application...")
            break
        else:
            print("Invalid option, please choose again.")

if __name__ == "__main__":
    main()

