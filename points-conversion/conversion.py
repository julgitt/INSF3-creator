def dane():
    file = open("input.txt")
    out = open("output.txt",'w',encoding = 'utf-8')
    text = file.read()

    word = ''

    for line in text:
        if line in " (){}": continue
        elif line == ',':
            word += ' '
            continue
        word += line
    out.write(word + "\n")
    file.close()
    out.close()
    
dane()
