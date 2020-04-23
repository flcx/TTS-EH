import re

if __name__ == '__main__':
    monsters = {}
    epic_monsters = {}

    # load monsters from csv
    with open("monsters.csv", "r") as monster_file :
        line = monster_file.readline()

        while(line) :
            data=line.split(';')
            name = data[0]
            mtype = data[1].lower()
            count = int(data[2])
            exp = data[3].strip()

            if mtype == "epic" :
                if not name in epic_monsters.keys() :
                    epic_monsters[name] = { }
                
                epic_monsters[name][exp]= count
                
            else :
                if not name in monsters.keys() :
                    monsters[name] = { }
                
                monsters[name][exp]= count

            line = monster_file.readline()

    """
    c = 0
    for m in monsters :
        print(m + ':' , end='')
        for e in monsters[m] :
            print(e + '/' + str(monsters[m][e]), end=' ')
        print("")
        c+=1

    print(c)
    """

    exp = None
    monster_pred = re.compile(r'"Nickname": "(?P<monster>[^"]+)"')
    gm_pred = re.compile('"GMNotes": ""')
    gmnotes_format = '"GMNotes": "{}"'

    monster_set = epic_monsters

    not_found = []
    with open("monsters.json", "r") as save_file:
        with open("monsters.out.json", "w") as out_file:
            line = save_file.readline()

            while line :
                line_out = line

                if exp :
                    if gm_pred.search(line) :
                        repl = gmnotes_format.format(exp)
                        line_out = gm_pred.sub(repl, line)
                        exp = None
                else :
                    match = monster_pred.search(line)
                    if match :
                        monster_name = match.group('monster')
                        if monster_name in monster_set :
                            m = monster_set[monster_name]
                            for e in m :
                                if m[e] > 0 :
                                    m[e] = m[e] - 1
                                    exp = e
                                    # print("Using {} for monster: {}".format(e, monster_name))
                                    break

                            if not exp :
                                print("Could not find expansion for {}".format(monster_name))
                                not_found.append(monster_name)
                        else :
                            print("Could not find the data for {}".format(monster_name))
                            not_found.append(monster_name)

                out_file.write(line_out)
                line = save_file.readline()
            out_file.flush()

    for m in monster_set :
        for e in monster_set[m] :
            if monster_set[m][e] > 0 :
                print('{} in {} left {}'.format(m, e, monster_set[m][e]))
        

    