import random

distinct_set_a = set()
distinct_set_b = set()

candidates = [ i for i in range(0, 42) ]

select_ratio = 0.4

for step in range(0, 100):

    for i in range(0, 1000):
        # method a
        a_list = candidates[:]
        random.shuffle(a_list)
        for j in range(0, 10):
            if random.random() >= select_ratio :
                continue
            batch = a_list[j*4:(j+1)*4]
            batch.sort()
            distinct_set_a.add(str(batch))
        # method b
        b_list = []
        for item in candidates:
            if random.random() < 0.4 :
                b_list.append(item)
        random.shuffle(b_list)
        for j in range(0, int(len(b_list)/4)):
            batch = b_list[j*4:(j+1)*4]
            batch.sort()
            distinct_set_b.add(str(batch))

    print('step %d: length a %d, length b %d'%\
          (step, len(distinct_set_a), len(distinct_set_b)))
