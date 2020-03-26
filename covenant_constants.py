# covenant lab upkee

#low upkeep costs
lab_upkeep_low = {
    -5: 1,
    -4: 2,
    -3: 3,
    -2: 5,
    -1: 7,
    0 : 10,
    1 : 15}
def lab_upkeep(cost):
    if cost < 2:
        return lab_upkeep_low[cost]
    return 5 * (cost) * (cost + 1)

spring_calc = {
'magi' : 5,
'nobles' : 5,
'companions' : 3,
'crafters' : 2,
'specialists': 2
}
summer_calc = {
'magi' : 10,
'nobles' : 10,
'companions' : 5,
'crafters' : 3,
'specialists': 3,
'horses' : 1
}
    

cost_max = {
    'buildings' : 0.5,
    'consumables' : 0.2,
    'laboratories' : 0.2,
    'provisions' : 0.2,
    'arms' : 0.5,
    'writing' : 0.5}
