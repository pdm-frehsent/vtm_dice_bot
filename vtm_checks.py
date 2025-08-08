from random import randint

def roll(pool_check, hunger):
    fail = "Провал"
    crit_fail = 'Провал (1)'
    blood_fail = "Провал (на крови)"
    crit_success = '(+) КРИТ'
    blood_success = "(+) Успех (на крови)"
    success = '(+) Успех'
    blood_crit_fail = 'ПРОВАЛ (1) (на крови)'
    blood_crit = '(+) КРИТ (на крови)'

    hunger = int(hunger)
    pool_check = int(pool_check)
    results  = [0]*pool_check
    fstr = ''

    for i, item in enumerate(results):
        result = randint(1, 10)
        if result == 1:
            item = crit_fail
        elif result == 10:
            item = crit_success
        elif result > 5:
            item = success
        else:
            item = fail

        if i+1 <= hunger:
            if item == crit_fail:
                item = blood_crit_fail
            elif item == crit_success:
                item = blood_crit
            elif item == success:
                item == blood_success
            elif item == fail:
                item = blood_fail
        
        results[i] = item



        fstr = fstr+f'{item}\n'
  

    successes = results.count(success) + results.count(blood_success) + (results.count(crit_success)+results.count(blood_crit))*2 - (results.count(crit_success)+results.count(blood_crit))%2
    crits = results.count(crit_success)+results.count(blood_crit)
    if results.count(blood_crit) > 0 and crits > 1:
        blood_triumph = True
    else:
        blood_triumph = False
    fstr = fstr+f'\n<b>Успехов: {successes}</b>'
    if blood_triumph:
        fstr = fstr + ' (КРОВАВЫЙ ТРИУМФ!!!)'
    return fstr

