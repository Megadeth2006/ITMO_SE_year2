using System.Reflection.Emit;


namespace part01 {
    [GameAttribute]
    public class MyMechanics {

        [CombatSkill("Pokemon", TriggerType.OnDefense, 20)]
        public void ExecuteOnDefense(BattleContext ctx) {
            var dynamicMethod = new DynamicMethod("DecreaseDamage", typeof(int), new[] {typeof(int)});
            ILGenerator il = dynamicMethod.GetILGenerator();
            il.Emit(OpCodes.Ldarg_0);
            il.Emit(OpCodes.Ldc_I4, 2);
            il.Emit(OpCodes.Div);
            il.Emit(OpCodes.Ret);

            var myDelegate = (Func<int, int>)dynamicMethod.CreateDelegate(typeof(Func<int, int>));
            ctx.DamageDealt = myDelegate(ctx.DamageDealt);
        }

        [CombatSkill("Butterfree", TriggerType.PostBattle, 50)]
        public void ExecutePostBattle(BattleContext ctx) {
            
            var dynamicMethod = new DynamicMethod("DecreaseHP", typeof(int), new[] {typeof(int)});
            ILGenerator il = dynamicMethod.GetILGenerator();
            il.Emit(OpCodes.Ldarg_0);
            il.Emit(OpCodes.Ldc_I4, 20);
            il.Emit(OpCodes.Sub);
            il.Emit(OpCodes.Ret);
            var myDelegate = (Func<int, int>)dynamicMethod.CreateDelegate(typeof(Func<int, int>));
            ctx.Attacker.Hp = myDelegate(ctx.Attacker.Hp);
            ctx.Defender.Hp = myDelegate(ctx.Defender.Hp);


        }

    }


}
