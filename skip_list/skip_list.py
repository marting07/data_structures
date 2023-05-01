import random

from skip_list.skip_list_node import SkipListNode


class SkipList:
    def __init__(self, max_level=4, p=0.5):
        self.max_level = max_level
        self.p = p
        self.head = SkipListNode(None, max_level)

    def random_level(self):
        level = 1
        while random.random() < self.p and level < self.max_level:
            level += 1
        return level

    def __str__(self):
        result = []
        node = self.head.next_nodes[0]
        while node:
            result.append(str(node.value))
            node = node.next_nodes[0]
        return " -> ".join(result)

    def search(self, value):
        current_node = self.head
        # Traverse the levels from top to bottom
        for level in range(self.max_level - 1, -1, -1):
            while current_node.next_nodes[level] and current_node.next_nodes[level].value < value:
                current_node = current_node.next_nodes[level]
        current_node = current_node.next_nodes[0]
        if current_node and current_node.value == value:
            return current_node
        else:
            return None

    def insert(self, value):
        # Search for the position where the new element should be inserted,
        # keeping track of the nodes at each level
        update_nodes = [None] * self.max_level
        current_node = self.head
        for level in range(self.max_level - 1, -1, -1):
            while current_node.next_nodes[level] and current_node.next_nodes[level].value < value:
                current_node = current_node.next_nodes[level]
            update_nodes[level] = current_node
        # Create a new node with the value and a randomly generated level
        new_node_level = self.random_level()
        new_node = SkipListNode(value, new_node_level)
        # Insert the new node into the appropriate levels of the list
        for level in range(new_node_level):
            new_node.next_nodes[level] = update_nodes[level].next_nodes[level]
            update_nodes[level].next_nodes[level] = new_node

    def delete(self, value):
        # Search for the element to be deleted, keeping track of the nodes at each level
        update_nodes = [None] * self.max_level
        current_node = self.head
        for level in range(self.max_level - 1, -1, -1):
            while current_node.next_nodes[level] and current_node.next_nodes[level].value < value:
                current_node = current_node.next_nodes[level]
            update_nodes[level] = current_node
        # Check if the element is found at the bottom level (Level 0)
        target_node = current_node.next_nodes[0]
        if target_node and target_node.value == value:
            # Remove the target node from all the levels it is present in
            for level in range(len(target_node.next_nodes)):
                update_nodes[level].next_nodes[level] = target_node.next_nodes[level]
            # Remove any empty levels from the top of the list
            while self.max_level > 1 and not self.head.next_nodes[self.max_level - 1]:
                self.max_level -= 1
            return True
        else:
            # Element not found
            return False
