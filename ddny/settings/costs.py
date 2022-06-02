'''Copyright 2015 Downtown Divers New York. All Rights Reserved.'''

from decimal import Decimal

# NOTE(stpyang): This is just for the gas that the club purchaes.
# The banked gases automatically calculate their costs based on these constants.

PENNY = Decimal('0.01')

EQUIPMENT_COST_FIXED = Decimal(3.00).quantize(PENNY)
EQUIPMENT_COST_PROPORTIONAL = Decimal(0.08).quantize(PENNY)

AIR_COST = Decimal(0.03).quantize(PENNY)
ARGON_COST = Decimal(1.25).quantize(PENNY)
HELIUM_COST = Decimal(0.00).quantize(PENNY)
OXYGEN_COST = Decimal(0.45).quantize(PENNY)

MONTHLY_DUES = Decimal(37.00).quantize(PENNY)
