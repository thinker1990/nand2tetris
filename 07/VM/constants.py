# VM command taxonomy:
ARITHMETIC_CMD = ('add', 'sub', 'neg', 'and', 'or', 'not', 'eq', 'gt', 'lt')
MEMORY_ACCESS_CMD = ('push', 'pop')

# Common assembly segments:
PUSH = '''@SP
          A=M
          M=D
          @SP
          M=M+1'''
POP = '''@SP
         M=M-1
         @SP
         A=M'''
