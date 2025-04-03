def convering_binary(a, b):
    if a<0:
        a=(1 << b)+a
    return format(a, '0{}b'.format(b))

def decimal_to_binary_converter(binary):
    if binary.startswith('1'):
        inverted_bits = ''.join('0' if bit== '1' else '1' for bit in binary)
        decimal = - (int(inverted_bits, 2) +1)
    else:
        decimal = int(binary, 2)
    
    return decimal
    

def binary_to_decimal(binary_str):
    decimal=0

    power=0
    for digit in reversed(binary_str):
        decimal+= int(digit) * (2 ** power)
        power+=1


    return decimal

def extending_sign_function(binary_num, num_bits):    
    if binary_num[0]== '1':
        extended_num= '1' * (num_bits-len(binary_num))+ binary_num
    else:
        extended_num= '0' * (num_bits-len(binary_num)) + binary_num

    return extended_num

def add_instruction(a,b):
    temp1= decimal_to_binary_converter(a) 
    temp2= decimal_to_binary_converter(b) 
    
    ans=temp1+temp2
    ans_str=convering_binary(ans,32)
    
    return ans_str  

def subtract_instruction(a,b):
    temp1=decimal_to_binary_converter(a)  
    temp2=decimal_to_binary_converter(b)  
    
    ans=temp1-temp2
    ans_str=convering_binary(ans,32)
    
    return ans_str

def left_shift_instruction(a,b):
    temp1=decimal_to_binary_converter(a)  
    temp2=decimal_to_binary_converter(b)  
    
    ans0=convering_binary(0,32)
    ans1=convering_binary(1,32)
    
    if(temp2>temp1):
        return ans1
    else:
        return ans0

def right_shift_instruction(a,b):
    temp_a= int (a,2)
    temp =b[-5:]
    
    num= binary_to_decimal(temp)
    ans= temp_a>>num
   
    return format(ans, '032b')

def or_operation(a,b):
    temp1=int(a,2)  
    temp2=int(b,2)  
    
    ans= temp1|temp2
    final_ans =convering_binary(ans,32)
    
    return final_ans 

def and_operation(a,b):
    temp1= int(a,2) 
    temp2=int(b,2)  
    
    ans= temp1&temp2
    final_ans =convering_binary(ans,32)
    
    return final_ans 

def instruction_type_R(data):
    global program_counter
    
    oprogram_counterode= data[-7:]
    rd= data[20:25]
    funct3= data[17:20]
    rs1= data[12:17]
    rs2= data[7:12]
    funct7= data[0:7]

    if (funct3=='000' and funct7=='0000000'): 
        register_access[rd] = "0b"+add_instruction(register_access[rs1][2:],register_access[rs2][2:])
    elif(funct3=='000' and funct7 == '0100000'): 
        register_access[rd]= "0b" + subtract_instruction(register_access[rs1][2:],register_access[rs2][2:])
    elif(funct3=='101'):
        register_access[rd]="0b" +right_shift_instruction(register_access[rs1][2:],register_access[rs2][2:])
    elif(funct3=='010'): 
        register_access[rd]="0b" +left_shift_instruction(register_access[rs1][2:],register_access[rs2][2:])
    elif(funct3=='110'): 
        register_access[rd]="0b"+or_operation(register_access[rs1][2:],register_access[rs2][2:])
    elif(funct3=='111'): 
        register_access[rd]="0b"+and_operation(register_access[rs1][2:],register_access[rs2][2:])
    
    program_counter = add_instruction(program_counter,convering_binary(4,32))

def instruction_type_I(data):
    global program_counter

    oprogram_counterode= data[-7::]
    rd= data[-12:-7]
    funct3 = data[-15:-12]
    rs1= data[-20:-15]
    imm = data[-32:-20]

    if funct3=='010':
        temp=add_instruction(register_access[rs1][2:],extending_sign_function(imm,32))
    
        temp1=hex(int(temp,2))[2:].lstrip('0')
        temp1='0x' + temp1.zfill(10- 2)
        register_access[rd]=memory_access[temp1]
        program_counter = add_instruction(program_counter,convering_binary(4,32))
    elif funct3 == '000' and oprogram_counterode=='0010011':
        register_access[rd]="0b"+add_instruction(register_access[rs1][2:],extending_sign_function(imm,32))
        program_counter= add_instruction(program_counter,convering_binary(4,32))
    else: 
        register_access[rd]="0b"+add_instruction(program_counter,convering_binary(4,32))
        register_access['00000'] = "0b00000000000000000000000000000000" 
        program_counter=add_instruction(register_access[rs1][2:],extending_sign_function(imm,32))
        program_counter=program_counter[:-1]+'0'


def instruction_type_S(data):
    global program_counter

    oprogram_counterode = data[-7::]
    imm1= data[-12:-7]
    funct3= data[-15:-12]
    rs1= data[-20:-15]
    rs2 =data[-25:-20]
    imm2= data[-32:-25]
    imm =imm2+imm1
    
    temp=add_instruction(register_access[rs1][2:],extending_sign_function(imm,32))
    temp1=hex(int(temp,2))[2:].lstrip('0')
    temp1='0x' + temp1.zfill(8)
    memory_access[temp1] = register_access[rs2]
    
    program_counter= add_instruction(program_counter,convering_binary(4,32))

def instruction_type_B(data):
    global program_counter
    
    oprogram_counterode= data[-7::]
    funct3 =data[17:20]
    rs1 =register_access[data[12:17]]
    rs2= register_access[data[7:12]]
    imm= data[0] + data[24] + data[1:7] +data[20:24]+"0"
    imm_decimal = decimal_to_binary_converter(extending_sign_function(imm, 32))
    
    if (rs1== "0b00000000000000000000000000000000") and (rs2== "0b00000000000000000000000000000000" and imm_decimal==0):
        return
    if imm_decimal==0:
        program_counter= add_instruction(program_counter, convering_binary(4, 32))
        return

    temp_program_counter= decimal_to_binary_converter(program_counter)//4
    temp_imm= decimal_to_binary_converter(extending_sign_function(imm,32))//4
    ans_program_counter= (temp_imm+temp_program_counter) * 4
    
    if(funct3=='000' and rs1==rs2):
        if rs1!= '0b' + '0' * 5: 
            program_counter =convering_binary(ans_program_counter, 32)
        return
    elif(funct3=='001' and rs1!=rs2):
        program_counter= convering_binary(ans_program_counter,32)
        return

    program_counter =add_instruction(program_counter,convering_binary(4,32))

def instruction_type_J(data):
    global program_counter

    oprogram_counterode = data[-7::]
    rd = data[-12:-7]
    temp_imm=data[0]+data[12:20]+data[11]+data[1:11]+"0"
    temp_program_counter = decimal_to_binary_converter(program_counter)//4
    temp_imm= decimal_to_binary_converter(extending_sign_function(temp_imm,32))//4
    register_access[rd]="0b"+add_instruction(program_counter,convering_binary(4,32))  

    ans_program_counter = (temp_imm+temp_program_counter) * 4
    program_counter =convering_binary(ans_program_counter,32)

    program_counter=program_counter[:-1]+'0'

def adding_normal_things(data):
    global program_counter

    print("error: ",data[0],)
    program_counter= add_instruction(program_counter,convering_binary(4,32))

    return

def changing_instruction_type(case_value,data):
    switch_dict = {'0110011': instruction_type_R,'0000011': instruction_type_I,'0010011': instruction_type_I,'1100111': instruction_type_I,'0100011': instruction_type_S,'1100011': instruction_type_B,'1101111': instruction_type_J,}
    switch_dict.get(case_value,adding_normal_things)(data)

import sys
input_file= sys.argv[1]  
output_file= sys.argv[2]  

program_counter='0'*32

memory_access={'0x00010000':'0b00000000000000000000000000000000','0x00010004':'0b00000000000000000000000000000000', '0x00010008':'0b00000000000000000000000000000000','0x0001000C':'0b00000000000000000000000000000000', '0x00010010':'0b00000000000000000000000000000000','0x00010014':'0b00000000000000000000000000000000', '0x00010018':'0b00000000000000000000000000000000','0x0001001C':'0b00000000000000000000000000000000', '0x00010020':'0b00000000000000000000000000000000','0x00010024':'0b00000000000000000000000000000000', '0x00010028':'0b00000000000000000000000000000000','0x0001002C':'0b00000000000000000000000000000000', '0x00010030':'0b00000000000000000000000000000000','0x00010034':'0b00000000000000000000000000000000', '0x00010038':'0b00000000000000000000000000000000','0x0001003C':'0b00000000000000000000000000000000', '0x00010040':'0b00000000000000000000000000000000','0x00010044':'0b00000000000000000000000000000000', '0x00010048':'0b00000000000000000000000000000000','0x0001004C':'0b00000000000000000000000000000000', '0x00010050':'0b00000000000000000000000000000000','0x00010054':'0b00000000000000000000000000000000', '0x00010058':'0b00000000000000000000000000000000','0x0001005C':'0b00000000000000000000000000000000', '0x00010060':'0b00000000000000000000000000000000','0x00010064':'0b00000000000000000000000000000000', '0x00010068':'0b00000000000000000000000000000000','0x0001006C':'0b00000000000000000000000000000000', '0x00010070':'0b00000000000000000000000000000000','0x00010074':'0b00000000000000000000000000000000', '0x00010078':'0b00000000000000000000000000000000','0x0001007C':'0b00000000000000000000000000000000'}

register_access ={'00000':'0b00000000000000000000000000000000', '00001':'0b00000000000000000000000000000000', '00010':'0b00000000000000000000000101111100', '00011':'0b00000000000000000000000000000000', '00100':'0b00000000000000000000000000000000', '00101':'0b00000000000000000000000000000000', '00110':'0b00000000000000000000000000000000', '00111':'0b00000000000000000000000000000000', '01000':'0b00000000000000000000000000000000', '01001':'0b00000000000000000000000000000000', '01010':'0b00000000000000000000000000000000', '01011':'0b00000000000000000000000000000000', '01100':'0b00000000000000000000000000000000', '01101':'0b00000000000000000000000000000000', '01110':'0b00000000000000000000000000000000', '01111':'0b00000000000000000000000000000000', '10000':'0b00000000000000000000000000000000', '10001':'0b00000000000000000000000000000000', '10010':'0b00000000000000000000000000000000', '10011':'0b00000000000000000000000000000000', '10100':'0b00000000000000000000000000000000', '10101':'0b00000000000000000000000000000000', '10110':'0b00000000000000000000000000000000', '10111':'0b00000000000000000000000000000000', '11000':'0b00000000000000000000000000000000', '11001':'0b00000000000000000000000000000000', '11010':'0b00000000000000000000000000000000', '11011':'0b00000000000000000000000000000000', '11100':'0b00000000000000000000000000000000', '11101':'0b00000000000000000000000000000000', '11110':'0b00000000000000000000000000000000', '11111':'0b00000000000000000000000000000000'}

with open(output_file, 'w') as f:
    f.write("")
with open(input_file,"+r") as input_file:
    lines = [line.rstrip('\n') for line in input_file.readlines()]
with open(output_file, 'a') as f:
    while(True):
        a=lines[decimal_to_binary_converter(program_counter)//4]
        changing_instruction_type(a[-7::],a)  
        register_access["00000"] = "0b"+"0"*32
        f.write("0b"+program_counter+" ")
        for key,value in register_access.items():
            f.write(value + " ")
        f.write('\n')
        if a == "00000000000000000000000001100011":
            break
    for key, value in memory_access.items():
        if key >= '0x00010000' and key <= '0x0001007C':
            f.write(key + ":" + value + "\n")