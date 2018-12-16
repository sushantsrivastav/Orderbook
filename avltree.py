from array import array

MAXSTACK = 32


class Node(object):
    """Internal object, represents a tree node."""
    __slots__ = ['left', 'right', 'balance', 'key', 'value']

    def __init__(self, key=None, value=None):
        self.left = None
        self.right = None
        self.key = key
        self.value = value
        self.balance = 0

    def __getitem__(self, key):
        """N.__getitem__(key) <==> x[key], where key is 0 (left) or 1 (right)."""
        return self.left if key == 0 else self.right

    def __setitem__(self, key, value):
        """N.__setitem__(key, value) <==> x[key]=value, where key is 0 (left) or 1 (right)."""
        if key == 0:
            self.left = value
        else:
            self.right = value

    def free(self):
        """Remove all references."""
        self.left = None
        self.right = None
        self.key = None
        self.value = None


def height(node):
    return node.balance if node is not None else -1


def jsw_single(root, direction):
    other_side = 1 - direction
    save = root[other_side]
    root[other_side] = save[direction]
    save[direction] = root
    rlh = height(root.left)
    rrh = height(root.right)
    slh = height(save[other_side])
    root.balance = max(rlh, rrh) + 1
    save.balance = max(slh, root.balance) + 1
    return save


def jsw_double(root, direction):
    other_side = 1 - direction
    root[other_side] = jsw_single(root[other_side], other_side)
    return jsw_single(root, direction)


class AVLTree(object):

    def __init__(self):
        self._root = None
        self._count = 0

    def _new_node(self, key, value):
        """Create a new tree node."""
        self._count += 1
        return Node(key, value)

    def insert(self, key, value):
        """T.insert(key, value) <==> T[key] = value, insert key, value into tree."""
        if self._root is None:
            self._root = self._new_node(key, value)
        else:
            node_stack = []  # node stack
            dir_stack = array('I')  # direction stack
            done = False
            top = 0
            node = self._root
            # search for an empty link, save path
            while True:
                if key == node.key:  # update existing item
                    node.value = value
                    return
                direction = 1 if key > node.key else 0
                dir_stack.append(direction)
                node_stack.append(node)
                if node[direction] is None:
                    break
                node = node[direction]

            # Insert a new node at the bottom of the tree
            node[direction] = self._new_node(key, value)

            # Walk back up the search path
            top = len(node_stack) - 1
            while (top >= 0) and not done:
                direction = dir_stack[top]
                other_side = 1 - direction
                top_node = node_stack[top]
                left_height = height(top_node[direction])
                right_height = height(top_node[other_side])

                # Terminate or rebalance as necessary */
                if left_height - right_height == 0:
                    done = True
                if left_height - right_height >= 2:
                    a = top_node[direction][direction]
                    b = top_node[direction][other_side]

                    if height(a) >= height(b):
                        node_stack[top] = jsw_single(top_node, other_side)
                    else:
                        node_stack[top] = jsw_double(top_node, other_side)

                    # Fix parent
                    if top != 0:
                        node_stack[top - 1][dir_stack[top - 1]] = node_stack[top]
                    else:
                        self._root = node_stack[0]
                    done = True

                # Update balance factors
                top_node = node_stack[top]
                left_height = height(top_node[direction])
                right_height = height(top_node[other_side])

                top_node.balance = max(left_height, right_height) + 1
                top -= 1

    def remove(self, key):
        """T.remove(key) <==> del T[key], remove item <key> from tree."""
        if self._root is None:
            raise KeyError(str(key))
        else:
            node_stack = [None] * MAXSTACK  # node stack
            dir_stack = array('I', [0] * MAXSTACK)  # direction stack
            top = 0
            node = self._root

            while True:
                # Terminate if not found
                if node is None:
                    raise KeyError(str(key))
                elif node.key == key:
                    break

                # Push direction and node onto stack
                direction = 1 if key > node.key else 0
                dir_stack[top] = direction

                node_stack[top] = node
                node = node[direction]
                top += 1

            # Remove the node
            if (node.left is None) or (node.right is None):
                # Which child is not null?
                direction = 1 if node.left is None else 0

                # Fix parent
                if top != 0:
                    node_stack[top - 1][dir_stack[top - 1]] = node[direction]
                else:
                    self._root = node[direction]
                node.free()
                self._count -= 1
            else:
                # Find the inorder successor
                heir = node.right

                # Save the path
                dir_stack[top] = 1
                node_stack[top] = node
                top += 1

                while heir.left is not None:
                    dir_stack[top] = 0
                    node_stack[top] = heir
                    top += 1
                    heir = heir.left

                # Swap data
                node.key = heir.key
                node.value = heir.value

                # Unlink successor and fix parent
                xdir = 1 if node_stack[top - 1].key == node.key else 0
                node_stack[top - 1][xdir] = heir.right
                heir.free()
                self._count -= 1

            # Walk back up the search path
            top -= 1
            while top >= 0:
                direction = dir_stack[top]
                other_side = 1 - direction
                top_node = node_stack[top]
                left_height = height(top_node[direction])
                right_height = height(top_node[other_side])
                b_max = max(left_height, right_height)

                # Update balance factors
                top_node.balance = b_max + 1

                # Terminate or rebalance as necessary
                if (left_height - right_height) == -1:
                    break
                if (left_height - right_height) <= -2:
                    a = top_node[other_side][direction]
                    b = top_node[other_side][other_side]
                    if height(a) <= height(b):
                        node_stack[top] = jsw_single(top_node, direction)
                    else:
                        node_stack[top] = jsw_double(top_node, direction)
                    # Fix parent
                    if top != 0:
                        node_stack[top - 1][dir_stack[top - 1]] = node_stack[top]
                    else:
                        self._root = node_stack[0]
                top -= 1

    def is_empty(self):
        return self._count == 0

    def max_item(self):
        if self.is_empty():
            raise ValueError("Tree is empty")
        node = self._root
        while node.right is not None:
            node = node.right
        return node.key, node.value

    def min_item(self):
        if self.is_empty():
            raise ValueError("Tree is empty")
        node = self._root
        while node.left:
            node = node.left
        return node.key, node.value

    def min_key(self):
        return self.min_item()[0]

    def max_key(self):
        return self.max_item()[0]
