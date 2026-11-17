public class AutoBattler
{
    private Hero hero1;
    private Hero hero2;
    private int turnCount;
    private Random random;
    private string logFilePath;

    public AutoBattler(Hero firstHero, Hero secondHero)
    {
        hero1 = firstHero;
        hero2 = secondHero;
        turnCount = 0;
        random = new Random();
        logFilePath = Path.Combine(Environment.CurrentDirectory, "log.txt");
        
        // Очищаем файл лога при создании нового боя
        File.WriteAllText(logFilePath, $" НОВЫЙ БОЙ \n{DateTime.Now}\n\n");
    }

    public void StartBattle()
    {
        ConsoleUtils.Logger(" НАЧАЛО БИТВЫ ", ConsoleColor.Yellow);
        LogToFile(" НАЧАЛО БИТВЫ ");
        
        ConsoleUtils.Logger($"Участники:", ConsoleColor.Cyan);
        ConsoleUtils.Logger($"{hero1}", ConsoleColor.White);
        ConsoleUtils.Logger($"{hero2}", ConsoleColor.White);
        LogToFile($"Участники: {hero1} vs {hero2}");

        while (hero1.HP > 0 && hero2.HP > 0)
        {
            turnCount++;
            ConsoleUtils.Logger($"\nХОД {turnCount}", ConsoleColor.Magenta);
            LogToFile($"\nХОД {turnCount} ");

            // Случайно выбираем кто атакует
            Hero attacker = random.Next(2) == 0 ? hero1 : hero2;
            Hero target = attacker == hero1 ? hero2 : hero1;

            PerformTurn(attacker, target);

           
            Thread.Sleep(2000);
        }

        // Определяем победителя
        Hero winner = hero1.HP > 0 ? hero1 : hero2;
        Hero loser = hero1.HP > 0 ? hero2 : hero1;

        ConsoleUtils.Logger($"\n БИТВА ЗАВЕРШЕНА ", ConsoleColor.Red);
        ConsoleUtils.Logger($"ПОБЕДИТЕЛЬ: {winner.Name} (HP: {winner.HP})", ConsoleColor.Green);
        ConsoleUtils.Logger($"ПРОИГРАВШИЙ: {loser.Name} (HP: {loser.HP})", ConsoleColor.Red);
        
        LogToFile($"\n БИТВА ЗАВЕРШЕНА ");
        LogToFile($"ПОБЕДИТЕЛЬ: {winner.Name} (HP: {winner.HP})");
        LogToFile($"ПРОИГРАВШИЙ: {loser.Name} (HP: {loser.HP})");

        // Звуки победы и поражения
        ConsoleUtils.PlayVictorySound();
        Thread.Sleep(2000);
        ConsoleUtils.PlayDefeatSound();
    }

    private void PerformTurn(Hero attacker, Hero target)
    {
        ConsoleUtils.Logger($"{attacker.Name} атакует {target.Name}!", ConsoleColor.Red);
        LogToFile($"{attacker.Name} атакует {target.Name}!");

        // Проверяем, нужно ли использовать SpecialAbility (раз в три хода)
        if (turnCount % 3 == 0)
        {
            ConsoleUtils.Logger($"{attacker.Name} использует специальную способность!", ConsoleColor.Yellow);
            LogToFile($"{attacker.Name} использует специальную способность!");
            attacker.SpecialAbility(target);
            ConsoleUtils.PlaySpecialAbilitySound(); 
        }
        else
        {
            // Обычная атака
            int damage = attacker.Attack;
            target.TakeDamage(damage);
            ConsoleUtils.Logger($"Нанесено урона: {damage}", ConsoleColor.White);
            LogToFile($"Нанесено урона: {damage}");
            ConsoleUtils.PlayAttackSound(); 
        }

        // Показываем состояние после атаки
        ConsoleUtils.Logger($"Состояние после атаки:", ConsoleColor.Cyan);
        ConsoleUtils.Logger($"{hero1}", ConsoleColor.White);
        ConsoleUtils.Logger($"{hero2}", ConsoleColor.White);
        LogToFile($"Состояние: {hero1} | {hero2}");
    }

    private void LogToFile(string message)
    {
        File.AppendAllText(logFilePath, $"{DateTime.Now:HH:mm:ss} - {message}\n");
    }
}
