def convert_to_readable_time_string(seconds):
    seconds = int(seconds)
    hours = int(seconds / 3600)
    seconds = - hours * 3600
    mins = int(seconds / 60)
    seconds = - mins * 60
    if hours:
        return str(hours) + 'h ' + str(mins) + 'min ' + str(seconds) + 's'
    elif mins:
        return str(mins) + 'min ' + str(seconds) + 's'
    else:
        return str(seconds) + 's'
