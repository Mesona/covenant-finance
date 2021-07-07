#!/usr/bin/python3

from covenants import Covenant
from laboratories import Laboratory


def semita():
    cov = Covenant(
        name = 'Semita Errabunda',
        season = 'spring',
        income_sources = {'trading' : 100},
        covenfolk_tiers = {
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
        laboratories = {
            'Carolus' : Laboratory(owner = "Carolus"),
            'Mari' : Laboratory(owner = "Mari"),
            'Moratamis' : Laboratory(owner = "Moratamis"),
            'Tillitus' : Laboratory(owner = "Tillitus"),
            'Darius' : Laboratory(owner = Darius, size = 2),
        },
        treasury = 100.0,
        armory = covenant.covenfolk_tiers['grogs'] * 32,
        writers = 4,
        cost_savings = [
            ['provisions', 'brewer', 6, 'crafter'],
            ['provisions', 'brewer', 6, 'crafter'],
            ['buildings', 'thatcher', 6, 'crafter'],
            ['buildings', 'carpenter', 6, 'crafter'],
            ['buildings', 'furniture maker', 6, 'crafter'],
            ['buildings', 'carpenter', 6, 'crafter'],
            ['consumables', 'blacksmith', 6, 'crafter'],
            ['consumables', 'cobbler', 6, 'crafter'],
            ['consumables', 'tinker', 6, 'crafter'],
            ['consumables', 'candlemaker', 6, 'crafter'],
            ['consumables', 'weaving', 6, 'magic loom'],
            ['consumables', 'blacksmith', 2, 'magic anvil']
        ],
    )
    return cov


def gglynn():
    cov = Covenant(
        name = 'Gwenton Glynn',
        season = 'Autumn',
        income_sources = {
            'Agriculture' : 250,
            'Mining' : 100
        },
        covenfolk_tiers = {
            'magi' : 6,
            'nobles' : 0,
            'companions' : 6,
            'crafters' : 8,
            'specialists': 4,
            'dependants': 25,
            'grogs': 12,
            'laborers' : 30,
            'servants' : 38,
            'teamsters' : 15,
            'horses': 6
        },
        laboratories = {
            'Iactus' : Laboratory(owner = "Iactus", size = 3),
            'Tepes' : Laboratory(owner = "Tepes", size = 3),
            'Perat' : Laboratory(owner = "Perat", size = 3),
            'Fieri' : Laboratory(owner = "Fieri", size = 3),
            'Cassius' : Laboratory(owner = "Cassius", size = 3),
            'Hristos' : Laboratory(owner = "Hristos", size = 3)
        },
        treasury = 250.0,
        armory = covenant.covenfolk_tiers['grogs'] * 32,
        writers = 4,
        cost_savings = [
            ['provisions', 'brewer', 6, 'crafter'],
            ['provisions', 'brewer', 6, 'crafter'],
            ['buildings', 'thatcher', 6, 'crafter'],
            ['buildings', 'carpenter', 6, 'crafter'],
            ['buildings', 'furniture maker', 6, 'crafter'],
            ['buildings', 'carpenter', 6, 'crafter'],
            ['consumables', 'blacksmith', 6, 'crafter'],
            ['consumables', 'candlemaker', 6, 'crafter'],
        ],
        return covenant
