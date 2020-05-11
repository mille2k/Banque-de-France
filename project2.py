file=open("conf.txt","r")
dic={}
for line in file:
    if line[0]!="#" and line[0]!=";" and line[0]!="\n":
        stringl=line.split(maxsplit=1)
        if len(stringl)>1:
            key=stringl[0]
            dic[key]=stringl[1]
        else:
            dic[stringl[0]]=" "
file.close()
while True:
    ques = input("Введите запрос вида get param : ")
    a = ques.split()
    for key in dic:
        if a[2]==key:
            if dic[key]!= " ":
                print(key,':',dic[key])
            else:
                print(key,':')
    while True:
        cont=input('Продолжить?(Да/Нет): ')
        if cont== 'Да':
            break;
        elif cont=='Нет':
            exit()



