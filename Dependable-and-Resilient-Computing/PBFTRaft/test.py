import sys

class Node(object):
    def __init__(self,data=None,next=None):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def append_at_end(self,data):
        node = Node(data)
        if self.head==None:
            self.head=node
            self.tail=node
        else:
            self.tail.next=node
            self.tail = node

    def search(self,d):
        temp= self.head

        while temp!=None:
            if (temp.data==d):
                return temp
            temp = temp.next

        return None

    def delete(self,n):
        temp = self.head
        while temp.next!=n:
            temp=temp.next

        temp.next=n.next
        n.next=None

    def printout(self):
        temp = self.head
        while temp!=None:
            print(temp.data)
            temp=temp.next

l = LinkedList()

l.append_at_end(1)
l.append_at_end(2)
l.append_at_end(3)
l.append_at_end(4)
l.append_at_end(5)

#l.printout()

#l.delete(l.search(3))

#l.printout()

l.tail.next = l.search(3)

#print("*****")
#l.printout()

temp_slow = l.head
temp_fast = l.head

while temp_slow!=None:
    temp_slow = temp_slow.next
    temp_fast = temp_fast.next.next
    if temp_slow==temp_fast:
        print("There is a loop")
        print(temp_fast.data)
        break




'''map = {}

temp = l.head
while temp!=None:
    if temp in map.keys():
        print("There is a loop")
        break
    map[temp]=1
    temp = temp.next'''


'''def palindromeIndex(s):
    # Complete this function
    if s == s[::-1]:
        #print("1")
        return -1

    for i in range (0,len(s)-1):
        temp = s[:i] + s[i+1:]
        if temp == temp[::-1]:
            #print("2")
            return i

    temp = s[:len(s)-1]
    if temp == temp[::-1]:
        #print("3")
        return len(s)-1


#print(palindromeIndex("aaba"))

q = int(input().strip())
for a0 in range(q):
    s = input().strip()
    result = palindromeIndex(s)
    print(result)'''