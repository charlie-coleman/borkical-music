letters = 'abcdefg'
numbers = '456'
change = [2, 1, 2, 2, 1, 2, 2]
num_arr = []
let_arr = []
num = -15
i = 0
started = False
for n in numbers:
    for l in letters:
        let_arr.append(l+n)
print(len(let_arr))
print(let_arr)
for n in numbers:
    for l in letters:
        if started:
            num += change[(i % len(change))]
            num_arr.append(num)
            i += 1
        else:
            num_arr.append(-15)
            started = True
print(len(num_arr))
print(num_arr)