public class Wizard : Hero
{
    public Wizard(string name) : base(name, 0, 0, 0)
    {
        // Случайные характеристики
        var random = new Random();
        Attack = random.Next(1, 31);       
        Defense = random.Next(1, 41);      
        HP = random.Next(30, 101);         
    }

    public override void SpecialAbility(Hero target)
    {
        // Игнорирование защиты - атака проходит полностью
        int damage = Attack;
        target.TakeDamageIgnoringDefense(damage);
    }

    public override void UseArtifact()
    {
        if (Artifact != null)
        {
            Artifact.Use(this);
        }
    }
}

