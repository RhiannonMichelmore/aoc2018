import os
import copy
import math
import sys
import numpy as np
import time
import re
import numpy as np

def solve(filepath):
    orig_groups = []
    NUM_IN_FACTION = 10
    with open(filepath) as f:
        line = f.readline()
        #Immune system first
        for i in range(NUM_IN_FACTION):
            line = f.readline().strip()
            orig_groups.append(make_group(line,'immune',i+1))

        line = f.readline()
        line = f.readline()

        for i in range(NUM_IN_FACTION):
            line = f.readline().strip()
            orig_groups.append(make_group(line,'infection',i+1))

        #for g in groups:
        #    print(g.id)
        immune_wins = False
        boost = 1
        while not immune_wins:
            groups = copy.deepcopy(orig_groups)
            for g in groups:
                if g.faction=='immune':
                    g.attack_val += boost
            fighting = True
            last_immune_win = 0
            if boost % 20 == 0:
                print(boost)
            
            counter = 0
            while fighting:
                if counter > 100000:
                    print("broken")
                    boost +=1
                    break
                counter += 1
                groups.sort(key=lambda g: ((g.n_units*g.attack_val),g.initiative),reverse=True)
                chosen = []
                for g in groups:
                    #print(str(g.n_units*g.attack_val),str(g.initiative))
                    #determine how much damange it would do to each enemy
                    enemies = [e for e in groups if not e.faction == g.faction and not (e.id,e.faction) in chosen]
                    damages = []
                    eff_pow = g.n_units*g.attack_val
                    for e in enemies:
                        damage = eff_pow
                        if g.attack_type in e.immunities:
                            damage = 0
                        elif g.attack_type in e.weakness:
                            damage *= 2
                        damages.append((damage,e))

                    damages.sort(key=lambda kv: (kv[0],(kv[1].n_units*kv[1].attack_val),kv[1].initiative),reverse=True)
                    if len(damages) == 0:
                        g.target = None
                    else:
                        target = damages[0]
                        if target[0] == 0:
                            g.target = None
                            #print(g.faction,g.id,"would deal no damage")
                        else:
                            g.target = target[1].id
                            chosen.append((target[1].id,target[1].faction))
                            #print(g.faction,g.id,"would deal",target[1].faction,target[1].id,target[0],"damage")

                groups.sort(key=lambda g: g.initiative,reverse=True)
                for g in groups:
                    if g.n_units <= 0:
                        continue
                    elif g.target == None:
                        continue
                    else:
                        #get target
                        target = [i for i in groups if i.id == g.target and not i.faction == g.faction][0]
                        damage_to_target = g.n_units*g.attack_val
                        #print(g.attack_type,target.immunities,target.weakness)
                        if g.attack_type in target.immunities:
                            damage_to_target = 0
                        elif g.attack_type in target.weakness:
                            damage_to_target *= 2
                        n_units_removed = math.floor(damage_to_target/target.unit_hp)
                        target.n_units -= n_units_removed
                        actual_removed = n_units_removed + (target.n_units if target.n_units <0 else 0)
                        #print(g.faction,g.id,"attacks",target.faction,target.id,"for",damage_to_target,"damage, killing",actual_removed,"units")


                #remove all 0 unit groups
                groups = [g for g in groups if g.n_units > 0]
                immune = [g for g in groups if g.faction == 'immune']
                infect = [g for g in groups if g.faction == 'infection']
                if len(immune) == 0:
                    fighting = False
                    boost += 1
                    total = sum([g.n_units for g in infect])
                    #print("Boost:",boost-1,"Infection wins:",total,"units left.")
                elif len(infect) ==0:
                    boost +=1
                    fighting = False
                    total = sum([g.n_units for g in immune])
                    print("Immune wins:",total,"units left.")
                    immune_wins = True




def make_group(line,faction,ident):
    regex_string = r'^(\d+) units each with (\d+) hit points (\((weak|immune) to ([a-z]+)(, ([a-z]+))*(; (weak|immune) to ([a-z]+)(, ([a-z]+))*)*\) )*with an attack that does (\d+) ([a-z]+) damage at initiative (\d+)$'
    regex = re.compile(regex_string)
    m = regex.match(line)
    n_units = int(m.group(1))
    unit_hp = int(m.group(2))
    weakness = []
    immunities = []
    if m.group(3):
        if m.group(4) == 'immune':
            immunities.append(m.group(5))
            if m.group(6):
                immunities.append(m.group(7))
        elif m.group(4) == 'weak':
            weakness.append(m.group(5))
            if m.group(6):
                weakness.append(m.group(7))
    if m.group(8):
        if m.group(9) == 'immune':
            immunities.append(m.group(10))
            if m.group(11):
                immunities.append(m.group(12))
        elif m.group(9) == 'weak':
            weakness.append(m.group(10))
            if m.group(11):
                weakness.append(m.group(12))
    attack_val = int(m.group(13))
    attack_type = m.group(14)
    initiative = int(m.group(15))
    return Group(ident,faction,n_units,unit_hp,immunities,weakness,attack_val,attack_type,initiative)

class Group:
    def __init__(self,ident,faction,n_units,unit_hp, immunities, weakness, attack_val, attack_type, initiative):
        self.id = ident
        self.faction = faction
        self.n_units = n_units
        self.unit_hp = unit_hp
        self.immunities = immunities
        self.weakness = weakness
        self.attack_val = attack_val
        self.attack_type = attack_type
        self.initiative = initiative
        self.target = None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide an input data file path.")
    filepath = sys.argv[1]
    solve(filepath)
