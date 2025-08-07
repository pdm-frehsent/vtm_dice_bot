from random import randint

def roll(pool_check, hunger):
    crit_fail = 'Crit Fail'
    crit_success = 'CRIT Success'
    success = 'Success'
    blood_fail = 'BLOOD Fail'
    blood_success = 'BLOOD Success'

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
            item = result

        if i+1 <= hunger:
            if item == crit_fail:
                item = blood_fail
            elif item == crit_success:
                item = blood_success
        
        results[i] = item



        fstr = fstr+f'{item}\n'
  

    successes = results.count(success) + (results.count(crit_success)+results.count(blood_success))*2 - (results.count(crit_success)+results.count(blood_success))%2
    crits = results.count(crit_success)+results.count(blood_success)
    if results.count(blood_success) > 0 and crits > 1:
        blood_triumph = True
    else:
        blood_triumph = False
    fstr = fstr+f'\n<b>Успехов: {successes}</b>'
    if blood_triumph:
        fstr = fstr + ' (BLOOD TRIUMPH!!!)'
    return fstr

