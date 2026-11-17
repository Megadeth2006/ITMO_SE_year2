public static class ConsoleUtils
{
    public static void Logger(string log, ConsoleColor color)
    {
        Console.ForegroundColor = color;
        Console.WriteLine(log);
        Console.ResetColor();
    }

    public static void Beep()
    {
        Console.Beep();
    }

    public static void PlayAttackSound()
    {
     
        Console.Beep(800, 200);
        Thread.Sleep(50);
        Console.Beep(600, 150);
    }

    public static void PlaySpecialAbilitySound()
    {
        Console.Beep(1000, 150);
        Thread.Sleep(100);
        Console.Beep(1200, 150);
        Thread.Sleep(100);
        Console.Beep(800, 200);
    }

    public static void PlayVictorySound()
    {
        Console.Beep(523, 200); 
        Console.Beep(659, 200); 
        Console.Beep(784, 200); 
        Console.Beep(1047, 400); 
    }

    public static void PlayDefeatSound()
    {
        Console.Beep(1047, 200); 
        Console.Beep(784, 200); 
        Console.Beep(659, 200); 
        Console.Beep(523, 400);
    }

    public static void PlayArtifactSound()
    {
        Console.Beep(880, 100); 
        Console.Beep(1109, 100); 
        Console.Beep(1319, 200);
    }

    public static void PlayCriticalHitSound()
    {
        Console.Beep(1200, 100);
        Console.Beep(1400, 100);
        Console.Beep(1600, 150);
    }
}