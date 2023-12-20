# convert assembly instructions into bytecode 

from bytecode import Instr, Bytecode

bytecode = Bytecode([Instr('LOAD_CONST', 1),
                     Instr('LOAD_CONST', 2),
                     Instr('BINARY_ADD'),
                     Instr('PRINT_EXPR'),
                     
                     Instr('LOAD_CONST', None),
                     Instr('RETURN_VALUE')])
code = bytecode.to_code()

# directly execute bytecode

exec(code)

# export bytecode to a executable pyc file 

import importlib

pyc_data = importlib._bootstrap_external._code_to_timestamp_pyc(code)
pyc = open('expression.pyc', 'wb')
pyc.write(pyc_data)
pyc.close()
