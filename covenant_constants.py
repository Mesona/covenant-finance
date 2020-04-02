# a file to keep all the charts and constants used by the covenant calculator

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


def semita(covenant):
        covenant.covenant_name = 'Semita Errabunda'
        covenant.covenant_season = 'spring'
        covenant.income_sources = {'trading' : 100}
        covenant.covenfolk_tiers = {
            'magi' : 5,
            'nobles' : 0,
            'companions' : 4,
            'crafters' : 12,
            'specialists': 4,
            'dependants': 5,
            'grogs': 20,
            'laborers' : 40,
            'servants' : 16,
            'teamsters' : 4,
            'horses': 6
            }
        covenant.laboratories = {
            'Carolus' : 0,
            'Mari' : 0,
            'Moratamis' : 0,
            'Tillitus' : 0,
            'Darius' : 2}
        covenant.treasury = 100.0
        covenant.armory = covenant.covenfolk_tiers['grogs'] * 32
        covenant.writers = 4
        covenant.cost_savings = [
            ['provisions', 'brewer', 6],
            ['provisions', 'brewer', 6],
            ['buildings', 'thatcher', 6],
            ['buildings', 'carpenter', 6],
            ['buildings', 'furniture maker', 6],
            ['buildings', 'carpenter', 6],
            ['consumables', 'blacksmith', 6],
            ['consumables', 'cobbler', 6],
            ['consumables', 'tinker', 6],
            ['consumables', 'candlemaker', 6],
            ['consumables', 'magic loom, weaving', 6],
            ['consumables', 'magic anvil, blacksmith', 2]
            ]
        return covenant
