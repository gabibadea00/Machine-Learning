

from label_parser import isNaN

def calculate(data):

    counter = 0
    age = 0

    for entry in data:
        try:

            entry[2] = entry[2].lower().replace(" ", "")

            if isNaN(entry[2]):
                pass
            elif "lun" in entry[2] and "an" in entry[2]:
                age += int("".join(filter(str.isdigit, entry[2][0])))
            elif "nou" in entry[2] or "lun" in entry[2] or "zi" in entry[2] or "ore" in entry[2]:
                age += 1
            elif "an" in entry[2]:
                age += int("".join(filter(str.isdigit, entry[2])))
            elif entry[2].isdigit():
                age += int(entry[2])

            counter += 1

        except AttributeError as e:
            pass

    mean_age = age / counter

    return int(mean_age)