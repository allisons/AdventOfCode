import argparse
import unittest
import numpy as np

class Test(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.testinput = """30373
25512
65332
33549
35390"""
        
    def test_parse_input(self):
        expected = np.array([[3,0,3,7,3],
                             [2,5,5,1,2],
                             [6,5,3,3,2],
                             [3,3,5,4,9],
                             [3,5,3,9,0]])
        actual = parse_input(self.testinput)
        self.assertEqual(actual[0,2],3)
        self.assertEqual(actual[2,0],6)
        self.assertTrue(np.all(expected==parse_input(self.testinput)))
                             
    def test_is_visible(self):
        arr = np.array([5,0])
        self.assertTrue(dirIsVisible(arr))
        
    def test_dir(self):
        arr = parse_input(self.testinput)
        self.assertTrue(np.all(np.array([5,5,0])==up(arr,2,1)),up(arr,2,1))
        self.assertTrue(np.all(np.array([5,3,5])==down(arr,2,1)),down(arr,2,1))
        self.assertTrue(np.all(np.array([5,6])==left(arr,2,1)),left(arr,2,1))
        self.assertTrue(np.all(np.array([5,3,3,2])==right(arr,2,1)),right(arr,2,1))
    
    def test_any_visible(self):
        arr = parse_input(self.testinput)
        self.assertTrue(any_visible(arr,1,1))
        self.assertTrue(any_visible(arr,1,2))
        self.assertFalse(any_visible(arr,1,3))
        self.assertTrue(any_visible(arr,2,1))
        self.assertFalse(any_visible(arr,2,2))
        self.assertTrue(any_visible(arr,2,3))        
    
    def test_puzzle1(self):
        self.assertEqual(21,puzzle1(self.testinput))

    def test_can_see_up(self):
        arr = parse_input(self.testinput)
        actual = viewBlocker(np.array([5,3]))
        expected = np.array([3])
        self.assertTrue(np.all(actual==expected))
        actual = viewBlocker(up(arr,1,2))
        self.assertTrue(np.all(actual==expected))
        
    def test_can_see_left(self):
        arr = parse_input(self.testinput)
        actual = viewBlocker(left(arr,1,2))
        expected = np.array([5])
        self.assertTrue(np.all(actual==expected),actual)

    def test_can_see_right(self):
        arr = parse_input(self.testinput)
        actual = viewBlocker(right(arr,1,2))
        expected = np.array([1,2])
        self.assertTrue(np.all(actual==expected),actual)

    def test_can_see_down(self):
        arr = parse_input(self.testinput)
        actual = viewBlocker(down(arr,1,2))
        expected = np.array([3,5])
        self.assertTrue(np.all(actual==expected),actual)

    def test_view_score(self):
        arr = parse_input(self.testinput)
        self.assertTrue(view_score(arr,1,3),4)
        
    def test_puzzle2(self):
        self.assertTrue(puzzle2(self.testinput),8)

    
def any_visible(arr,i,j):
    return any([dirIsVisible(direction(arr,i,j)) for direction in [up,down,left,right]])

def parse_input(text):
    return np.array([[int(v) for v in row] for row in text.split("\n")])

def dirIsVisible(arr):
    return np.all(arr[1:] < arr[0])

def up(arr,row,col):
    return arr[:row+1,col][::-1]

def down(arr,row,col):
    return arr[row:,col]

def left(arr,row,col):
    return arr[row,:col+1][::-1]

def right(arr,row,col):
    return arr[row,col:]

def viewBlocker(arr):
    me = arr[0]
    pointer = 1
    while(pointer<len(arr)):
        # print (f"Top of loop {pointer}, arr is {arr[1:pointer]}")
        if arr[pointer] >= me:
            return arr[1:pointer+1]
        pointer+=1
    return arr[1:]

def view_score(arr,i,j):
    return np.prod([len(viewBlocker(direction(arr,i,j))) for direction in [up,down,left,right]])
    

def puzzle1(text):
    arr = parse_input(text)
    h,w = arr.shape
    results = np.zeros_like(arr,dtype=bool)
    results[0,:] = True
    results[:,0] = True
    results[h-1,:]= True
    results[:,w-1] = True
    for i in range(1,h-1):
        for j in range(1,w-1):
            results[i,j] = any_visible(arr,i,j)
    return results.sum()
    
    

def puzzle2(text):
    arr = parse_input(text)
    h,w = arr.shape
    results = np.zeros_like(arr)
    for i in range(1,h-1):
        for j in range(1,w-1):
            results[i,j] = view_score(arr,i,j)
    return results.max()


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

    
