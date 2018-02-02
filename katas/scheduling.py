#! /Users/jayden/anaconda2/envs/py36/bin/python
def is_busy(current_timeslot, timeslot):
    if timeslot[0] <= current_timeslot[1] and timeslot[1] >= current_timeslot[0]:
        return True

    return False


def test_method(no_operators, timeslots):
    operators = list()
    for idx_timeslots, timeslot in enumerate(timeslots):
        timeslot_is_assigned = False
        if idx_timeslots == 0:
            operators.extend([[timeslot]])
            continue

        for idx_operator, operator in enumerate(operators):
            overlapped_slot = False
            for current_timeslot in operator:
                if is_busy(current_timeslot, timeslot):
                    overlapped_slot = True
                    break

            if not overlapped_slot:
                operators[idx_operator].append(timeslot)
                timeslot_is_assigned = True
                break

        if not timeslot_is_assigned:
            operators.extend([[timeslot]])


    if len(operators) > no_operators:
        return len(operators) - no_operators

    return 0


current_num_of_operators = 1
timeslots = [
    [0, 19],
    [30, 39],
    [10, 29],
    [30, 39],
    [40, 49],
    [0, 19],
    [20, 49],
    [40, 49],
    [24, 25],
    [20, 29]
]

# for timeslot in timeslots:
#     print(timeslot[0], timeslot[1])
print(test_method(current_num_of_operators, timeslots))


