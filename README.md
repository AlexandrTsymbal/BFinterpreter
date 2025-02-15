# Интерпретатор BEFUNGE #

## Что это? ##

Класс Interpreter, на вход в конструктор, которого передается имя файла с кодом на языке Befunge, который этот класс исполняет

----------

## Использование ##


_Импортирование класса:_

    from Interpreter import Interpreter

_Исполнение Befunge кода:_

    Interpreter("example.bf")

_Пример оконачания работы:_

    Кончился стек или вышли за поле

## Быстрая справка ##
 Символ           | Описание                                                                       
 ---------------------|----------------------------------------------------------------------------------- 
`0-9`               | Поместить это число в стек                                                     
`+`                 | Извлечь `a` и `b` из стека, затем поместить `a+b`.                                                 
`-`                 | Извлечь `a` и `b` из стека, затем поместить `a-b`.                                                 
`*`                 | Извлечь `a` и `b` из стека, затем поместить `a*b`.                                                 
`/`                 | Извлечь `a` и `b` из стека, затем поместить `floor(b/a)`, при условии, что `a` не равно нулю.           
`%`                 | Извлечь `a` и `b` из стека, затем поместить `a (mod b)`.                                           
`!`                 | Извлечь `a`. Если `a = 0`, поместить 1, в противном случае поместить 0.                                    
`'`                 | Извлечь `a` и `b` из стека, затем поместить 1, если `b > a`, в противном случае 0.                             
`>`                 | Переместить вправо.                                                                       
`<`                 | Переместить влево.                                                                        
`^`                 | Переместить вверх.            Character           | Description                                                                       
`v`                 | Переместить вниз.                                                                        
`?`                 | Переместить в случайном направлении.                                                       
`_`                 | Извлечь `a`. Если `a = 0`, переместить вправо, в противном случае переместить влево.                             
`\|`                 | Извлечь `a`. Если `a = 0`, переместить вниз, в противном случае переместить вверх.                               
`"`                 | Начать режим строки. Поместить ASCII-значение каждого символа до следующего ". 
`:`                 | Дублировать значение на вершине стека.                                              
`\\`                 | Поменять местами два значения на вершине стека.                                          
`$`                 | Удалить значение на вершине стека.                                             
`.`                 | Извлечь `a`. Вывести целочисленное значение `a`.                                         
`,`                 | Извлечь `a`. Вывести `chr(a)`.                                                         
`#`                 | Пропустить следующую ячейку.                                                                   
`p`                 | Извлечь `y`, `x` и `v`. Изменить символ в позиции `(x,y)` на `chr(v)`.       
`g`                 | Извлечь `y` и `x`, затем поместить ASCII-значение символа в позиции `(x,y)`.  
`&`                 | Запросить пользователя число и поместить его в стек.                                             
`~`                 | Запросить пользователя символ и поместить его ASCII-значение в стек.                             
`@`                 | Остановить указатель инструкции.                                                          

----------

## Developer ##

Telegram: [_**Sanchezzzz300**_](https://t.me/sanchezzzz300) 