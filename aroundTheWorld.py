text=open("TaskList.txt","r")

task_list = []
counter=0

for i in text:
    counter+=1
    temp = i.split(",")
    if counter!=5:
        tempx = temp.pop(3)
        tempx = tempx[:-1]
        temp.append(tempx)

    task_list.append(temp)
print(task_list)

hero_hp=3000
pegasus_hp=550
hero_foot=20
pegasus_speed=50
hero_damage_perhour=10
pegasus_damage_perhour=15
total_time = 0

def Invalid_tasks(task_list,general_input):
    state=True
    task_names = []
    for i in range(len(task_list)):
        task_names.append(task_list[i][0].lower())

    while state:
        if general_input not in task_names:
            print("Invalid input")
            general_input=input("Where should Hero go next?").lower()

        else:
            state=False
    return general_input

def Invalid_way(way_main,way, travel_type):
    while way not in way_main:
        print("Invalid input")
        if travel_type == "travel":
            way = input("How do you want to travel?(Foot/Pegasus)").lower()
        elif travel_type == "home":
            way = input("How do you want to go home?(Foot/Pegasus)").lower()

    return way

def way_foot(element):
    temp = task_list[element][1]
    temp = (int)(temp)
    time = int(temp / hero_foot)
    hero_d = int(time * hero_damage_perhour)

    return hero_d,time

def way_pegasus(element):
    temp = (int)(task_list[element][2])
    time = int(temp / pegasus_speed)
    pegasus_d = int(time * pegasus_damage_perhour)
    return  pegasus_d, time

def no_foot_tasks(task, way,pegasus_hp,e,alive,travel_type):
    task = task.lower()

    while (task == "task1" or task == "task2") and way=="foot":
        print("You cannot go there by foot.")
        way = input("How do you want to travel?(Foot/Pegasus)")
        way = Invalid_way(way_main,way,travel_type)

    pegasus_d = (way_pegasus(e))[0]
    if (task == "task1" or task == "task2") and pegasus_hp < pegasus_d:
        alive = False

    return way,alive

def travel_damage(tasks,way,hero_hp,pegasus_hp,total_time,alive,travel_type): #travel
    task_rn=0
    for e in range(len(task_list)):
        temp_task = task_list[e][0]
        temp_task = temp_task.lower()
        if temp_task == tasks:
            state = no_foot_tasks(tasks, way, pegasus_hp, e,alive,travel_type)

            if state[1] == False:
                print("Game over.")
                alive = False
                break
            else:
                way = state[0]

            hp_to_kill = (int)(task_list[e][3])
            hero_d = way_foot(e)[0]
            pegasus_d = (way_pegasus(e))[0]

            while way=="foot" and (hero_d + hp_to_kill) > hero_hp and pegasus_d < pegasus_hp:
                print("You cannot go there by foot.")
                way = input("How do you want to travel?(Foot/Pegasus)").lower()
                if way == "pegasus":
                    break

            while way == "pegasus" and pegasus_hp < pegasus_d and (hero_d + hp_to_kill) < hero_hp:
                print("Pegasus does not have enough HP.")
                way = input("How do you want to travel?(Foot/Pegasus)").lower()
                if way == "foot":
                    break

            if way=="foot":
                if (hero_d+hp_to_kill)>hero_hp and pegasus_d>pegasus_hp:
                    print("Game over.")
                    alive = False
                    break
                else:
                    total_time+=way_foot(e)[1]
                    hero_hp = hero_hp - hero_d - hp_to_kill
                    print("Hero defeated the monster.")
                    print("Time passed :", total_time, "hour")

            elif way == "pegasus":
                if (hero_d+hp_to_kill)>hero_hp and pegasus_d>pegasus_hp:
                    print("Game over.")
                    alive = False
                    break
                else:
                    total_time+=way_pegasus(e)[1]
                    hero_hp-=hp_to_kill
                    pegasus_hp-=pegasus_d
                    print("Hero defeated the monster.")
                    print("Time passed :", total_time, "hour")
            task_rn = e
            continue
    if alive == True:
        print("\nRemaining HP for Hero : ", hero_hp)
        print("Remaining HP for Pegasus:", pegasus_hp, "\n")

    return hero_hp, pegasus_hp, task_rn,total_time,alive

def home_damage(task_rn,way,hero_hp,pegasus_hp,alive,total_time,travel_type): #go to home
    e = task_rn
    state = no_foot_tasks(task_list[task_rn][0], way, pegasus_hp, e, alive, travel_type)
    if state[1] == False:
        print("Game over.")
        alive = False
        return hero_hp, pegasus_hp, alive, total_time

    else:
        way = state[0]

        hero_d = way_foot(e)[0]
        pegasus_d = way_pegasus(e)[0]

        while way == "foot" and hero_d > hero_hp and pegasus_d < pegasus_hp:
            print("You cannot go there by foot.")
            way = input("How do you want to go home?(Foot/Pegasus)").lower()
            if way == "pegasus":
                break

        while way == "pegasus" and pegasus_hp < pegasus_d and hero_d < hero_hp:
            print("Pegasus does not have enough HP.")
            way = input("How do you want to go home?(Foot/Pegasus)").lower()
            if way == "foot":
                break

        if way == "foot":
            if hero_d > hero_hp and pegasus_d > pegasus_hp:
                print("Game over.")
                alive = False


            else:
                total_time += way_foot(e)[1]
                hero_hp = hero_hp - hero_d
                print("Hero arrived home.")
                print("Time passed :", total_time, "hour")

        elif way == "pegasus":
            if hero_d > hero_hp and pegasus_d > pegasus_hp:
                print("Game over.")
                alive = False

            else:
                total_time += way_pegasus(e)[1]
                pegasus_hp -= pegasus_d
                print("Hero arrived home.")
                print("Time passed :", total_time, "hour")

        if alive == True:
            print("\nRemaining HP for Hero : ", hero_hp)
            print("Remaining HP for Pegasus:", pegasus_hp, "\n")

        return hero_hp, pegasus_hp, alive, total_time

def remove_task(task_list, finished_task,x):
    temporary = task_list[x]
    task_temp = temporary[0].lower()
    if task_temp == finished_task.lower():
        task_list.remove(temporary)
    else:
        remove_task(task_list,finished_task,x+1)
    return task_list

def print_remaining_tasks(task_list,x):
    temporary = task_list[x]

    if x==0 and len(task_list)!=0:
        print("Here are the tasks left that hero needs to complete:")
        print("---------------------------------------------------------------------")
        print("|\tTaskName\t|\tByFootDistance\t|\tByPegasus\t|\tHPNeeded\t|")
        print("---------------------------------------------------------------------")
        if len(task_list)==1:
            print("|\t", temporary[0], "\t\t|\t\t", temporary[1], "km\t\t|\t", temporary[2], "km\t\t|\t\t",temporary[3], "\t|")
            print("---------------------------------------------------------------------")

        #There was an error with printing task4, solution:
        elif temporary[0] == "Task4" and len(task_list)!=1:
            print("|\t", temporary[0], "\t\t|\t\t", temporary[1], "km\t|\t", temporary[2], "km\t\t|\t\t", temporary[3], "\t|")
            print_remaining_tasks(task_list, x + 1)

        else:
            print("|\t", temporary[0], "\t\t|\t\t", temporary[1], "km\t\t|\t",temporary[2], "km\t\t|\t\t", temporary[3], "\t|")
            print_remaining_tasks(task_list, x + 1)

    elif x>0 and x<len(task_list)-1:
        if temporary[0] == "Task4":
            print("|\t", temporary[0], "\t\t|\t\t", temporary[1], "km\t|\t", temporary[2], "km\t\t|\t\t", temporary[3], "\t|")
        else:
            print("|\t", temporary[0], "\t\t|\t\t", temporary[1], "km\t\t|\t",temporary[2], "km\t\t|\t\t", temporary[3], "\t|")

        print_remaining_tasks(task_list, x + 1)

    elif x == len(task_list)-1:
        if temporary[0] == "Task4":
            print("|\t", temporary[0], "\t\t|\t\t", temporary[1], "km\t|\t", temporary[2], "km\t\t|\t\t", temporary[3], "\t|")
        else:
            print("|\t", temporary[0], "\t\t|\t\t", temporary[1], "km\t\t|\t", temporary[2], "km\t\t|\t\t", temporary[3], "\t|")
        print("---------------------------------------------------------------------")

    else:
        print("")

def hall_of_fame(total_time):
    name = input("What is your name :")

    temp ="|\t" + name + "\t|\t" + (str)(total_time) + " hour\t|\n"

    f = open("HallOfFame.txt", "a")
    f.writelines(temp)
    f.close()

    print("\n\tHall Of Fame")
    print("-----------------------------")
    print("|\tName\t|\tFinish Time\t|")
    print("-----------------------------")

    d = open("HallOfFame.txt", "r")
    for i in range(3):
        line = d.readline()
        print(line,end="")
        print("-----------------------------")
    d.close()

way_main=["foot","pegasus"]
travel_type1 = "travel"
travel_type2 = "home"
alive = True

print("Welcome to Hero’s 5 Labors!")
print("Remaining HP for Hero :", hero_hp)
print("Remaining HP for Pegasus :", pegasus_hp)

while alive:
    a=0 #index

    print_remaining_tasks(task_list,a)

    task = input("Where should Hero go next?").lower()
    task = Invalid_tasks(task_list, task)
    task_origin = task

    way = input("How do you want to travel?(Foot/Pegasus)").lower()
    way=Invalid_way(way_main, way,travel_type1)

    rn = travel_damage(task, way, hero_hp, pegasus_hp, total_time,alive, travel_type1 )
    print(rn)
    hero_hp = rn[0]
    pegasus_hp = rn[1]
    task = rn[2]
    total_time= rn[3]
    alive=rn[4]

    if alive == False:
        break

    returning = input("How do you want to go home?(Foot/Pegasus)")
    returning = Invalid_way(way_main, returning,travel_type2)
    xd = home_damage(task, returning, hero_hp , pegasus_hp, alive, total_time,travel_type2)
    x = 0 #index

    hero_hp = xd[0]
    pegasus_hp = xd[1]
    total_time = xd[3]
    alive = xd[2]
    task_list = remove_task(task_list, task_origin, x)

    if alive==True and len(task_list)==0:
        print("Congratulations, you have completed the task.")
        hall_of_fame(total_time)
        alive = False