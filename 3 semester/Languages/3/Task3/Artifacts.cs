// Артефакт лечения
public class HealingPotion : IArtifact
{
    private int healingAmount;

    public HealingPotion(int healing = 25)
    {
        healingAmount = healing;
    }

    public void Use(Hero hero)
    {
        int oldHP = hero.HP;
        hero.HP += healingAmount;
        int actualHealing = hero.HP - oldHP;
        
        ConsoleUtils.Logger($"{hero.Name} использовал зелье лечения! +{actualHealing} HP", ConsoleColor.Green);
        ConsoleUtils.PlayArtifactSound();
    }
}

// Артефакт увеличения атаки
public class AttackBoost : IArtifact
{
    private int attackBonus;

    public AttackBoost(int bonus = 15)
    {
        attackBonus = bonus;
    }

    public void Use(Hero hero)
    {
        hero.Attack += attackBonus;
        ConsoleUtils.Logger($"{hero.Name} получил усиление атаки! +{attackBonus} атаки", ConsoleColor.Yellow);
        ConsoleUtils.PlayArtifactSound();
    }
}

// Артефакт увеличения защиты
public class DefenseBoost : IArtifact
{
    private int defenseBonus;

    public DefenseBoost(int bonus = 10)
    {
        defenseBonus = bonus;
    }

    public void Use(Hero hero)
    {
        hero.Defense += defenseBonus;
        ConsoleUtils.Logger($"{hero.Name} получил усиление защиты! +{defenseBonus} защиты", ConsoleColor.Blue);
        ConsoleUtils.PlayArtifactSound();
    }
}

