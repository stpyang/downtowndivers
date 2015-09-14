'''Copyright 2015 Downtown Divers New York. All Rights Reserved.'''

from decimal import Decimal

# NOTE(stpyang): This is just for the gas that the club purchaes.
# The banked gases automatically calculate their costs based on these constants.

PENNY = Decimal('0.01')

EQUIPMENT_COST = Decimal(0.10).quantize(PENNY)
AIR_COST = Decimal(0.03).quantize(PENNY)
ARGON_COST = Decimal(1.00).quantize(PENNY)
HELIUM_COST = Decimal(1.35).quantize(PENNY)
OXYGEN_COST = Decimal(0.20).quantize(PENNY)
