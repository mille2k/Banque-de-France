flag = True
test = True

while flag:

    val_1 = int(input("Введите число X= "))
    val_2 = int(input("Введите число Y= "))
    while test:
        func = input("Выберете функию(+;-;*;/)")   
        if func == "+":
            result = val_1 + val_2
            test = False
            
        elif func == "-":
            result = val_1 - val_2
            test = False
            
        elif func == "*":
            result = val_1 * val_2
            test = False
            
        elif func == "/":
            while val_2 == 0:
                print("На ноль делить нельзя")
                val_2 = int(input("Введите второе число повторно "))
            result = val_1/val_2
            test = False
                
        else:
            result = "Неверный знак"
            
                

                
    
 
    print(result)
    counter = 0
    while True:
        if counter == 3:
            exit()
        rep = input("Продолжить? (Да или Нет)")
        if rep == "Да":
            test = True
            break
        elif rep == "Нет":
            flag = False 
            break
        else:    
            counter+=1 

        



