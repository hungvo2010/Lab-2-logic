# PROJECT 02 - LOGIC
# HO VA TEN: VO CHANH HUNG
# MSSV: 19120523

import os

def read_file(file_path):
    file = open(file_path, 'r')

    # read first line then alpha
    alpha = file.readline()
    # read number of clauses in KB
    number_clauses = int(file.readline())

    KB = set({})
    for i in range(number_clauses):
        # read one clause
        clause = file.readline()
        # add standardized clause to KB
        KB.add(standardize(clause))

    file.close()
    return KB, standardize(alpha)

def standardize(clause):
    # A OR B => ('A', 'B')
    return tuple((x.strip() for x in clause.split('OR')))

def PL_RESOLUTION(KB, alpha, output_path):
    clauses = set({})
    num = 0 # order of loop

    clauses.update(KB)
    # add negative of literal in A to clauses
    for i in alpha:
        clauses.add((negative(i),))
    
    while True:
        num += 1
        new = set({}) # set of new clauses after one loop
        list_clauses = list(clauses)
        for i in range(len(clauses)):
            for j in range(i + 1, len(clauses)):
                    x = list_clauses[i]
                    y = list_clauses[j]
                    clause = PL_RESOLVE(x, y)
                    # clause[0] = 0 => create TRUE clause
                    # clause[0] = 1 => do not create new clause
                    # clause[0] = 2 => create empty clause
                    # clause[0] = 3 => create new clause
                    if clause[0] > 1:
                        if clause[1] not in clauses:
                            new.add(clause[1])
        # do not create new clause      
        if len(new) == 0: 
            write_file(output_path, '0\nNO', 'a')
            return False

        # first loop then write file mode is W, otherwise A
        mode = 'a'
        if num > 1:
            mode = 'a'
        else:
            mode = 'w'

        # write file and see if any empty clause created
        empty_clause = write_file(output_path, new, mode)
        # if no empty clause found, add new clause to clauses
        if not empty_clause:
            clauses.update(new)
        else:
        # otherwise, return True
            return True
            
def write_file(file_path, clauses, mode):
    file = open(file_path, mode)

    # if typeof clauses is STRING <=> YES/NO
    if isinstance(clauses, str):
        file.write(clauses)
        file.close()
        return
    
    print_buffer = []
    print_buffer.append(str(len(clauses)) + '\n')
    
    # empty clause is found
    flag = False
    for clause in clauses:
        # empty clause is found
        if len(clause) == 0:
            flag = True
            print_buffer.append(r'{}' + '\n')
            continue
        print_buffer.append(' OR '.join(clause) + '\n')
    
    if flag:
        print_buffer.append('YES')
    file.writelines(print_buffer)
    file.close()

    return flag

def sort_literal_key(literal):
    return literal[-1]

def PL_RESOLVE(clause1, clause2):
    duality_count = 0
    idx1 = 0
    idx2 = 0

    for i in range(len(clause1)):
        for j in range(len(clause2)):
            if clause1[i] == negative(clause2[j]):
                idx1 = i
                idx2 = j
                duality_count += 1
                if duality_count > 1:
                    # create TRUE clause
                    return [0, None]
                break
    if duality_count == 0:
        # do not create new clause
        return [1, None]
    if duality_count == 1 and len(clause2) == 1 and len(clause1) == 1:
        # create empty clause
        return [2, ()]

    set_literal = set({})
    for literal in clause1:
        if literal != clause1[idx1]:
            set_literal.add(literal)
    for literal in clause2:
        if literal != clause2[idx2]:
            set_literal.add(literal)
    
    list_literal = list(set_literal)
    list_literal.sort(key = sort_literal_key)
    # create new clause
    return [3, tuple(list_literal)]
    
def negative(literal):
    if literal[0] == '-':
        return literal[1:]
    return '-' + literal
    
def read_write_folder():
    # path to SRC folder
    dir_path = os.path.dirname(os.path.realpath(__file__))
    # path to /SRC/input folder
    input_folder = os.path.join(dir_path, "input")
    # path to /SRC/output folder
    output_folder = os.path.join(dir_path, "output")

    for file in os.listdir(input_folder):
        # path to input path
        input_path = os.path.join(input_folder, file)
        # path to output path, respectively
        output_path = os.path.join(output_folder, 'output' + input_path[-5] + '.txt')
        KB, alpha = read_file(input_path)
        PL_RESOLUTION(KB, alpha, output_path)

if __name__ == "__main__":
    read_write_folder()