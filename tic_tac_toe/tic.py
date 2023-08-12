
def check_win(player):
    won = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 7], [2, 5, 8], [3, 6, 9], [1, 5, 9], [3, 5, 7]]
    for f in won:
        if all(i in player for i in f):
            return [i - 1 for i in f]
    return None
# Check win
def check_wuin(player):
    
    # Checking for win
    if (('1' in player) and ('2' in player)) and ('3' in player):
        return 1
    elif ('4' in player) and ('5' in player) and ('6' in player):
        return 1
    elif ('7' in player) and ('8' in player) and ('9' in player):
        return 1
    elif ('1' in player) and ('4' in player) and ('7' in player):
        return 1
    elif ('2' in player) and ('5' in player) and ('8' in player):
        return 1
    elif ('3' in player) and ('6' in player) and ('9' in player):
        return 1
    elif ('1' in player) and ('5' in player) and ('9' in player):
        return 1
    elif ('3' in player) and ('5' in player) and ('7' in player):
        return 1

     # Checking if all spaces are occupied
    elif len(player) == 5:
        return 0

     # return -1 if their is no win
    else:
        return -1


# Check win
def Check_win(inputs):
    
    # Checking for win
    if inputs[0] == inputs[1] == inputs[2] and inputs[0] != '':
        return 1
    elif inputs[3] == inputs[4] == inputs[5] and inputs[3] != '':
        return 1
    elif inputs[6] == inputs[7] == inputs[8] and inputs[6] != '':
        return 1
    elif inputs[0] == inputs[3] == inputs[6] and inputs[0] != '':
        return 1
    elif inputs[1] == inputs[4] == inputs[7] and inputs[1] != '':
        return 1
    elif inputs[2] == inputs[5] == inputs[8] and inputs[2] != '':
        return 1
    elif inputs[0] == inputs[4] == inputs[8] and inputs[0] != '':
        return 1
    elif inputs[2] == inputs[4] == inputs[6] and inputs[2] != '':
        return 1

     # Checking if all spaces are occupied
    else:
        for c in inputs:
            if c == '':
                # return -1 if their is no win
                return -1

        return 0

def win(inputs, index, player):
    row_index = int(index) // 3
    row = inputs[row_index * 3: (row_index+1)*3]
    if all(s == player for s in row):
        return True
    col_ind = int(index) % 3
    col = [inputs[col_ind+i*3] for i in range(3)]
    if all(s == player for s in col):
            return True