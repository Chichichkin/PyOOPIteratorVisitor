from __future__ import annotations

import random
from abc import ABC, abstractmethod
from collections.abc import Iterable, Iterator


class Tree(Iterable):
    def __init__(self, root):
        self.root = root
        self.Nodes = []

    def __iter__(self) -> WidthOrderIterator:
        return WidthOrderIterator(self.Nodes)

    def get_reverse_iterator(self) -> WidthOrderIterator:
        return WidthOrderIterator(self.Nodes, True)

    def add_node(self, obj):
        self.Nodes.append(obj)

    def get_all_nodes(self):
        print(*self.Nodes, sep="\n")
        print('Tree Size:' + str(len(self.Nodes)))


class WidthOrderIterator(Iterator):
    _position: int = None
    _reverse: bool = False

    def __init__(self, collection, reverse: bool = False) -> None:
        self._collection = collection
        self._reverse = reverse
        self._position = -1 if reverse else 0

    def __next__(self):
        try:
            value = self._collection[self._position]
            self._position += -1 if self._reverse else 1
        except IndexError:
            raise StopIteration()

        return value


class Node(ABC):

    def __init__(self, data, index, parent: Node = None):
        self.data = data
        self.index = index
        self.parent = parent
        self.children = []

    def add_node(self, obj):
        self.children.append(obj)

    @abstractmethod
    def accept(self, visitor: Visitor) -> None:
        pass


class BlackNode(Node):

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_black(self)

    def black_info(self) -> str:
        return f"Node {self.index} is {self.data}"


class WhiteNode(Node):

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_white(self)

    def white_info(self) -> str:
        return f"Node {self.index} is {self.data}"


class Visitor(ABC):
    @abstractmethod
    def visit_black(self, element: BlackNode) -> None:
        pass

    @abstractmethod
    def visit_white(self, element: WhiteNode) -> None:
        pass


class ConcreteVisitor1(Visitor):
    def visit_black(self, element) -> None:
        print(f"{element.black_info()} + ConcreteVisitor1")

    def visit_white(self, element) -> None:
        print(f"{element.white_info()} + ConcreteVisitor1")


class ConcreteVisitor2(Visitor):
    def visit_black(self, element) -> None:
        print(f"{element.black_info()} + ConcreteVisitor2")

    def visit_white(self, element) -> None:
        print(f"{element.white_info()} + ConcreteVisitor2")


def find_node(index: int, node: Node):
    if node.index == index:
        return node
    elif len(node.children) == 0:
        return 0
    else:
        for child in node.children:
            res = find_node(index, child)
            if res != 0:
                return res
        return 0


def create_tree(node_list: list):
    counter = 1
    if len(node_list) != 0:
        if bool(random.getrandbits(1)):
            root_node = WhiteNode("White", counter)
        else:
            root_node = BlackNode("Black", counter)
        new_tree = Tree(root_node)
        new_tree.add_node(root_node)
        for i in range(len(node_list)):
            num_creat = node_list[i]
            work_node = find_node(i + 1, root_node)
            while num_creat > 0:
                counter += 1
                if bool(random.getrandbits(1)):
                    child_node = WhiteNode("White", counter, work_node)
                else:
                    child_node = BlackNode("Black", counter, work_node)
                work_node.add_node(child_node)
                new_tree.add_node(child_node)
                num_creat -= 1
        return new_tree
    return 0


if __name__ == "__main__":
    s = [2, 2, 1, 2, 0, 2]
    tree = create_tree(s)
    if tree == 0:
        exit(-1)
    visitor1 = ConcreteVisitor1()
    for node in tree:
        node.accept(visitor1)
    visitor2 = ConcreteVisitor2()
    for node in tree.get_reverse_iterator():
        node.accept(visitor2)
