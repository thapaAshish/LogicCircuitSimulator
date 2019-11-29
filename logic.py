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
        for input in inputs: self.connects.append(input)

    def set(self , value):
        if self.value == value: return
        self.value = value
        if self.activates : self.owner.evaluate()
        if self.monitor :
            print("connector {}-{} set to {} ".format(self.owner.name,self.name,self.value))
            for connection in self.connects:
                connection.set(value)


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
        self.B.set(not self.A.value)

class Gate2(LC):
    def __init__(self,name):
        LC.__init__(self,name)
        self.A = Connector(self,'A',activates=1)
        self.B = Connector(self,'B',activates=1)
        self.C = Connector(self,'C')

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
        self.x1 = Or('x1')
        self.a1 = And('A1')
        self.a2 = And('A2')
        self.n1 = Not('n1')
        self.n2 = Not('n2')
