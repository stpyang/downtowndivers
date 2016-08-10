user_tanks = Tank.objects.filter(owner=user.member) \
    .order_by(tank_code)
non_user_tanks = Tank.objects.exclude(owner=user.member)
    .order_by(tank_code)
tanks = chain(user_tanks, non_user_tanks)
tank_info = defaultdict(list)
for tank in tanks:
    tank_dict = {
        "is_current_hydro": tank.is_current_hydro,
        "is_current_vip": tank.is_current_vip,
        "last_hydro_date": "None",
        "last_vip_date": "None",
        "tank_code": escape(tank.code),
        "tank_factor": tank.tank_factor,
    }
    if tank.last_hydro:
        tank_dict["last_hydro_date"] = str(tank.last_hydro.date)
    if tank.last_vip:
        tank_dict["last_vip_date"] = str(tank.last_vip.date)
    if tank.doubles_code:
        tank_info[escape(tank.doubles_code)] += [tank_dict]
    else:
        tank_info[escape(tank.code)] += [tank_dict]



__user_tanks = Tank.objects.filter(owner=user.member)
__non_user_tanks = Tank.objects.exclude(owner=user.member)
__tanks = [(t.owner.first_name, t.code, t.doubles_code) for t in (
    chain(__user_tanks, __non_user_tanks)
)]
__grouped_tanks = defaultdict(set)
for t in __tanks:
    __grouped_tanks[t[0]].add(t[2] if t[2] else t[1])
__choices = []
for g in __grouped_tanks:
    __codes = [(x, x) for x in __grouped_tanks[g]]
    __choices += [(g, __codes)]
tank = forms.ChoiceField(
    choices=__choices,
    required=True,
)

