for x in range(2,101):
    flag = 0
    for y in range(2,x):
        if x%y==0:
            flag=1
            break
    if flag==0:
        print(x)