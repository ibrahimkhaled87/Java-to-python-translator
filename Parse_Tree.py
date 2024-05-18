import nltk
from nltk.tree import Tree

###################################################### Translation #########################################################

def translate_code(java_code):
    tokens = java_code.split()
    if tokens[0] != "for" :
        raise Exception("Invalid Statement : Excepted for statement")
    loop_var=tokens[2]
    try:

        mainString1 =java_code.index("(")
        mainString2 = java_code.index(")")
    except:
        return Exception("Syntax error : missing brackets")
     
    new_token=java_code[mainString1+1:mainString2]
    new_token_split = new_token.split(";")
    tokens = java_code[mainString2+2:]
    parentthesis = java_code[mainString2+2]

    if parentthesis != "{":
        if tokens.count(";")>1 :
            raise Exception("Syntax error : missing parentthesis")
        
    


    # ----------------------------------------checking for the start--------------------------------------------#
    first= new_token_split[0].split()
    cond = new_token_split[1].split()
    step = new_token_split[2].split()

    #checking for the datatype
    if first[0] !="int" :
        raise Exception("Syntax error : check datatype")
    
    #checking of the validation for the variable name
    try:
        str(first[0][1])
        str(cond [2])
    except:
        raise Exception("SyntaxError : invalid variable name")
    if first[2] != "=" :
        raise Exception("SyntaxError : check operator")

    try:
        int(first[3])
        start =first[3]
    except:
        raise Exception("SyntaxError : invalid input :input must be an integer value")

    # ----------------------------------------checking for the condition--------------------------------------------#

    
    if(first[1] != cond[0]):
        raise Exception("SyntaxError : invalid variable")

    if cond[1] != "<" :
        raise Exception("SyntaxError : invalid operator")
    end=cond[2]

    # ----------------------------------------checking for the step--------------------------------------------#

    if first[1] != step[0]:
        if step[0] == first[1]+"++":
            steps=1
        elif step[0] == first[1]+"--":
            steps=-1
        else :
            raise Exception("SyntaxError : invalid step")  

    elif step[1] != "=":
        raise Exception("SyntaxError : invalid step")
    
    else:
        try:
            int(step[4])
            steps= step[4]
        except:
            raise Exception("SyntaxError : invalid variable name")
    
    python_loop=f"for {loop_var} in range ({start},{end},{steps}):"
    return python_loop



def convert_java_to_python(java_code):
    # Split the Java code by lines
    java_lines = java_code.split('\n')
    # Initialize an empty list to store the converted Python code
    python_code = []
    # Initialize a flag to track whether the while loop has started
    inside_while_loop = False
    inside_for_loop = False
    flag=0
    # Iterate through each line of the Java code
    for line in java_lines:
        # Check if the line starts with "while"
        if line.strip().startswith("while"): 
            # Set the flag indicating that the while loop has started
            inside_while_loop = True
            #indicate that last thing the code entered is while to know which flag we should turn off
            flag=1
            #get the index of opening parenthesis for while loop
            opening_parenthesis_index = line.find('(')
            #get the index of closing parenthesis for while loop
            closing_parenthesis_index = line.find(')')

            # Extract the condition from the Java while statement
            condition = line.strip()[opening_parenthesis_index + 1:closing_parenthesis_index]

            # Add the converted while statement to the Python code
            #check first if the while loop exist inside a for loop or not
            #case 1: while loop does exist inside a for loop
            if (inside_for_loop):
                python_code.append("    while " + condition + ":")
            #case 2: while loop doesn't exist inside a for loop
            else:
                python_code.append("while " + condition + ":")
            
            #check if the line starts with for
        if line.strip().startswith("for"): 
            # Set the flag indicating that the for loop has started
            inside_for_loop = True
            #indicate that last thing the code entered is for to know which flag we should turn off
            flag=2
            #get the translated statement
            converted_code =translate_code(line)
            #check first if the for loop exist inside a while loop or not
            #case 1: for loop does exist inside a while loop
            if (inside_while_loop):
                python_code.append("    " + converted_code)
            #case 2: while loop doesnot exist inside a for loop
            else:
                python_code.append(converted_code)
            
         # Check if the line contains an assignment statement and the while/for loop has not started yet
        elif "=" in line and not inside_while_loop and not inside_for_loop and not line.strip().startswith("while") and not line.strip().startswith("for"):
            # remove ; and replace , by ; incase of multiple declaration
            assignment_statement = line.strip().replace(";", "")
            assignment_statement = assignment_statement.strip().replace(",", "; ")
            # Split the assignment statement by spaces
            parts = assignment_statement.split()
            # Remove data type keywords
            assignment_statement = ' '.join(part for part in parts if part not in ["int", "char", "float", "double", "boolean"])
            # Add the modified assignment statement to the Python code
            python_code.append(assignment_statement)

        # If assign statement inside the while and for loop bodies
        elif "=" in line and inside_while_loop and inside_for_loop and not line.strip().startswith("while") and not line.strip().startswith("for"):
            # Remove data type declarations such as int, char, etc.
            assignment_statement = line.strip().replace(";", "")
            assignment_statement = assignment_statement.strip().replace(",", "; ")
            
            # Split the assignment statement by spaces
            parts = assignment_statement.split()
            # Remove data type keywords
            assignment_statement = ' '.join(part for part in parts if part not in ["int", "char", "float", "double", "boolean"])
            # Add the modified assignment statement to the Python code with indentation
            python_code.append("        " + assignment_statement)
            
         # If assign statement inside the while or for loop body
        elif "=" in line and (inside_while_loop or inside_for_loop) and not line.strip().startswith("while")and not line.strip().startswith("for"):
            # Remove data type declarations such as int, char, etc.
            assignment_statement = line.strip().replace(";", "")
            assignment_statement = assignment_statement.strip().replace(",", "; ")
            
            # Split the assignment statement by spaces
            parts = assignment_statement.split()
            # Remove data type keywords
            assignment_statement = ' '.join(part for part in parts if part not in ["int", "char", "float", "double", "boolean"])
            # Add the modified assignment statement to the Python code with indentation
            python_code.append("    " + assignment_statement)
            
        elif "++" in line or "--" in line:
            assignment_statement = line.strip().replace(";", "")
            if "++" in line:
                variable_name = assignment_statement[0:-3]
                assignment_statement = variable_name +"+=1"
            
            elif "--" in line:
                variable_name = assignment_statement[0:-3]
                assignment_statement = variable_name +"-=1"
            if  not inside_while_loop and not inside_for_loop and not line.strip().startswith("while") and not line.strip().startswith("for"):
                python_code.append(assignment_statement)
            elif inside_while_loop and inside_for_loop and not line.strip().startswith("while") and not line.strip().startswith("for"):
                python_code.append("        "+assignment_statement)
            elif  (inside_while_loop or inside_for_loop) and not line.strip().startswith("while")and not line.strip().startswith("for"):
                python_code.append("    "+assignment_statement)
            

            
        elif "}" in line:
            if inside_while_loop and not inside_for_loop:
                 inside_while_loop=False
            elif inside_for_loop and not inside_while_loop:
                 inside_for_loop=False
            else:
                #While is the last entered loop
                if flag==1:
                    inside_while_loop=False
                #For is the last entered loop
                elif flag==2:
                    inside_for_loop=False
    # Combine the converted Python code into a single string
    python_code = '\n'.join(python_code)

    return python_code





###################################################### Parser #########################################################


def add_spaces(sentence):
    """Adds spaces before and after symbols in a sentence.
    Args:
        sentence: The input sentence as a string.
    Returns:
        The modified sentence with spaces around symbols.
    """

    symbols = ["(", ")", ";", "==", "!=", "+=", "-=", "*=", "/=", ">=", "<=", "=", "+", "-", "*", "/", ">", "<"]
    result = sentence

    # Loop through symbols and replace them with spaced versions
    for symbol in symbols:
        result = result.replace(symbol, f" {symbol.strip()} ")

    # Remove extra spaces between consecutive equal signs
    result = result.replace("  =  =  ", " == ")
    result = result.replace("  !  =  ", " != ")
    result = result.replace("  +  =  ", " += ")
    result = result.replace("  -  =  ", " -= ")
    result = result.replace("  *  =  ", " *= ")
    result = result.replace("  /  =  ", " /= ")
    result = result.replace("  >  =  ", " >= ")
    result = result.replace("  <  =  ", " <= ")
    result = result.replace(" +  + ", "++")
    result = result.replace(" -  - ", "--")
    return result



#defining Contex Free Grammar
grammar = nltk.CFG.fromstring("""
    stmt -> for_stmt | assign_stmt | while_stmt |                
    for_stmt -> 'for' '(' var_type start ';' cond ';' step ')' '{' stmt '}' stmt       
    assign_stmt -> var_type id assign_op expr ';' stmt | step ';' stmt  
    while_stmt -> 'while' '(' cond ')' '{' stmt '}' stmt
    
    start -> id '=' expr
    cond -> id rel_op expr
    step -> '#INCR#' | id assign_op expr
                              
    expr -> expr '+' term | expr '-' term | term
    term -> term '*' factor | term '/' factor | factor
    factor -> id | num | '('expr')'

    assign_op -> '=' | '+=' | '-=' | '*=' | '/='                                                 
    var_type -> 'int' | 'double' | 'char' | 'float' | 'boolean' | 
    rel_op -> '<' | '>' | '<=' | '>=' | '==' | '!='                            
    id -> '#ID#'
    num -> '#NUM#'
  """)
# edits needed
# ((( convert original sentence to standard syntax (add spaces) )))



try:
    # Read input sentence from file
    file = open('input.txt','r')
    sentence = file.read()
    print("Original Sentence: \n", sentence, '\n')




    # Convert original code to standard form where symbols have spaces before and after them
    sentence = add_spaces(sentence)
    print("Modified Sentence: \n", sentence, '\n')
    sentence0 = sentence.split()




    # Make modifications on sentence to accomodate id++, any id, any num
    reserved_words = ['for', 'while', 'int', 'douoble', 'float', 'char', 'boolean']

    sentence2 = ['#NUM#' if i.isdigit() else i for i in sentence0]
    numbers = [i for i in sentence0 if i.isdigit()]
    sentence3 = ['#ID#' if (i.isidentifier() and i not in reserved_words) else i for i in sentence2]
    ids = [i for i in sentence2 if (i.isidentifier() and i not in reserved_words)]
    sentence4 = ['#INCR#' if (i[:-2].isidentifier() and i[:-2] not in reserved_words and (i[-2:] in ['++', '--'])) else i for i in sentence3]
    incrs = [i for i in sentence3 if (i[:-2].isidentifier() and i[:-2] not in reserved_words and (i[-2:] in ['++', '--'])) ]
    # print(sentence4, numbers, ids, incrs)




    # Start check CFG
    def parse(sent):
        #Returns nltk.Tree.Tree format output
        a = []  
        parser = nltk.ChartParser(grammar)
        for tree in parser.parse(sent):       
            a.append(tree)
        return(a[0])

    # tree with placeholders
    t=parse(sentence4)

    # convert back to original num, id, incr
    for leafPos in t.treepositions('leaves'):
        if t[leafPos] == "#NUM#":
            t[leafPos] = numbers.pop(0)
        if t[leafPos] == "#ID#":
            t[leafPos] = ids.pop(0)
        if t[leafPos] == "#INCR#":
            t[leafPos] = incrs.pop(0)
    #print(t)
    t.draw()


except:
    print("Syntax Error: Parser Failed.")


else:
    print("Java code: ")
    print(sentence)

    print("\n")
    print("Pyton code: ")
    python_code = convert_java_to_python(sentence)
    print(python_code)


