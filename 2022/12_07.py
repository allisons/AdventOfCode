import argparse
import unittest
import numpy as np
import re
from collections import defaultdict
from functools import partial
from heapq import nsmallest 

class Test(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.testinput = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""
        
        cls.testinput2 = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir a
dir e
29116 f
2557 g
62596 h.lst
$ cd a
1000 fake.txt
$ cd ..
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""
        
    def test_parse_input(self):
        pass
        
    
    def test_create_tree(self):
        root = NodeTree("/")
        self.assertEqual("\ndir /",root.__str__())
        root.add_node_child("a",root)
        a = root.get_child('a')
        self.assertEqual("\ndir a",a.__str__())
        self.assertEqual("\ndir /\ndir a",root.__str__())
        root.add_leaf_child("b.txt",14848514,root)
        root.add_leaf_child("c.data",8504156,root)
        root.add_node_child("d",root)
        self.assertEqual("""
dir /
dir a
14848514 b.txt
8504156 c.data
dir d""",root.__str__())
    def test_tree_build(self):
        pointer = NodeTree("/")
        pointer.add_node_child("a",pointer)
        pointer.add_leaf_child("b.txt",14848514,pointer)
        pointer.add_leaf_child("c.data",8504156,pointer)
        pointer.add_node_child("d",pointer)
        pointer = pointer.get_child("a")
        pointer.add_node_child("e",pointer)
        pointer.add_leaf_child("f",29116,pointer)
        pointer.add_leaf_child("g",2557,pointer)
        pointer.add_leaf_child("h.lst",62596,pointer)
        self.assertEqual("""
dir /
dir a
dir e
29116 f
2557 g
62596 h.lst
14848514 b.txt
8504156 c.data
dir d""",pointer.parent.__str__())
        pointer = pointer.get_child("e")
        pointer.add_leaf_child("i",584,pointer)
        pointer = pointer.parent
        pointer = pointer.parent
        pointer = pointer.get_child("d")
        pointer.add_leaf_child("j",4060174,pointer)
        pointer.add_leaf_child("d.log",8033020,pointer)
        pointer.add_leaf_child("d.ext",5626152,pointer)
        pointer.add_leaf_child("k",7214296,pointer)
        

    def test_build_tree(self):
        tree = build_tree(parse_input(self.testinput))
        self.assertEqual(tree.name,"/")
        self.assertEqual(tree.get_child('a').name,"a")
        self.assertEqual(tree.get_child('a').get_child('e').name,"e")
        self.assertEqual(tree.get_child("b.txt").name,"b.txt")
        self.assertEqual(tree.get_child("d").get_child("j").size,4060174)
        
    def test_size_calc(self):
        tree = build_tree(parse_input(self.testinput))
        self.assertEqual(tree.get_child('a').get_child('e').calculate_size(),584)
        self.assertEqual(tree.get_child('a').calculate_size(),94853)
        self.assertEqual(tree.get_child('d').calculate_size(),24933642)
        self.assertEqual(tree.calculate_size(),48381165)
        
    def test_little_children(self):
        tree = build_tree(parse_input(self.testinput))
        little_children = tree.little_children(tree.name,{})
        self.assertEqual(sum(little_children.values()),95437)

    def test_little_children(self):
        tree = build_tree(parse_input(self.testinput))
        little_children = tree.little_children(tree.name,{})
        self.assertEqual(sum(little_children.values()),95437)
        
    def test_big_children(self):
        tree = build_tree(parse_input(self.testinput))
        expected = {'/': 48381165, '/d': 24933642}
        big_children = tree.big_children(8381165,tree.name,{"/":tree.calculate_size()})
        self.assertEqual(expected,big_children)
    
    def test_puzzle1(self):
        tree = build_tree(parse_input(self.testinput))
        self.assertEqual(sum(tree.little_children(tree.name,{}).values()),95437)
    def test_nested_a(self):
        tree = build_tree(parse_input(self.testinput2))
        self.assertEqual(tree.calculate_size(),48382165)
        self.assertEqual(tree.get_child("a").get_child("a").calculate_size(),1000)
        
        
    def test_puzzle2(self):
        self.assertEqual(puzzle2(self.testinput),24933642)
        

class NodeTree(object):
    
    def __init__(self,name,parent=None):
        self.children = {}
        self.name = name
        self.isTerminal = True
        self.parent = parent
        
    def get_child(self,child_name):
        return self.children[child_name]
    
    def add_node_child(self,child_name,parent):
        assert child_name not in self.children.keys()
        self.isTerminal = False
        self.children[child_name] = NodeTree(child_name,parent=parent)
    
    def add_leaf_child(self,child_name,size,parent):
        assert child_name not in self.children.keys()
        self.children[child_name] = NodeLeaf(child_name,size,parent)

    def get_parent(self):
        return self.parent
    
    def calculate_size(self):
        size = 0
        if self.isTerminal:
            return sum([child.size for child in self.children.values()])
        else:
            for child in self.children.values():
                if isinstance(child,NodeLeaf):
                    size+=child.size
                else:
                    size+=child.calculate_size()
        return size
    
    def little_children(self,root,sizemap):
        for child in self.children.values():
            mysize = child.calculate_size()
            if isinstance(child,NodeLeaf):
                continue
            elif mysize <= 100000:
                sizemap[root+child.name] = mysize
            child.little_children(root+child.name+"/",sizemap)
        return sizemap
    
    def big_children(self,need_space,root,sizemap):
        for child in self.children.values():
            mysize = child.calculate_size()
            if isinstance(child,NodeLeaf):
                continue
            elif mysize >= need_space:
                sizemap[root+child.name] = mysize
            child.big_children(need_space,root+child.name+"/",sizemap)
        return sizemap
            

    
        
    def __str__(self):
    
        return f"\ndir {self.name}"+"".join([child.__str__() for name,child in self.children.items()])
        
        
class NodeLeaf(object):
    def __init__(self,name,size,parent):
        self.name = name
        self.size=size
        self.parent = parent
    def calculate_size(self):
        return self.size
    
    
    def __str__(self):
        return f"\n{self.size} {self.name}"

def parse_input(text):
    return text.split("\n")

def build_tree(lines):
    pointer = NodeTree("/")
    for line in lines[1:]:
        args = line.split()
        if args[0] == "dir":
            pointer.add_node_child(args[1],pointer)
        elif args[0].isnumeric():
            pointer.add_leaf_child(args[1],int(args[0]),pointer)
        elif args[0:2] == ["$","cd"]:
            if args[2] == "..":
                pointer = pointer.parent
            else:
                pointer = pointer.get_child(args[2])
        else:
            continue
    while pointer.parent:
        pointer = pointer.parent
    return pointer
    
    
def puzzle1(text):
    tree = build_tree(parse_input(text))    
    return sum(tree.little_children("/",{}).values())

def puzzle2(text):
    tree = build_tree(parse_input(text))
    free_space = 70000000- tree.calculate_size()
    need_space = 30000000-free_space
    big_children = tree.big_children(need_space,"/",{"/":tree.calculate_size()})
    return [val for _, val in nsmallest(1, big_children.items(), key = lambda ele: ele[1])][0]
    


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest="mode")
    
    run = subparser.add_parser('run')
    run.add_argument("--input",required=True,type=str)
    run.add_argument("--puzzle",required=True,type=int)
    
    
    args = parser.parse_args()
    if args.mode =='run':
        with open(args.input) as f:
            text = f.read().strip()
        if args.puzzle == 1:
            print (puzzle1(text))
            
        elif args.puzzle==2:
            print (puzzle2(text))
    else:
        unittest.main()

    
