#! python3
# cov-test.py - used to test functionality on covenant.py
from covenant import Covenant
import covenant_constants as cc

cov = Covenant()

#test base covenant, Vernus
#print('Total covenant points: %s' % cov.calc_points())
#print('Needed servants and teamsters: %s' % cov.calc_needs())
#cov.display_finances()
#cov.advance_year()

# test second covenant, Semita Errebunda, for cost savings
cc.semita(cov)
cov.display_finances()
print(cov.calc_expenditures())
print(cov.calc_savings('buildings'))
