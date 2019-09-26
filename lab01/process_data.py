names_count = {}

with open("female-names.txt", "r") as reader:
    for line in reader:
        if line[0] not in names_count.keys():
            names_count[line[0]] = 0
        names_count[line[0]] += 1

with open("female-names-count.txt", "w") as writer:
    for key, value in names_count.items():
        writer.write(f" SET {key} {value}\n")