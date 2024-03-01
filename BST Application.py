def printTree(root, element="element", left="left", right="right"):                              
    def display(root, element=element, left=left, right=right):                                    
        """Returns list of strings, width, height, and horizontal coordinate of the root."""
        # No child.
        if getattr(root, right) is None and getattr(root, left) is None:
            line = '%s' % getattr(root, element)
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if getattr(root, right) is None:
            lines, n, p, x = display(getattr(root, left))
            s = '%s' % getattr(root, element)
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if getattr(root, left) is None:
            lines, n, p, x = display(getattr(root, right))
            s = '%s' % getattr(root, element)
            u = len(s)
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
        left, n, p, x = display(getattr(root, left))
        right, m, q, y = display(getattr(root, right))
        s = '%s' % getattr(root, element)
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
        if p < q:
            left += [n * ' '] * (q - p)
        elif q < p:
            right += [m * ' '] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2
    
    lines = []
    if root != None:
        lines, *_ = display(root, element, left, right)
    print("\t== Binary Tree: shape ==")
    print()
    if lines == []:
        print("\t  No tree found")
    for line in lines:
        print("\t", line)
    print()

class BinaryTree:
    def __init__(self):
        self.root = None
        self.size = 0

    # Insert element e into the binary search tree
    # Return True if the element is inserted successfully
    def insert(self, e):
        if self.root == None:
          self.root = self.createNewNode(e) # Create a new root
        else:
          # Locate the parent node
          parent = None
          current = self.root
          while current != None:
            if e < current.element:
              parent = current
              current = current.left
            elif e > current.element:
              parent = current
              current = current.right
            else:
              return False # Duplicate node? not inserted

          # Create the new node and attach it to the parent node
          if e < parent.element:
            parent.left = self.createNewNode(e)
          else:
            parent.right = self.createNewNode(e)

        self.size += 1 # Increase tree size
        return True # Element inserted

    # Create a new TreeNode for element e
    def createNewNode(self, e):
      return TreeNode(e)

    # Inorder traversal from the root
    def inorder(self):
      self.inorderHelper(self.root)

    # Inorder traversal from a subtree
    def inorderHelper(self, r):
      if r != None:
        self.inorderHelper(r.left)
        print(r.element, end = " ")
        self.inorderHelper(r.right)
  
    def inverse_inorder(self):
        self.inverse_inorderHelper(self.root)

    def inverse_inorderHelper(self, root):
        if root != None:
            self.inverse_inorderHelper(root.right)
            print(root.element, end = " ")
            self.inverse_inorderHelper(root.left)
    
    def leaf_BST(self):
        self.leaf_BSTHelper(self.root)

    def leaf_BSTHelper(self, node):
        if node:
            if node.left is None and node.right is None:
                print(node.element, end = " ")
            else:
                self.leaf_BSTHelper(node.left)
                self.leaf_BSTHelper(node.right)

    def non_leaf_BST(self):
        self.non_leaf_BSTHelper(self.root)

    def non_leaf_BSTHelper(self, node):
        if node:
            if node.left is not None or node.right is not None:
                print(node.element, end = " ")
            self.non_leaf_BSTHelper(node.left)
            self.non_leaf_BSTHelper(node.right)
    
    def total_nodesBST(self, N):
        node = self.searchNode(N)
        if node:
            count = self.total_nodesBSTHelper(node)
            return node, count
        else:
            return None, 0

    def total_nodesBSTHelper(self, node):
        if node is None:
            return 0
        else:
            return 1 + self.total_nodesBSTHelper(node.left) + self.total_nodesBSTHelper(node.right)
    
    def depth_nodeBST(self, N):
        depth = 0
        current = self.root
        while current != None:
            if N < current.element:
                current = current.left
                depth += 1
            elif N > current.element:
                current = current.right
                depth += 1
            else:
                return depth
        return None
    
    def depth_subtreeBST(self, N):
        node = self.searchNode(N)
        if node:
            return self.depth_subtreeBSTHelper(node)
        else:
            return None

    def depth_subtreeBSTHelper(self, node):
        if node is None:
            return -1
        else:
            left_depth = self.depth_subtreeBSTHelper(node.left)
            right_depth = self.depth_subtreeBSTHelper(node.right)
            return max(left_depth, right_depth) + 1
    
    def delete_(self, key):
        self.root, deleted = self.deleteHelper(self.root, key)
        if deleted:
            self.size -= 1
        return deleted

    def deleteHelper(self, node, key):
        if node is None:
            return node, False

        deleted = False
        if key < node.element:
            node.left, deleted = self.deleteHelper(node.left, key)
        elif key > node.element:
            node.right, deleted = self.deleteHelper(node.right, key)
        else:
            if node.left is None:
                return node.right, True
            elif node.right is None:
                return node.left, True

            temp_val = self.findMinValue(node.right)
            node.element = temp_val
            node.right, deleted = self.deleteHelper(node.right, temp_val)
        return node, deleted

    def findMinValue(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current.element
    
    # Postorder traversal from the root
    def postorder(self):
      self.postorderHelper(self.root)

    # Postorder traversal from a subtree
    def postorderHelper(self, root):
      if root != None:
        self.postorderHelper(root.left)
        self.postorderHelper(root.right)
        print(root.element, end = " ")

    # Preorder traversal from the root
    def preorder(self):
      self.preorderHelper(self.root)

    # Preorder traversal from a subtree
    def preorderHelper(self, root):
      if root != None:
        print(root.element, end = " ")
        self.preorderHelper(root.left)
        self.preorderHelper(root.right)

    # Return true if the tree is empty
    def isEmpty(self):
      return self.size == 0

    # Remove all elements from the tree
    def clear(self):
      self.root == None
      self.size == 0

    # Return the root of the tree
    def getRoot(self):
      return self.root
    
    def searchNode(self, N):
        current = self.root # Start from the root

        while current != None:
            if N < current.element:
                current = current.left
            elif N > current.element:
                current = current.right
            else: # element matches current.element
                return current # Node is found

        return None

class TreeNode:
    def __init__(self, e):
      self.element = e
      self.left = None # Point to the left node, default None
      self.right = None # Point to the right node, default None

############################################## Main Application #####################################################################
def main():
    binary_tree = BinaryTree()
    while True:
        print("\nLevel-1 Menu")
        print("1. Pre-load a sequence of integers to build a BST")
        print("2. Manually enter integer values, one by one, to build a BST")
        print("3. Exit")
        option = input("Please choose an option: ")

        if option == "1":
            preloaded_data = [58, 84, 68, 23, 38, 82, 26, 17, 24, 106, 95, 48, 88, 54, 50, 51, 53, 49, -6, -46]
            for data in preloaded_data:
                binary_tree.insert(data)
            level_2_menu(binary_tree)
        elif option == "2":
            while True:
                data = input("Enter an integer (or type 'exit' to stop): ")
                if data == 'exit':
                    break
                if data.isdigit():
                    binary_tree.insert(int(data))
                else:
                    print("Invalid input. Try again")   
            level_2_menu(binary_tree)
        elif option == "3":
            print("Exiting the application...")
            break
        else:
            print("Invalid option, please choose again.")

def level_2_menu(binary_tree):
    while True:
        print("\nLevel-2 Menu")
        print("1. Display the tree shape of current BST, and then show the pre-order, in-order, post-order and inverse-in-order traversal sequences of the BST")
        print("2. Show all leaf nodes of the BST, and all non-leaf nodes")
        print("3. Show a sub-tree and count its nodes")
        print("4. Show the depth of a given node in the BST")
        print("5. Show the depth of a subtree of the BST")
        print("6. Insert a new integer key into the BST")
        print("7. Delete an integer key from the BST")
        print("8. Exit")
        option = input("Please choose an option: ")

        if option == "1":
            printTree(binary_tree.getRoot())
            print("\nPre-order traversal: ", end="")
            binary_tree.preorder()
            print("\nIn-order traversal: ", end="")
            binary_tree.inorder()
            print("\nPost-order traversal: ", end="")
            binary_tree.postorder()
            print("\nInverse in-order traversal: ", end="")
            binary_tree.inverse_inorder()
        elif option == "2":
            print("\nLeaf nodes: ", end="")
            binary_tree.leaf_BST()
            print("\nNon-leaf nodes: ", end="")
            binary_tree.non_leaf_BST()
        elif option == "3":
            node_key = int(input("Enter the node key to search: "))
            node, count = binary_tree.total_nodesBST(node_key)
            if node:
                print("\nTotal nodes in the subtree rooted at", node_key, "is", count)
                printTree(node)
            else:
                print("ERROR: Node", node_key, "not found!")
        elif option == "4":
            node_key = int(input("Enter the node key to search: "))
            node = binary_tree.searchNode(node_key)
            if node:
                print("Depth of the node", node_key, "is", binary_tree.depth_nodeBST(node_key))
            else:
                print("ERROR: Node", node_key, "not found!")
        elif option == "5":
            node_key = int(input("Enter the node key to search: "))
            depth = binary_tree.depth_subtreeBST(node_key)
            if depth:
                print("Depth of the subtree rooted at", node_key, "is", binary_tree.depth_subtreeBST(node_key))
            else:
                print("ERROR: Subtree rooted at node", node_key, "not found!")
        elif option == "6":
            node_key = int(input("Enter the new node key to insert: "))
            if binary_tree.insert(node_key):
                print("Node", node_key, "inserted successfully.")
                print("Inverse in-order traversal: ",  end="") 
                binary_tree.inverse_inorder()
                print("\n")
            else:
                print("ERROR: node key", node_key, "already exists in the BST!")
        elif option == "7":
            node_key = int(input("Enter the node key to delete: "))
            if binary_tree.delete_(node_key):
                print("Node", node_key, "deleted successfully.")
                print("Inverse in-order traversal: ",  end="") 
                binary_tree.inverse_inorder()
            else:
                print("ERROR: Node", node_key, "not found!")
        elif option == "8":
            print("Exiting to Level-1 menu...")
            break
        else:
            print("Invalid option, please choose again.")

if __name__ == "__main__":
    main()
