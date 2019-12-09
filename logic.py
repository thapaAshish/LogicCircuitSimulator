class Connector :
    def __init__(self, owner , name , activates=0,monitor=0):
        self.value = None
        self.owner = owner
        self.name = name
        self.monitor = monitor
        self.connects = []
        self.activates =activates

    def connect(self,inputs):
        if type(inputs) != type([]):  #check the type of variable. If not array convert into one
            inputs = [inputs]
        for input in inputs:
            #print(self.owner.name, " pin ",self.name ," is connected to ",input.owner.name ," pin ",input.name,)
            self.connects.append(input)

    def set(self , value):

        if self.value == value: return
        self.value = value
        if self.activates : self.owner.evaluate()
        if self.monitor :
            print("connector {}-{} set to {} ".format(self.owner.name,self.name,self.value))
        for connection in self.connects:
            connection.set(value)
           # print("{}-{} set to {}".format(connection.owner.name,connection.name,connection.value))


class LC :
    def __init__(self,name):
        self.name = name

    def evaluate(self) : return


class Not(LC):
    def __init__(self,name):
        LC.__init__(self,name)
        self.A = Connector(self,'A',activates=1)  #input so it activates evaluation
        self.B = Connector(self,'B') #output

    def evaluate(self):
        if self.A.value == 1:
            self.B.set(0)
        else:
            self.B.set(1)

class Gate2(LC):
    def __init__(self,name):
        LC.__init__(self,name)
        self.A = Connector(self,'A',activates=1)
        self.B = Connector(self,'B',activates=1)
        self.C = Connector(self,'C')
    def evaluate(self):
        return

class And(Gate2):
    def __init__(self,name):
        Gate2.__init__(self,name)
    def evaluate(self):
        self.C.set(self.A.value and self.B.value)
class Or(Gate2):
    def __init__(self,name):
        Gate2.__init__(self,name)
    def evaluate(self):
        self.C.set(self.A.value or self.B.value)

class Xor(Gate2):
    def __init__(self,name):
        Gate2.__init__(self,name)
        self.n1 = Not('n1')
        self.n2 = Not('n2')
        self.a1 = And('a1')
        self.a2 = And('a2')
        self.o1 = Or('o1')
        self.A.connect([self.n1.A,self.a2.A])
        self.B.connect([self.n2.A,self.a1.A])
        self.n1.B.connect(self.a1.B)
        self.n2.B.connect(self.a2.B)
        self.a1.C.connect(self.o1.A)
        self.a2.C.connect(self.o1.B)
        self.o1.C.connect(self.C)
class halfAdder(LC):
    def __init__(self,name):
        LC.__init__(self,name)
        self.A = Connector(self,'A',1)
        self.B = Connector(self,'B',1)
        self.S = Connector(self,'S')
        self.C = Connector(self,'C')
        self.X1 = Xor("x1")
        self.A1 = And("A1")
        self.A.connect([self.X1.A,self.A1.A])
        self.B.connect([self.X1.B,self.A1.B])
        self.X1.C.connect([self.S])
        self.A1.C.connect([self.C])
class fullAdder(LC):
    def __init__(self,name):
        LC.__init__(self,name)
        self.A = Connector(self,'A',1)
        self.B = Connector(self,'B',1)
        self.S = Connector(self,'S')
        self.Cin = Connector(self,'Cin',1)
        self.Cout = Connector(self,'Cout',monitor=1)
        self.H1 = halfAdder("H1")
        self.H2 = halfAdder("H2")
        self.o1 = Or('o1')
        self.A.connect([self.H1.A])
        self.B.connect([self.H1.B])
        self.Cin.connect([self.H2.A])
        self.H1.S.connect([self.H2.B])
        self.H1.C.connect([self.o1.B])
        self.H2.S.connect(self.Cout)
        self.H2.C.connect([self.o1.A])
        self.o1.C.connect([self.S])
        


FA = fullAdder('f1')
FA.S.monitor = 1

FA.A.set(1)
FA.B.set(1)
FA.Cin.set(1)



#tests for xor gates
#x1 = Xor('x1')
#x1.C.monitor = 1

#x1.A.set(1)
#x1.B.set(0)
#print(x1.a2.A.value)
#print(x1.n2.B.value)
#print(x1.a2.C.value)

#h1 = halfAdder("H1")
#h1.S.monitor = 1
#h1.C.monitor = 1
#h1.A.set(1)
#h1.B.set(1)




        

