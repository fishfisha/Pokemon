from random import randint
import requests
from datetime import datetime, timedelta

class Pokemon:
    pokemons = {}
    # Инициализация объекта (конструктор)
    def __init__(self, pokemon_trainer):

        self.pokemon_trainer = pokemon_trainer

        self.pokemon_number = randint(1,1000)
        self.img = self.get_img()
        self.name = self.get_name()

        self.power = randint(30,40)
        self.hp = randint(200,400)

        Pokemon.pokemons[pokemon_trainer] = self

    # Метод для получения картинки покемона через API
    def get_img(self): 
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return (data['sprites']['other']['official-artwork']['front_default'])
        else:
            return "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/1.png"

    # Метод для получения имени покемона через API
    def get_name(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return (data['forms'][0]['name'])
        else:
            return "Pikachu"    
 

    # Метод класса для получения информации
    def info(self):
        return f"""имя твоего покеомона: {self.name}
        сила покемона: {self.power}
        здоровье покемона: {self.hp}"""

    # Метод класса для получения картинки покемона
    def show_img(self):
        return self.img
    

    def feed(self, feed_interval = 20, hp_increase = 10 ):
        current_time = datetime.now()
        delta_time = timedelta(seconds=feed_interval)
        if (current_time - self.last_feed_time) > delta_time:
            self.hp += hp_increase
            self.last_feed_time = current_time
            return f"здоровье покемона увеличено! текущее здоровье: {self.hp}"
        else:
            return f"следующее время кормления покемона: {self.last_feed_time+delta_time}"



    def attack(self, enemy):
        if isinstance(enemy, Wizard): # Проверка на то, что enemy является типом данных Wizard (является экземпляром класса Волшебник)
            chance = randint(1,5)
            if chance == 1:
                return "покемон-волшебник применил щит в сражении"
        
        if enemy.hp > self.power:
            enemy.hp -= self.power
            return f"сражение @{self.pokemon_trainer} с @{enemy.pokemon_trainer}"
        else:
            enemy.hp = 0
            return f"победа @{self.pokemon_trainer} над @{enemy.pokemon_trainer}! "


class Wizard(Pokemon):
    def info(self):
        return "у тебя покемон - волшебник! \n\n" + super().info()

    def feed(self):
        return super().feed(feed_interval= 10)

class Fighter (Pokemon):
    def attack(self, enemy):
        super_power = randint(5,15)
        self.power += super_power
        result = super().attack(enemy)
        self.power -= super_power
        return result + f"\nбоец применил супер-атаку силой:{super_power} "

    def info(self):
            return "у тебя покемон - боец! \n\n" + super().info()
    
    def feed(self):
        return super().feed(feed_interval= 25)


if __name__ == '__main__':
    wizard = Wizard("username1")
    fighter = Fighter("username2")

    print(wizard.info())
    print()
    print(fighter.info())
    print()
    print(fighter.attack(wizard))
