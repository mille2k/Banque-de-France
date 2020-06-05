from abc import ABC, abstractmethod, abstractclassmethod
import random

class Abstract(ABC):

    def enter_way(self,str):
        flag=True
        while flag:
            way=input("Укажите путь к файлу с нужным расширением ")
            try:
                exampl=way.split('.')
                exampl.reverse()
                if exampl[0]==str:
                    return way
                raise Exception("Указано неверное расширение")
            except Exception:
                print("Неправильный путь / Файл не найден")


    
    def read_txt(self):
        print("Укажите файл с текстом для шифровки")       
        file_txt=open(self.enter_way("txt"),"r", encoding='utf-8')
        return file_txt

    
    def read_encrypt(self):
        print("Укажите путь для зашифрованного файла")      
        encrypt_file=open(self.enter_way("encrypt"),"r", encoding='utf-8')
        return encrypt_file

     
    def read_alpha(self):   
        print("Укажите путь к файлу с алфавитом")
        alpha_list=[]
        with open(self.enter_way("alph"),"r",encoding='utf-8') as file_alpha:
            line=file_alpha.readline()
            while line:
                if line[0]!='\n':
                    if len(line)<3:
                        if alpha_list.count(line[0])<1:
                            alpha_list.append(line[0])
                line=file_alpha.readline()
        return alpha_list


class repl(Abstract):
    

  
    def Encrypt(self): 
        key_dict=self.read_key()
        while key_dict==None:
            print("Ключ не подходит к методу шифровки")
            key_dict=self.read_key()
        file_txt=self.read_txt()
        print("Укажите имя файла с зашифрованным текстом")
        way=self.enter_way("encrypt")
        new_line=''
        flag=True
        with open(way,'w', encoding='utf-8') as encrypt_file:
            encrypt_file.write("Метод зашифровки: 1 - :Замена\n")
        for line in file_txt:  
            for ch in line:
                for key,value in key_dict.items():   
                    if ch==key:         
                        ch_new=key_dict[key]
                        new_line=new_line+ch_new
                        flag=False
                        break
                if flag:
                   new_line=new_line+ch
                flag=True
            with open(way,'a', encoding='utf-8') as encrypt_file:
               encrypt_file.write(new_line)
            new_line='' 
        print("Текст зашифрован")
    
    def decode(self):
        key_dict=self.read_key()
        while key_dict==None:
            print("Ключ не подходит к методу шифровки")
            key_dict=self.read_key()
        encrypt_file=self.read_encrypt()
        line=encrypt_file.readline()
        confirm=line.split(' ')
        while confirm[4]!=':Замена\n':
            print('Зашифрованный файл не подходит ')
            encrypt_file=self.read_encrypt()
            line=encrypt_file.readline()
            confirm=line.split(' ')
        new_line=''
        flag=True
        print("Введите имя для расшифрованного файла")
        with open(self.enter_way("txt"),'w') as decrypt_file:
            for line in encrypt_file:  
                for ch in line:
                    for letter_first,letter_second in key_dict.items():                            
                        if ch==letter_second:    
                            ch_new=letter_first
                            new_line=new_line+ch_new
                            flag=False
                            break
                    if flag:
                       new_line=new_line+ch
                    flag=True
                decrypt_file.write(new_line)
                new_line=''
        print("Файл расшифрован")
   
    def key_generator(self):
        self.alpha_data=self.read_alpha()
        new_list=random.sample(self.alpha_data, len(self.alpha_data))
        print("Введите имя для файла с ключом")
        with open(self.enter_way("key"),'w',encoding='utf-8') as gen_key:
            i=0
            while i<len(self.alpha_data):
                string=self.alpha_data[i]+' '+new_list[i]+'\n'
                gen_key.write(string)
                i+=1 
            gen_key.write('\nСпособ - :Замена')
        print("Ключ создан")

    def read_key(self):
        print("Укажите путь к файлу с ключом")
        key_dict=dict()
        next=0
        with open(self.enter_way("key"),'r', encoding='utf-8') as key_file:
            line=key_file.readline()
            while line:
                if line[0]!='\n':
                    test_list=line.split(' ',1)
                    if len(test_list)==1:
                        pass
                    elif len(test_list)==2 and test_list[1]!='- :Замена':
                        key_dict[line[0]]=line[2]
                    elif len(test_list)==2:
                        if test_list[1]=='- :Замена':
                            next+=1
                        else:
                            print("Неправильный ключ")
                            return None
                line=key_file.readline()
        if next==0:
            return None
        elif next>0:
            return key_dict


class tranpos(Abstract):

  

    def read_key(self):
        print("Укажите путь к файлу с ключом")
        key_list=[]
        exit=0
        with open(self.enter_way("key"),'r', encoding='utf-8') as key_file:
            flag=True
            while flag:
                try:
                    line=key_file.readline()
                    length=int(line)
                    line=key_file.readline()
                    key_list=line.split(' ')
                    if len(key_list)!=length:
                        line=key_file.readline()
                    if len(key_list)==length:
                        line=key_file.readline()
                        line=line.split(' ')
                        if len(line)==3:
                            if line[2]==':Перестановка':
                                return key_list
                        elif len(line)<3:
                            exit+=1
                            if exit==100:
                                return None
                        else:
                            return None
                except ValueError:
                    exit+=1
                    if exit==100:
                       return None
        return key_list

   
    def gener_key(self):   
        try:
            length=0
            while length<2:
                length=int(input("Введите длину ключа "))
                if length<2:
                    print("Слишком мало ")
            length+=1
            key_list=[x for x in range(1, length)]
            random.shuffle(key_list)
            with open(self.enter_way("key"),'w',encoding='utf-8') as gen_key:
                gen_key.write(str(length)+'\n')
                i=0
                string=''
                while i<len(key_list):                   
                    string=string+str(key_list[i])+' '
                    i+=1 
                gen_key.write(string)
                gen_key.write('\nСпособ - :Перестановка')
        except Exception:
            print("Неправильный ввод")

    def encrypt(self):    
        key_list=self.read_key()
        while key_list==None:
            print("Ключ не подходит к методу шифровки")
            key_list=self.read_key()
        file_txt=self.read_txt()
        if key_list[-1]=='':
            key_list.pop()
        length=len(key_list)-1
        line=file_txt.read()
        list_block_length=[]
        i=0
        my_list=list()
        print("Укажите имя файла с зашифрованным текстом ")
        with open(self.enter_way("encrypt"),'w',encoding='utf-8') as encode_file:
            encode_file.write("Способ шифрования: 2 - Перестановка\n")
            for index in range(0,len(line),length):
                if index<=len(line):
                    my_list=list(line[index:index+length])
                i=0
                list_none=[None]*len(key_list)
                for item in my_list:
                    if len(my_list)<length:
                        my_list.append("q")
                    list_none[int(key_list[i])-1]=item              
                    i+=1
                string=''
                for item in list_none:
                    if item==None:
                        item=''
                    string=string+item
                encode_file.write(string)

    def decode(self):
            key_list=self.read_key()
            while key_list==None:
                print("Ключ не подходит к методу")
                key_list=self.read_key()
            encrypt_file=self.read_encrypt()
            line=encrypt_file.readline()
            confirm=line.split(' ')
            while confirm[4]!='Перестановка\n':
                print('Зашифрованный файл не подходит')
                encrypt_file=self.read_encrypt()
                line=encrypt_file.readline()
                confirm=line.split(' ')
            line=encrypt_file.read() 
            if key_list[-1]=='':
               key_list.pop()
            length=len(key_list)-1
            print("Укажите имя файла с расшифрованным текстом ")
            with open(self.enter_way("txt"),'a',encoding='utf-8') as decode_file:
                for index in range(0,len(line),length):
                    if index<=len(line):
                        my_list=list(line[index:index+length])
                    i=0
                    string=''
                    for item in my_list:
                        ch=my_list[int(key_list[i])-1]
                        i+=1
                        string=string+ch
                    decode_file.write(string)


class Gamm(Abstract):
   
    def read_key(self):
        exit=0
        index=0
        i=0
        list_alph=list()
        list_key=list()
        flag=True
        print("Укажите путь к файлу с ключом")
        while flag:
                with open(self.enter_way("key"),'r',encoding='utf-8') as key_file: 
                    for line in key_file:
                         try:
                             if line=='Key\n':
                                 j=0
                                 line=key_file.readline()
                                 list_key=line.split()
                                 if len(list_key)==1:
                                    list_alph.append(list_key[0])
                                    j+=1
                                 elif len(list_key)==2:
                                     index=int(list_key[1])
                                     j+=1
                                     i+=1
                                 if j==0 and line!='\n':
                                     list_key=line.split()
                                     if list_key[-1]=='Gam':
                                        break
                                     else:
                                         exit+=1
                                         break
                             if i==1 and line!='\n':
                                 if list_alph.count(line[0])==0:
                                    list_alph.append(line[0])
                             if i==0:
                                 list_second_line=line.split()
                                 if list_alph.count(line[0])==0:
                                    list_alph.append(line[0])
                                 if len(list_second_line)>1:
                                    index=int(list_second_line[1])
                                 else:
                                     index=0
                                 del(list_second_line)
                                 i+=1
                         except ValueError:
                             pass
                all_list=list()
                if exit==0:
                   all_list.append(list_alph)
                   all_list.append(list_key)
                   all_list.append(index)
                else:
                    return None
                return all_list
           

    def alphabet(self):
        print("Укажите путь к файлу с алфавитом ")
        alphabet=open(self.enter_way("alph"),"r",encoding='utf-8')
        return alphabet
        
    def gen_key(self): 
        list_key=list()
        alphabet_file=self.alphabet()
        list_alph=alphabet_file.read()
        gamma=0
        print("Введите длину ключа, большую чем 1 ")
        while gamma<2:
            gamma=int(input(".>> "))
            if gamma<2:
                print("Введите длину больше чем 1 ")
        i=0
        list_alph=list_alph.split('\n')
        list_key=[x for x in range(1, gamma+1)]
        random.shuffle(list_key)
        print("Укажите путь к файлу с ключом")
        list_key.append('Gam')
        with open(self.enter_way("key"),"w", encoding='utf-8') as key_file:
            for ellement in list_alph:
                key_file.write(str(ellement)+'\n')
            key_file.write("\n\nKey\n")
            for ellement in list_key:
                key_file.write(str(ellement))
                key_file.write(' ')
            key_file.write('\nспособ - :Гаммирование')
        print("Ключ создан")



    def encrypt(self):
        text_file=self.read_txt()
        list_alph=list()
        list_key=list()
        index=0
        i=0
        all_list=self.read_key()
        while all_list==None:
            print("Указан неправильный ключ")
            all_list=self.read_key()
        list_alph=all_list[0]
        list_key=all_list[1]
        if list_key[-1]=='XOR':
            list_key.pop()
        index=all_list[2]
        print("Укажите путь к файлу с зашифрованным текстом ")
        string_line=''
        index_encode=0
        encode_ellement=''
        exit=0
        with open(self.enter_way("encrypt"),'w',encoding='utf-8') as encode_file:
            encode_file.write("Способ шифрования: 3 - Гаммирование\n")
            while exit!=100:
                text=text_file.read(len(list_key))
                i=0
                string_block=''
                new_index=0
                if text=='':
                    exit+=1
                for ch in text:
                    try:
                        if 0<list_alph.count(ch):
                            index_encode=list_alph.index(ch)+index
                            key_ellement=list_key[i]
                            encode_ellement=list_alph[(index_encode+int(key_ellement))%len(list_alph)]
                            i+=1
                            string_block=string_block+encode_ellement
                        else:
                            string_block=string_block+ch
                    except ValueError:
                        pass
                string_line=string_line+string_block
            encode_file.write(string_line)
        print("Зашифровано")


    def decode(self):
        encrypt_file=self.read_encrypt()
        line=encrypt_file.readline()
        confirm=line.split(' ')
        while confirm[4]!='Гаммирование\n':
                print('Файл не подходит, укажите файл с зашифрованным текстом')
                encrypt_file=self.read_encrypt()
                line=encrypt_file.readline()
                confirm=line.split(' ')
        list_alph=list()
        list_key=list()
        i=0
        all_list=self.read_key()
        while all_list==None:
            print("Неправильный ключ")
            all_list=self.read_key()
        list_alph=all_list[0]
        list_key=all_list[1]
        index=all_list[2]
        if list_key[-1]=='Gam':
            list_key.pop()
        index=all_list[2]
        string_line=''
        index_encode=0
        encode_ellement=''
        exit=0
        print("Укажите путь к файлу с расшифрованным тестом ")
        with open(self.enter_way("txt"),'w',encoding='utf-8') as decrypt_file:            
            while exit!=100:
                text=encrypt_file.read(len(list_key))
                i=0
                string_block=''
                new_index=0
                if text=='':
                    exit+=1
                for ch in text:
                    try:
                        if 0<list_alph.count(ch):
                            index_encode=list_alph.index(ch)-index 
                            key_ellement=list_key[i]
                            j=(index_encode-int(key_ellement))%(len(list_alph))
                            encode_ellement=list_alph[j]
                            i+=1
                            string_block=string_block+encode_ellement
                        else:
                            string_block=string_block+ch
                    except ValueError:
                        pass
                string_line=string_line+string_block
            decrypt_file.write(string_line)
        print("Успешно")

obj=repl()
obj2=tranpos()
obj3=Gamm()

flag=True
i=0
while flag:
    try:
        print(" Главное меню")
        print(" \t1) Зашифровка/Расшифровка")
        print(" \t2) Создать ключ")
        print(" \t3) Выход")
        command=int(input("Выберите действие "))
        if command<1 or command>3:
            print("Неправильный выбор")
            i+=1
            if i>3:
                print('Слишком много ошибок')
                flag=False
                break
        if command==1:
            i=0
            main_menu=0
            while flag and main_menu!=1:
                print(" Зашифровка/Расшифровка")
                print(" \t1) Зашифровка")
                print(" \t2) Расшифровка")
                print(" \t3) Обратно в главное меню")
                command=int(input("Выберите действие "))
                if command<1 or command>3:
                    print("Неправильный выбор")
                    i+=1
                    if i>2:
                        print('Слишком много ошибок')
                        flag=False
                        break
                if command==1:
                        i=0
                        main_menu=0
                        while flag:
                            print(" Выберите метод шифровки ")
                            print(" \t1) Замена")
                            print(" \t2) Перестановка")
                            print(" \t3) Гаммирование")
                            print(" \t4) Обратно в главное меню")
                            command=int(input("Выберите действие "))
                            if command<1  or command>4:
                                print("Неправильный выбор")                        
                                i+=1
                                if i>2:
                                    print('Слишком много ошибок')
                                    flag=False
                                    break
                            if command==1:
                                obj.Encrypt()
                            if command==2:
                                obj2.encrypt()
                            if command==3:
                                obj3.encrypt()
                            if command==4:
                                main_menu=1
                                break
                elif command==2:
                        i=0
                        main_menu=0
                        while flag:
                            print(" Выберите метод шифровки ")
                            print(" \t1) Замена")
                            print(" \t2) Перестановка")
                            print(" \t3) Гаммировние")
                            print(" \t4) Обратно в главное меню")
                            command=int(input("Выберите действие "))
                            if command<1 or command>4:
                                print("Неправильный выбор")
                                i+=1
                                if i>2:
                                    print('Слишком много ошибок')
                                    flag=False
                                break
                            if command==1:
                                obj.decode()
                            elif command==2: 
                                obj2.decode()
                            elif command==3:
                                obj3.decode()           
                            if command==4:
                                main_menu=1
                                break
                elif command==3:
                    main_menu=1
                    break
        elif command==2:
            i=0
            main_manu=1
            while flag:
                print(".>> ВЫберите метод:")
                print(".>> \t1) Замена")
                print(".>> \t2) Перестановка")
                print(".>> \t3) Гаммирование")
                print(".>> \t4) Обратно в главное меню")
                command=int(input("Выберите действие "))
                if command<1 or command>4:
                    print("Неправильный выбор")
                    i+=1
                    if i>2:
                        print('Слишком много ошибок')
                        flag=False
                        break
                if command==1:
                    obj.key_generator()
                elif command==2:
                    obj2.gener_key()
                elif command==3:
                    obj3.gen_key()
                elif command==4:
                    main_menu=1
                    break
        elif command==3:
            flag=False
            break
        if main_menu==0:
            command=input("Вернуться в гланое меню? Y/N").lower()
            if command[0]=='n':
                flag=False
                break
    except SyntaxError:
        print("Неправильная еоманда")
    except ValueError:
       print("Неправильная команла\данные в файле")
    except PermissionError:
        print("Невозможно открыть файл")
        flag=False
        break
    except FileNotFoundError:
                print("Файл не найден")
    except IndexError:
        print("Проблемы с файлом, проверьте и переделайте его в првильный формат")
    except Exception:
        print("Системная ошибка ")
        flag=False
        break
    except BaseException:
        print("Системная ошибка")
        flag=False
        break