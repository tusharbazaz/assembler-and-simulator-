import sys
#Simple Assembler made by only 'Nabh Rajput' supported and helped by other group members.
#Special thanks to "Anuj" and "Yash" bhaiya , they helped me much in clearing doubts

def ieeetodeci(a): #accepts IEEE
    a = str(a)
    b = a[0:3] #expo
    c = a[3:] #mantissa
    final = "1"+c
    b = int(b,2) 
    
    inn = final[0:b+1]
    deci = final[b+1:]
    sum1 = 0
    inn = int(inn,2)

    for i in range(0,len(deci)):
        sum1 += (int(deci[i]))*(2**((-1)*(i+1)))

    final1 = float(inn)+float(sum1)
    return(final1)

def floatdecitobin(a): #takes in floating point
    try:
        b = int(a)  #before '.'
        c = a-b     #after '.'
        binb = int(str(bin(b)).replace("0b",""))
        af = ""
        #d = str(c)[2:] #decimal
        d = str(c)
        count = 0
        while((int(d[2:]) != 0) and (count<5)):
            e = str(2*float(d))
            if(e[0]=='0'):
                af += '0'
            else:
                af+='1'

            d = str(float(d)*2)

            for i in range(len(d)):
                if(d[i]=="."):
                    break

            d = '0'+d[i:]
            count += 1

        binb = str(binb)
        af = str(af)

        expo = len(binb) - 1
        mantissa = binb[1:] + af

        binexpo = str(bin(expo)).replace("0b","")

        while((len(mantissa))<5):
            mantissa = mantissa + '0'

        if(len(mantissa)>=6):
            mantissa = mantissa[:5]

        while(len(binexpo)<3):
            binexpo = '0' + binexpo
        
        '''print(f"integer part = {binb}")
        print(f"decimal part = {af}")
        print(f"exponent = {binexpo}")
        print(f"mantissa = {mantissa}")'''
        
        #print(f"Final Representation = {binexpo + mantissa}")

        return(binexpo+mantissa)

    except ValueError:
        return("Error : Too Pricise value")

def bitchange(no,size):
    while(len(no)!=size):
        no = '0'+no
    return(no)     

memadd = 0
memdict ={}
variables = {}
labels = {}

instruction = {"add":"10000",
"sub":"10001",
"mov":"10010",
"ld":"10100",
"st":"10101",
"mul":"10110",
"div":"10111",
"rs":"11000",
"ls":"11001",
"xor":"11010",
"or":"11011",
"and":"11100",
"not":"11101",
"cmp":"11110",
"jmp":"11111",
"jlt":"01100",
"jgt":"01101",
"je":"01111",
"hlt":"01010",
"movf":"00010",
"addf":"00000",
"subf":"00001"}

A = ["add","sub","mul","xor","or","and","addf","subf"]
B = ["mov","rs","ls"]
C = ["mov","div","not","cmp","movf"]
D = ["ld","st"]
E = ["jmp","jlt","jgt","je"]
F = ["hlt"]

register ={"R0":"000",
    "R1":"001",
    "R2":"010",
    "R3":"011",
    "R4":"100",
    "R5":"101",
    "R6":"110",
    "FLAGS":"111",
    "r0":"000",
    "r1":"001",
    "r2":"010",
    "r3":"011",
    "r4":"100",
    "r5":"101",
    "r6":"110", 
}
cons_label = 0 
each_line_list = []
allline=[]
for line in sys.stdin:
    allline.append(line)

for i in range(0,len(allline)):
    oneline = allline[i]
    oneline = oneline.split()
    each_line_list.append(oneline)


halt_finder = 0
for p in range(len(each_line_list)):
    if(each_line_list[p] == []):
        pass
    elif(each_line_list[p][0]=="hlt"):
        halt_finder = 1

var_at_start = 0
k = 0
while(True):
    try:
        if(each_line_list[k]==[]): #for empty lines
            each_line_list.pop(k)
        elif(each_line_list[k+1]==[]):
            each_line_list.pop(k+1)
        elif((each_line_list[k][0]=="Var" or each_line_list[k][0]=="var") and (each_line_list[k+1][0]=="Var" or each_line_list[k+1][0]=="var")):
            var_at_start+=1
            k +=1
        else:
            break
    except IndexError:
        break
ins_counter = 0
var_counter = 0
for n in range(0,len(each_line_list)):
    ins1 = each_line_list[n]
    if(ins1 == []):
        pass
    elif(ins1[0]=="Var" or ins1[0]=="var"):
        pass
    elif(ins1[0][-1]==":"):
        if(len(ins1)>1):
            if(ins1[1] in instruction):
                ins_counter+=1
    elif(ins1[0] in instruction):
        ins_counter+=1

if(var_at_start == 0):
    if((each_line_list[0][0]=="Var") or (each_line_list[0][0]=="var")):
        var_at_start+=1

elif(var_at_start!=0):
    var_at_start+=1
e = 0
outputcode = []
j = 0 

for i in range(0,len(each_line_list)):
    add = each_line_list[i]
    try:
        if(len(add)==1 and add[0][-1]==":"):
            print(f"SyntaxError in line {i+1}: Label '{add[0]}' can't be left empty.")
            e = 1
            break

        if(add[0] in labels):
            print(f"SyntaxError in line {i+1}: {add[0]} is defined again")
            e = 1
            break

        if(add[0][-1]==":"):
            labels[add[0]] = bitchange(str(bin(i-var_at_start)).replace("0b",""),8)
            memdict[add[0]] = bitchange(str(bin(i-var_at_start)).replace("0b",""),8)
    except IndexError:
        pass
        
'''for m in range(0,len(each_line_list)):
    print(each_line_list[m])'''

while((j<len(each_line_list)) and (e==0)):
    ins = each_line_list[j]
    #print(ins)
    try:
        if(ins == []): #ignore the empty line
            pass

        if((ins_counter+var_counter)>256):
            print(f"Out of Memory")
            e = 1
            break

        elif(len(ins)==4 and (ins[0][-1]!= ":") and ins[0] not in B and ins[0] not in C and ins[0] not in D and ins[0] not in E and ins[0] not in F): #type A instructions
            cons_label=0
            if(ins[0] not in instruction):
                print(f"Name Error in line {j+1} : instruction '{ins[0]}' is not defined ")
                e = 1
                break

            if(ins[1] not in register):
                print(f"Name Error in line {j+1}  : register '{ins[1]}' is not defined ")
                e = 1
                break

            if(ins[2] not in register):
                print(f"Name Error in line {j+1} : register '{ins[2]}' is not defined ")
                e = 1
                break

            if(ins[3] not in register):
                print(f"Name Error in line {j+1} : register '{ins[3]}' is not defined ")
                e = 1
                break

            if(ins[1] == "FLAGS" or ins[2] == "FLAGS" or ins[3] == "FLAGS"):
                print(f"Name Error in line {j+1} : 'FLAGS' register is used illegaly")
                e = 1
                break

            code = ""
            #try:
            a = instruction.get(ins[0])
            b = register.get(ins[1])
            c = register.get(ins[2])
            d = register.get(ins[3])
            memadd1 = str(memadd)
            memadd1 = str(str(bin(int(memadd1))).replace("0b",""))
            memadd1 = bitchange(memadd1,8) 
            try:
                if(labels.get(emptylabel)==""):
                    labels[emptylabel] =  bitchange(str(bin(memadd)).replace("0b",""),8)
                    memdict[emptylabel] = bitchange(str(bin(memadd)).replace("0b",""),8)
            except NameError:
                pass
            memadd += 1
            code = code+a+"00"+b+c+d
            outputcode.append(code)
            #print(code)

        elif(((ins[0] in A) and (len(ins)!=4)) or ((ins[0] in B) and (len(ins)!=3)) or ((ins[0] in C) and (len(ins)!=3)) or ((ins[0] in D) and (len(ins)!=3)) or ((ins[0] in E) and (len(ins)!=2)) or ((ins[0] in F) and (len(ins)!=1))):
            print(f"SyntaxError in line {j+1}: Number of arguments used in {ins[0]} are not appropriate.")
            e = 1
            break

        elif(((ins[0]=="Var") or (ins[0]=="var")) and (len(ins)!=2)):
            print(f"SyntaxError in line {j+1}: {ins[0]} is defined illegaly")
            e = 1
            break

        elif(len(ins)==3 and (ins[0][-1]!= ":") and (ins[0] != "Var") and(ins[0] != "var") and (ins[0] not in A) and (ins[0] not in E) and (ins[0] not in F)): #type B and C
            cons_label=0

            if(ins[0] not in instruction):
                print(f"Name Error in line {j+1}: instruction '{ins[0]}' is not defined ")
                e = 1
                break
            code = ""
            if(ins[0]=="mov"): #working with mov instruction
                if(ins[1] not in register):
                    print(f"Name Error in line {j+1}: register '{ins[1]}' is not defined ")
                    e = 1
                    break
                if(ins[2] == "FLAGS"):
                    print(f"SyntaxError in line {j+1}: Illegal use of 'FLAGS' register")
                    e = 1
                    break
                if(ins[2] in register): #type B instruction move register
                    memadd1 = str(memadd)
                    memadd1 = str(str(bin(int(memadd1))).replace("0b",""))
                    memadd1 = bitchange(memadd1,8)
                    memdict[ins[2]] = memadd1
                    a = "10011"
                    b = register.get(ins[1])
                    c = register.get(ins[2])
                    try:
                        if(labels.get(emptylabel)==""):
                            labels[emptylabel] =  bitchange(str(bin(memadd)).replace("0b",""),8)
                            memdict[emptylabel] = bitchange(str(bin(memadd)).replace("0b",""),8)
                    except NameError:
                        pass
                    memadd = memadd+1
                    code = code+a+"00000"+b+c
                    outputcode.append(code)
                    #print(code)
                    

                elif(ins[2][0] != "$"): #type C move immidiate
                    try:
                        if(type(int(ins[2]))==int):
                            print(f"SyntaxError in line {j+1}: Do you mean '${ins[2]}'")
                            e = 1
                            break
                    except ValueError:
                        print(f"Name Error in line {j+1}: register '{ins[2]}' is not defined ")
                        e = 1
                        break

                elif(ins[2][0] == "$"):
                    memadd1 = str(memadd)
                    memadd1 = str(str(bin(int(memadd1))).replace("0b",""))
                    memadd1 = bitchange(memadd1,8)
                    memdict[ins[2]] = memadd1
                    if(ins[1] not in register):
                        print(f"Name Error in line {j+1}: register '{ins[1]}' is not defined ")
                        e = 1
                        break
                    try:
                        if(int((ins[2][1::])) not in range(0,256)):
                            print(f"OutOfRangeError in line {j+1}: Immediate Value '{ins[2][1::]}' is not in range 0-255")
                            e = 1
                            break
                    except ValueError:
                        print(f"SyntaxError in line {j+1}: '{ins[2]}' is an invalid Immediate Value")
                        e = 1
                        break
                    
                    a = instruction.get(ins[0])
                    b = register.get(ins[1])
                    c = str(str(bin(int(ins[2][1::]))).replace("0b",""))
                    c = bitchange(c,8)
                    try:
                        if(labels.get(emptylabel)==""):
                            labels[emptylabel] =  bitchange(str(bin(memadd)).replace("0b",""),8)
                            memdict[emptylabel] = bitchange(str(bin(memadd)).replace("0b",""),8)
                    except NameError:
                        pass
                    memadd = memadd+1
                    code = code+a+b+c
                    outputcode.append(code)
                    #print(code)

            elif(ins[0]=="movf"): #working with mov instruction
                if(ins[1] not in register):
                    print(f"Name Error in line {j+1}: register '{ins[1]}' is not defined ")
                    e = 1
                    break
                if(ins[2] == "FLAGS"):
                    print(f"SyntaxError in line {j+1}: Illegal use of 'FLAGS' register")
                    e = 1
                    break
                elif(ins[2][0] != "$"): #type C move immidiate
                    try:
                        if(type(int(ins[2]))==int):
                            print(f"SyntaxError in line {j+1}: Do you mean '${ins[2]}'")
                            e = 1
                            break
                    except ValueError:
                        print(f"Name Error in line {j+1}: register '{ins[2]}' is not defined ")
                        e = 1
                        break

                elif(ins[2][0] == "$"):
                    memadd1 = str(memadd)
                    memadd1 = str(str(bin(int(memadd1))).replace("0b",""))
                    memadd1 = bitchange(memadd1,8)
                    memdict[ins[2]] = memadd1
                    if(ins[1] not in register):
                        print(f"Name Error in line {j+1}: register '{ins[1]}' is not defined ")
                        e = 1
                        break
                    try:
                        if(int(float(ins[2][1::])) not in range(0,16)):
                            print(f"OutOfRangeError in line {j+1}: Immediate Value '{ins[2][1::]}' is not in range 0-255")
                            e = 1
                            break
                    except ValueError:
                        print(f"SyntaxError in line {j+1}: '{ins[2]}' is an invalid Immediate Value")
                        e = 1
                        break
                    
                    a = instruction.get(ins[0])
                    b = register.get(ins[1])
                    c = floatdecitobin(float(ins[2][1::]))
                    try:
                        if(labels.get(emptylabel)==""):
                            labels[emptylabel] =  bitchange(str(bin(memadd)).replace("0b",""),8)
                            memdict[emptylabel] = bitchange(str(bin(memadd)).replace("0b",""),8)
                    except NameError:
                        pass
                    memadd = memadd+1
                    code = code+a+b+c
                    outputcode.append(code)
                    #print(code)


            elif((ins[0] in B) and (ins[0]!= "mov")): #type B left shift and right shift
                if(ins[1] == "FLAGS" or ins[2] == "FLAGS"):
                    print(f"Name Error in line {j+1} : 'FLAGS' register is used illegaly")
                    e = 1
                    break
                cons_label=0
                if(ins[1] not in register):
                    print(f"Name Error in line {j+1}: register '{ins[1]}' is not defined ")
                    e = 1
                    break

                memadd1 = str(memadd)
                memadd1 = str(str(bin(int(memadd1))).replace("0b",""))
                memadd1 = bitchange(memadd1,8)
                memdict[ins[2]] = memadd1
                a = instruction.get(ins[0])
                b = register.get(ins[1])
                c = str(str(bin(int(ins[2][1::]))).replace("0b",""))
                c = bitchange(c,8)
                code = code+a+b+c
                try:
                    if(labels.get(emptylabel)==""):
                        labels[emptylabel] =  bitchange(str(bin(memadd)).replace("0b",""),8)
                        memdict[emptylabel] = bitchange(str(bin(memadd)).replace("0b",""),8)
                except NameError:
                    pass
                memadd = memadd+1
                memadd += 1
                outputcode.append(code)
                #print(code)

            

            #type B complete


            elif(ins[0] in C): #rest of the type C
                if(ins[1] == "FLAGS" or ins[2] == "FLAGS"):
                    print(f"Name Error in line {j+1} : 'FLAGS' register is used illegaly")
                    e = 1
                    break

                if(ins[1] not in register):
                    print(f"Name Error in line {j+1}: register '{ins[1]}' is not defined ")
                    e = 1
                    break

                if(ins[2] not in register):
                    print(f"Name Error in line {j+1}: register '{ins[2]}' is not defined ")
                    e = 1
                    break
                cons_label=0 
                memadd1 = str(memadd)
                memadd1 = str(str(bin(int(memadd1))).replace("0b",""))
                memadd1 = bitchange(memadd1,8)
                memadd = memadd+1
                memdict[ins[2]] = memadd1
                a = instruction.get(ins[0])
                b = register.get(ins[1])
                c = register.get(ins[2])
                try:
                    if(labels.get(emptylabel)==""):
                        labels[emptylabel] =  memadd1
                        memdict[emptylabel] = memadd1
                except NameError:
                    pass

                memadd += 1
                code = code + a+"00000"+b+c
                outputcode.append(code)
                #print(code)

            #type C complete

            elif(ins[0] in D): #type D have load and store
                cons_label=0
                if(ins[1] == "FLAGS"):
                    print(f"Name Error in line {j+1} : 'FLAGS' register is used illegaly")
                    e = 1
                    break
                if(ins[1] not in register):
                    print(f"Name Error in line {j+1}: register '{ins[1]}' is not defined ")
                    e = 1
                    break
                if(ins[0]=="st"): #store command
                    a = instruction.get(ins[0])
                    b = register.get(ins[1])
                    c = ins[2] #memory address name
                    if((c in memdict) and (c not in labels)):
                        #variable name always already exist 
                        memadd1 = str(int(variables.get(ins[2]))+int(ins_counter))
                        memadd1 = str(str(bin(int(memadd1))).replace("0b",""))
                        memadd1 = bitchange(memadd1,8)
                        memdict[ins[2]] = memadd1  
                        

                    elif(ins[2] in labels):
                        print(f"TypeError in line {j+1}: Label '{ins[2]}' can't be used as a variable")
                        e=1
                        break

                    elif(ins[2] not in memdict):
                        print(f"Name Error in line {j+1}: Variable '{c}' not defined ")
                        e = 1
                        break

                    try:
                        if(labels.get(emptylabel)==""):
                            labels[emptylabel] =  bitchange(str(bin(memadd)).replace("0b",""),8)
                            memdict[emptylabel] = bitchange(str(bin(memadd)).replace("0b",""),8)
                    except NameError:
                        pass
                    memadd = memadd+1
                    code = code +a+b+memadd1
                    outputcode.append(code)
                    #print(code)

                elif(ins[0]=="ld"): #load command
                    if(ins[1] == "FLAGS"):
                        print(f"Name Error in line {j+1} : 'FLAGS' register is used illegaly")
                        e = 1
                        break
                    if(ins[2] in memdict):
                        a = instruction.get(ins[0])
                        b = register.get(ins[1])
                        memadd1 = str(int(variables.get(ins[2]))+ins_counter)
                        memadd1 = str(str(bin(int(memadd1))).replace("0b",""))
                        memadd1 = bitchange(memadd1,8)
                    elif(ins[2] in labels):
                        print(f"TypeError in line {j+1}: Label '{ins[2]}' can't be used as a variable")
                        e=1
                        break

                    elif(ins[2] not in memdict):
                        print(f"Name Error in line {j+1}: Variable '{ins[2]}' is not defined")
                        e = 1
                        break

                    try:
                        if(labels.get(emptylabel)==""):
                            labels[emptylabel] =  bitchange(str(bin(memadd)).replace("0b",""),8)
                            memdict[emptylabel] = bitchange(str(bin(memadd)).replace("0b",""),8)
                    except NameError:
                        pass
                    memadd+=1
                    code = code+a+b+memadd1
                    outputcode.append(code)
                    #print(code)

        elif(len(ins)==2 and (ins[0][-1]!= ":") and ins[0]!= "Var" and ins[0]!= "var"): #type E command
            cons_label=0
            code =""
            if(ins[0] not in instruction):
                print(f"Name Error in line {j+1}: instruction '{ins[0]}' is not defined ")
                e = 1
                break
            if(ins[1]+":" in memdict):
                a = instruction.get(ins[0])
                memadd1 = memdict.get(ins[1]+":")

            if(ins[1] in memdict):
               print(f"SyntaxError in line{j+1}: do you mean '{ins[1][:-1]}' instead of '{ins[1]}'")
               e = 1
               break

            if(ins[1]+":" not in memdict):
                print(f"Name Error in line {j+1}: label '{ins[1]}' is not defined")
                e = 1
                break

            if(ins[1] in variables):
                print(f"TypeError in line {j+1}: Variable '{ins[1]}' can't be use as a label")
                e=1
                break
            memadd += 1 #for instructions
            code = code+a+"000"+memadd1
            outputcode.append(code)
            #print(code)


        elif(ins[0][-1]==":"): #label defination
            if(ins[0][:-1] in register):
                print(f"SyntaxError in line {j+1}: '{ins[0][:-1]}' is a register name can't be used as a label name")
                e = 1
                break
            if(cons_label==1):
                print(f"Error in line {j+1}: two labels cannot be defined consequtively")
                e = 1
                break

            if(ins[0][:-1] in variables):
                print(f"TypeError in line {j+1}: '{ins[0]}' is a variable can't be used as a label")
                e = 1
                break
            if(len(ins)==1):
                print(f"SyntaxError in line {j+1}: Label '{ins[0]}' can't be left empty.")
                e = 1
                break

            else:
                cons_label=1
                if(ins[1][-1]==":"):
                    print(f"SyntaxError in line {j+1}: You cannot use double labels in a single instruction")
                    e = 1
                    break
                else:
                    ins.pop(0)
                    j-=1
            
        elif((ins[0]=="Var") or (ins[0]=="var")): #variable defination                                       
            cons_label=0
            if(len(ins)!=2):
                print(f"syntax Error in line {j+1}: Invalid arguments")
                e = 1
                break
            memdict[ins[1]] = str(var_counter)
            if(ins[1] in variables):
                print(f"SyntaxError in line {j+1}: '{ins[1]}' is defined again")
                e = 1
                break

            variables[ins[1]] = str(var_counter)
            var_counter+=1
            if(len(variables)>var_at_start):
                print(f"Syntax Error in line {j+1}: '{ins[1]}' should be defined at the top")
                e = 1
                break


        elif(len(ins)==1):
            cons_label=0
            if(ins[0] not in instruction):
                print(f"Name Error in line {j+1}: instruction '{ins[0]}' is not defined ")
                e = 1
                break
            code = ""
            if(ins[0]=='hlt'):
                halt_finder=1
            a = instruction.get(ins[0])
            try:
                if(labels.get(emptylabel)==""):
                    labels[emptylabel] =  bitchange(str(bin(memadd)).replace("0b",""),8)
                    memdict[emptylabel] = bitchange(str(bin(memadd)).replace("0b",""),8)
            except NameError:
                pass
            memadd = memadd+1
            code+= a+"00000000000"
            outputcode.append(code)
            #print(code)
            break

        elif(ins[1] == ":"):
            print(f"SyntaxError in line {j+1}: label defination is incorrrect ")
            e = 1
            break

        else:
            print(f"General Syntax Error in line {j+1}")
            e = 1
            break
        j+=1
    except IndexError:
        j+=1

#print(ins_counter)
#print(variables)
#print(labels)
#print(memdict)

#loop ends now check that if any statement is used after the 'hlt' statement if yes give error
if(e==0):
    try:
        if(len(each_line_list) > j+1):
            print(f"SyntaxError : '{each_line_list[j+1][0]}' instruction is used after hlt statement")
            e = 1

        if(halt_finder==0):
            print(f"SyntaxError : hlt statement not found")
            e = 1
    except IndexError:
        pass

#all code appended to our list just write it in the stdout.txt and read the same to get the output
#check if any error has occured or not , if not give output otherwise give the first error occured
if(e!=1):
    #we have to clear the already written data from the existing file to add new one
    for i in range(0,len(outputcode)):
        sys.stdout.write(outputcode[i]+"\n")


#khatam