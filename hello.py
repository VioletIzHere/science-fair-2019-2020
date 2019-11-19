
# N = number of successful terror attacks

# chi = number of resources made per member in resource cell ### USE ### [1, 5] in 5 units

# nu_r_a = proportion of resources sent to action cell
# nu_re = number of recruits collected (exponential function of N) ### USE ### [1, 5] in 5 units

# rho_re = retention time of recruits
# rho_t = retention time of trainees

# zeta_a1 = number of members needed to perform a terror attack
# zeta_a2 = number of resources needed to perform a terror attack

# phi_t_a = probability that a trainee goes to an action cell
# phi_t_r = probability that a trainee goes to a resource cell
# phi_a1 = probability that a terror attack is successful ### USE ### [50, 90] in 5 units
# phi_a2 = probability that an individual in a terror attack is eliminated

import random, time, math

N = 0 ; chi = 1
nu_r_a = 0.7 ; nu_re = 3
rho_re = 2 ; rho_t = 3
zeta_a1 = 5 ; zeta_a2 = 10
phi_t_a = 90 ; phi_t_r = 10 ; phi_a1 = 80 ; phi_a2 = 10

def initialize(c, nu):
    global chi, nu_re, phi_a1
    chi = c
    nu_re = nu

initialize(5,5)

# let's use 3 action cells, one resource cell, one recruit cell, and one training cell

class Agent:
    def __init__(self, retention):
        self.retention = retention

resource_cell = {
    "members": [],
    "resources": 0
}

recruit_cell = {
    "members": []
}

training_cell = {
    "members": []
}

action_cells = [
    {
        "members": [],
        "resources": 0
    },
    {
        "members": [],
        "resources": 0
    },
    {
        "members": [],
        "resources": 0
    }
]

t = 0

for k in range(27):

    t += 1

    for i in list(range(len(recruit_cell["members"])))[::-1]:
        recruit_cell["members"][i].retention += 1
        if recruit_cell["members"][i].retention >= rho_re:
            recruit_cell["members"].pop(i)
            training_cell["members"].append(Agent(0))
    for i in range(int(math.pow(nu_re, N))):
        recruit_cell["members"].append(Agent(0))

    for i in list(range(len(training_cell["members"])))[::-1]:
        training_cell["members"][i].retention += 1
        if training_cell["members"][i].retention >= rho_t:
            training_cell["members"].pop(i)
            if random.randint(1, 100) <= phi_t_a:
                action_cells[random.randint(0, 2)]["members"].append(Agent(0))
            else:
                resource_cell["members"].append(Agent(0))
    
    resource_cell["resources"] += len(resource_cell["members"]) * chi
    action_cells[random.randint(0, 2)]["resources"] += int(nu_r_a * resource_cell["resources"])
    resource_cell["resources"] -= int(nu_r_a * resource_cell["resources"])

    for i in [0, 1, 2]:
        if len(action_cells[i]["members"]) >= zeta_a1 and action_cells[i]["resources"] >= zeta_a2:
            if random.randint(1, 100) <= phi_a1:
                N += 1
            for j in list(range(len(action_cells[i]["members"])))[::-1]:
                if random.randint(1, 100) <= phi_a2:
                    action_cells[i]["members"].pop(j)
            action_cells[i]["resources"] -= random.randint(int(action_cells[i]["resources"] / 2), action_cells[i]["resources"])
    
    print(str(len(action_cells[0]["members"]) + len(action_cells[1]["members"]) + len(action_cells[2]["members"])))
