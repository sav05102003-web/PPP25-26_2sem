import random

def choose_difficulty():
    while True:
        try:
            level = int(input("Выберите уровень сложности (1-3): "))
            if level == 1:
                return 1, 10, 5
            elif level == 2:
                return 1, 50, 7
            elif level == 3:
                return 1, 100, 10
            else:
                print("Пожалуйста, выберите уровень 1, 2 или 3.")
        except ValueError:
            print("Пожалуйста, введите число от 1 до 3.")

def play_game():
    print("Добро пожаловать в игру 'Угадай число'!")
    
    min_num, max_num, attempts = choose_difficulty()
    secret_number = random.randint(min_num, max_num)
    attempts_left = attempts
    attempt_count = 0
    
    print(f"Я загадал число от {min_num} до {max_num}. У вас {attempts} попыток.")
    print("Чтобы выйти напишите exit или выход или выйти")
    
    while attempts_left > 0:
        user_input = input(f"У вас осталось {attempts_left} попыток. Введите число: ")
        
        if user_input.lower() in ["exit", "выход", "выйти"]:
            print("Спасибо за игру! До свидания!")
            return
        
        if user_input.lower() == "restart":
            print("Начинаем новую игру!")
            play_game()
            return
        
        try:
            guess = int(user_input)
            attempt_count += 1  
            
            if guess == secret_number:
                print(f"Поздравляем! Вы угадали число {secret_number} за {attempt_count} попыток!")
                break
            elif guess < secret_number:
                print("Загаданное число больше.")
            else:
                print("Загаданное число меньше.")
            
            attempts_left -= 1
            
        except ValueError:
            print("Пожалуйста, введите корректное число или команду (restart/exit/выход/выйти).")
    
    if attempts_left == 0:
        print(f"К сожалению, вы проиграли. Загаданное число было {secret_number}.")
    
    play_again = input("Хотите сыграть ещё раз? (да/нет): ").lower()
    if play_again in ['да', 'д', 'yes', 'y']:
        play_game()
    else:
        print("Спасибо за игру! До новых встреч!")

play_game()
