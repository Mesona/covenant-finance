#! python3
# cov-test.py - used to test functionality on covenant.py
from covenant import Covenant
import covenant_constants as cc

cov = Covenant()

def gglynn(covenant):
        covenant.covenant_name = 'Gwenton Glynn'
        covenant.covenant_season = 'Autumn'
        covenant.income_sources = {
            'Agriculture' : 250,
            'Mining' : 100}
        covenant.covenfolk_tiers = {
            'magi' : 6,
            'nobles' : 0,
            'companions' : 6,
            'crafters' : 12,
            'specialists': 4,
            'dependants': 5,
            'grogs': 12,
            'laborers' : 30,
            'servants' : 36,
            'teamsters' : 14,
            'horses': 6
            }
        covenant.laboratories = {
            'Iactus' : 2,
            'Tepes' : 2,
            'Perat' : 2,
            'Fieri' : 2,
            'Cassius' : 2,
            'Hristos' : 2}
        covenant.treasury = 250.0
        covenant.armory = covenant.covenfolk_tiers['grogs'] * 32
        covenant.writers = 4
        covenant.cost_savings = [
            ['provisions', 'brewer', 6, 'crafter'],
            ['provisions', 'brewer', 6, 'crafter'],
            ['buildings', 'thatcher', 6, 'crafter'],
            ['buildings', 'carpenter', 6, 'crafter'],
            ['buildings', 'furniture maker', 6, 'crafter'],
            ['buildings', 'carpenter', 6, 'crafter'],
            ['consumables', 'blacksmith', 6, 'crafter'],
            ['consumables', 'candlemaker', 6, 'crafter'],
            ]
        return covenant


cov = gglynn(cov)
cov.display_finances()
print("Required Servants: " +str(cov.calc_needs()[0]))
print("Required Teamsters: " +str(cov.calc_needs()[1]))
print(cov.calc_expenditures())
