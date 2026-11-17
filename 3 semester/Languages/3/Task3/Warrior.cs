public class Warrior : Hero
{
    public Warrior(string name, int attack, int defense, int hp) :
        base(name, attack, defense, hp)
    {

    }

    public override void UseArtifact()
    {
        if (Artifact != null)
        {
            Artifact.Use(this);
        }
    }

    public override void SpecialAbility(Hero target)
    {
        target.TakeDamage(2 * this.Attack);
    }
}