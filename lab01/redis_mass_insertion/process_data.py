names_count = {}

with open("female-names.txt", "r") as reader:
    for line in reader:
        first_char = line[0].upper()
        if first_char not in names_count.keys():
            names_count[first_char] = 0
        names_count[first_char] += 1

with open("initials4redis.txt", "w") as writer:
    for key, value in names_count.items():
        writer.write(f" SET {key} {value}\n")