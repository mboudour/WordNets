

class LinkedListNode:

    def __init__(self, inData, inNext):
        """Construct a new Linked List Node"""
        self.data = inData
        self.next = inNext

class LinkedList:

    def __init__(self):
        """Construct a new LinkedList. The first node and last node are the same. Size is 0"""
        self.firstNode = LinkedListNode(None, None)
        self.lastNode = self.firstNode
        self.size = 0
    def add(self, data):
        """Add a node to the list"""
        node = LinkedListNode(data, None)
        node.data = data;

        if self.firstNode.data == None:
            self.firstNode = node
            self.lastNode = node
        else:
            self.lastNode.next = node
            self.lastNode = node

        self.size += 1

    def add_many(self, list_of_data):
        """Add a list of nodes to the linked list"""
        for x in list_of_data:
            self.add(x)
    def remove(self, data):
        """Remove a node from the list"""
        currentNode = self.firstNode
        wasDeleted = False

        if self.size == 0:
            pass

        # The first node is being removed
        if data == currentNode.data:
            # This is the case where we have only one node in the list
            if currentNode.next == None:
                self.firstNode = LinkedListNode(None, None)
                self.lastNode = self.firstNode
                self.size = self.size - 1
                return

            # Here there are more than one nodes in the list
            currentNode = currentNode.next
            self.firstNode = currentNode
            self.size = self.size - 1
            return;

        while True:

            if currentNode == None:
                wasDeleted = False
                break

            # Check if the data of the next is what we're looking for
            nextNode = currentNode.next
            if nextNode != None:
                if data == nextNode.data:
                    # Found the right one, loop around the node
                    nextNextNode = nextNode.next
                    currentNode.next = nextNextNode

                    nextNode = None
                    wasDeleted = True
                    break

            currentNode = currentNode.next

        if wasDeleted:
            self.size = self.size - 1;

    def remove_many(self, list_of_data):
        """Remove a list of nodes from the linked list"""
        for x in list_of_data:
            self.remove(x)
    def to_string(self):
        """Get a string representation of the list"""
        result = ""
        currentNode = self.firstNode
        i = 0

        result = result + "{"

        while currentNode != None:
            if i > 0:
                result = result + ","

            dataObj = currentNode.data

            if dataObj != None:
                result = result + dataObj

            currentNode = currentNode.next

            i = i + 1

        result = result + "}"
        return result

    def contains(self, data):
        """Check whether a node is in the list or not"""
        currentNode = self.firstNode

        while currentNode != None:
            if currentNode.data == data:
                return True
            else:
                currentNode = currentNode.next

        return False

    def index_of(self, data):
        """Find the position of a node in the list"""
        currentNode = self.firstNode
        pos = 0

        while currentNode != None:
            if (currentNode.data == data):
                return pos
            else:
                currentNode = currentNode.next
                pos = pos + 1

        return -1    

    def get_size(self):
        """Get the size of the list"""
        return self.size

