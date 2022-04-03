# Game-of-life
Игру «Жизнь» изобрел математик Джон Хортон Конвей в 1970 году. Она пользовалась популярностью не только среди его коллег. Об увлекательности игры «Жизнь» свидетельствуют результаты множества интересных исследований и многочисленные компьютерные реализации. При этом она имеет непосредственное отношение к перспективной области математики - теории клеточных автоматов.

Правила игры
«Жизнь» разыгрывается на бесконечном клеточном поле.
У каждой клетки 8 соседних клеток.
В каждой клетке может жить существо.
Существо с двумя или тремя соседями выживает в следующем поколении, иначе погибает от одиночества или перенаселённости.
В пустой клетке с тремя соседями в следующем поколении рождается существо [1].
Реализация
Для реализации клеточного поля был использован набор модулей pygame, предназначенный для создания компьютерных игр.
