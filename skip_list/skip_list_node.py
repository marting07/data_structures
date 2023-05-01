class SkipListNode:
    def __init__(self, value, max_level):
        self.value = value
        self.next_nodes = [None] * max_level

    def __str__(self):
        return f"Value: {self.value}, Level: {len(self.next_nodes)}"
