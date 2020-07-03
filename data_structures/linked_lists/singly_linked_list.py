# coding: utf-8
import unittest


class ListNode:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next


class LinkedList:
    def __init__(self, head=None):
        self.head = head

    # O(n)
    def __len__(self):
        length = 0
        current_node = self.head
        while current_node:
            length += 1
            current_node = current_node.next

        return length

    # O(n)
    def __iter__(self):
        current_node = self.head
        while current_node:
            yield current_node.value
            current_node = current_node.next

    # O(n)
    def __getitem__(self, index):
        if index < 0:
            raise ValueError('Negative index is yet not supported')

        current_index = 0
        current_node = self.head
        while current_node:
            if current_index == index:
                return current_node.value
            else:
                current_node = current_node.next
                current_index += 1

        raise IndexError

    # O(n)
    def __setitem__(self, index, value):
        if index < 0:
            raise ValueError('Negative index is yet not supported')

        current_node = self.head
        current_index = 0
        while current_node:
            if current_index == index:
                current_node.value = value
                return
            current_node = current_node.next
            current_index += 1

        raise IndexError

    # O(n), O(1) if it inserts before the first item
    def insert_before(self, index, value):
        if index < 0:
            raise ValueError('Negative index is yet not supported')

        new_node = ListNode(value)
        if not self.head:
            self.head = new_node
            return

        if index == 0:
            new_node.next = self.head
            self.head = new_node
        else:
            current_node = self.head
            current_index = 0
            while current_node:
                # We find the node that before the node at the index we are looking for
                if current_index == index - 1:
                    target_node = current_node.next
                    current_node.next = new_node
                    new_node.next = target_node
                    return

                current_node = current_node.next
                current_index += 1

            raise IndexError

    # O(n), O(1) if it pops the first item
    def pop(self, index):
        if index < 0:
            raise ValueError('Negative index is yet not supported')

        if index == 0:
            if not self.head:
                raise IndexError('pop from empty linked list')

            deleted_value = self.head.value
            self.head = self.head.next
            return deleted_value
        else:
            previous_node = self.head
            current_node = self.head.next
            current_index = 1
            while current_node:
                if current_index == index:
                    deleted_value = current_node.value
                    previous_node.next = current_node.next
                    return deleted_value

                previous_node = current_node
                current_node = current_node.next
                current_index += 1

            raise IndexError

    # O(n)
    def index(self, value):
        current_index = 0
        current_node = self.head
        while current_node:
            if current_node.value == value:
                return current_index
            current_node = current_node.next
            current_index += 1

        raise ValueError(f'{value} is not in linked list')

    # O(n)
    def append(self, value):
        new_node = ListNode(value)
        if not self.head:
            self.head = new_node
            return

        current_node = self.head
        while current_node.next:
            current_node = current_node.next
        current_node.next = new_node

    # O(n)
    def reverse(self):
        previous_node = None
        current_node = self.head
        while current_node:
            next_node = current_node.next
            current_node.next = previous_node
            previous_node = current_node
            current_node = next_node

        self.head = previous_node


class TestCase(unittest.TestCase):
    def setUp(self):
        self.empty_linked_list = LinkedList()

        self.node_0 = ListNode('nobody exists on purpose')
        self.node_1 = ListNode('nobody belongs anywhere')
        self.node_2 = ListNode('everybody is gonna die')
        self.node_3 = ListNode('come writing Python')
        self.node_0.next = self.node_1
        self.node_1.next = self.node_2
        self.node_2.next = self.node_3
        self.linked_list = LinkedList(self.node_0)

    def test__len__(self):
        self.assertEqual(len(self.empty_linked_list), 0)
        self.assertEqual(len(self.linked_list), 4)

    def test__iter__(self):
        self.assertEqual(list(self.empty_linked_list), [])
        self.assertEqual(list(self.linked_list), [self.node_0.value, self.node_1.value, self.node_2.value, self.node_3.value])

    def test__getitem__(self):
        with self.assertRaises(IndexError):
            print(self.empty_linked_list[0])

        self.assertEqual(self.linked_list[0], self.node_0.value)
        self.assertEqual(self.linked_list[1], self.node_1.value)
        self.assertEqual(self.linked_list[2], self.node_2.value)
        self.assertEqual(self.linked_list[3], self.node_3.value)

        with self.assertRaises(IndexError):
            print(self.linked_list[4])

    def test__setitem__(self):
        with self.assertRaises(IndexError):
            self.empty_linked_list[0] = 0

        self.linked_list[0] = '0'
        self.linked_list[1] = '1'
        self.linked_list[3] = '3'
        self.assertEqual(self.linked_list.head.value, '0')
        self.assertEqual(self.linked_list[0], '0')
        self.assertEqual(self.linked_list[1], '1')
        self.assertEqual(self.linked_list[2], self.node_2.value)
        self.assertEqual(self.linked_list[3], '3')

        with self.assertRaises(IndexError):
            self.linked_list[4] = '4'

    def test_insert(self):
        self.empty_linked_list.insert_before(0, '0')
        self.assertEqual(self.empty_linked_list[0], '0')

        self.linked_list.insert_before(0, '0')
        self.linked_list.insert_before(1, '1')
        self.linked_list.insert_before(3, '3')
        self.linked_list.insert_before(6, '6')
        self.linked_list.insert_before(8, '8')
        expected = [
            '0',
            '1',
            self.node_0.value,
            '3',
            self.node_1.value,
            self.node_2.value,
            '6',
            self.node_3.value,
            '8',
        ]
        self.assertEqual(self.linked_list.head.value, '0')
        self.assertEqual(list(self.linked_list), expected)

        with self.assertRaises(IndexError):
            self.linked_list.insert_before(10, '10')

    def test_pop(self):
        with self.assertRaises(IndexError):
            self.empty_linked_list.pop(0)

        self.assertEqual(self.linked_list.pop(0), self.node_0.value)
        self.assertEqual(self.linked_list.pop(2), self.node_3.value)
        expected = [
            self.node_1.value,
            self.node_2.value,
        ]
        self.assertEqual(self.linked_list.head.value, self.node_1.value)
        self.assertEqual(list(self.linked_list), expected)

        with self.assertRaises(IndexError):
            self.linked_list.pop(10)

    def test_index(self):
        self.assertEqual(self.linked_list.index(self.node_0.value), 0)
        self.assertEqual(self.linked_list.index(self.node_1.value), 1)
        self.assertEqual(self.linked_list.index(self.node_2.value), 2)
        self.assertEqual(self.linked_list.index(self.node_3.value), 3)

        with self.assertRaises(ValueError):
            print(self.linked_list.index('NOT EXIST'))

    def test_append(self):
        self.empty_linked_list.append('0')
        self.assertEqual(self.empty_linked_list.head.value, '0')
        self.assertEqual(self.empty_linked_list[0], '0')

        self.linked_list.append('4')
        expected = [
            self.node_0.value,
            self.node_1.value,
            self.node_2.value,
            self.node_3.value,
            '4',
        ]
        self.assertEqual(list(self.linked_list), expected)

    def test_reverse(self):
        self.empty_linked_list.reverse()
        self.assertEqual(list(self.empty_linked_list), [])

        self.linked_list.reverse()
        expected = [
            self.node_3.value,
            self.node_2.value,
            self.node_1.value,
            self.node_0.value,
        ]
        self.assertEqual(self.linked_list.head.value, self.node_3.value)
        self.assertEqual(list(self.linked_list), expected)


if __name__ == '__main__':
    unittest.main()
