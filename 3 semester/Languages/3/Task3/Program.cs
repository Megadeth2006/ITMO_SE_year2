Console.WriteLine("СИСТЕМА АВТОБАТТЛЕРА");


Hero warrior = new Warrior("Воин", 12, 6, 25);
Hero wizard = new Wizard("Маг");

warrior.Artifact = new HealingPotion(30);
wizard.Artifact = new AttackBoost(20);

ConsoleUtils.Logger("Созданные персонажи:", ConsoleColor.Cyan);
ConsoleUtils.Logger($"{warrior}", ConsoleColor.White);
ConsoleUtils.Logger($"{wizard}", ConsoleColor.White);


ConsoleUtils.Logger("\n ДЕМОНСТРАЦИЯ АРТЕФАКТОВ ", ConsoleColor.Magenta);
warrior.UseArtifact();
wizard.UseArtifact();

ConsoleUtils.Logger("\nСостояние после использования артефактов:", ConsoleColor.Cyan);
ConsoleUtils.Logger($"{warrior}", ConsoleColor.White);
ConsoleUtils.Logger($"{wizard}", ConsoleColor.White);



ConsoleUtils.Logger("\n НАЧАЛО БИТВЫ ", ConsoleColor.Red);
AutoBattler battler = new AutoBattler(warrior, wizard);
battler.StartBattle();

// 1. Написать класс Wizard отнаследованный от Hero
// 1.5 Характеристики случайные.
// 2. Реализовать SpecialAbility (игнорирование защиты например)
// 3. Сделать метод(класс) AutoBattler 
// 4. Бесконечная битва (достаточно двух персонажей)
//     пока у кого-то не будет HP <= 0
// 5. Каждый ход атакует случайный персонаж (реализовать метод атаки)
// 6. Раз в три хода используется SpecialAbility
// 7. Цветной вывод в консоль о ходе битвы
// 8. Вывод хода битвы в файл
// 9*. Использование звука.
// 10*. Использование артифактов.
