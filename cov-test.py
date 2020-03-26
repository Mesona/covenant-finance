#! python3
# cov-test.py - used to test functionality on covenant.py
from covenant import Covenant
import covenant_constants as cc

cov = Covenant()
print('Total covenant points: %s' % cov.calc_points())
print('Needed servants and teamsters: %s' % cov.calc_needs())

cov.advance_year()
cov.display_finances()
