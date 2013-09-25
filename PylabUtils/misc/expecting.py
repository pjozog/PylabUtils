import inspect, dis, sys

def expecting():
    """

    Return how many values the caller is expecting

    Examples
    --------

    def myFunc ():
        numArgs = plu.misc.expecting ()
        if numArgs == 1: 
            return 'hello'
        elif numArgs == 2: 
            return ('hello', 'world')
        else:
            print 'Hello world'

    a = myFunc ()
    (b,c) = myFunc ()
    print a                         # 'hello'
    print b                         # 'hello'
    print c                         # 'world'
    myFunc ()                       # 'Hello world'

    """

    f = sys._getframe().f_back.f_back
    i = f.f_lasti + 3
    bytecode = f.f_code.co_code
    instruction = ord(bytecode[i])
    while True:
        if instruction == dis.opmap['DUP_TOP']:
            if ord(bytecode[i + 1]) == dis.opmap['UNPACK_SEQUENCE']:
                return ord(bytecode[i + 2])
            i += 4
            instruction = ord(bytecode[i])
            continue
        if instruction == dis.opmap['STORE_NAME']:
            return 1
        if instruction == dis.opmap['UNPACK_SEQUENCE']:
            return ord(bytecode[i + 1])
        return 0
