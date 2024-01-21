def find_last_person(n):
    colleagues = list(range(1, n + 1))
    
    index = 0
    while len(colleagues) > 1:
        index = (index + 2) % len(colleagues)  
        colleagues.pop(index)
    
    return colleagues[0]

n = int(input("please input (0~100): "))

if 0 <= n <= 100:
    result = find_last_person(n)
    print(f"answer is {result}")
else:
    print("input invalid, please input (0~100)")
