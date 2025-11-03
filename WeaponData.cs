using UnityEngine;

// This attribute allows you to create instances of this object from the Assets menu in Unity.
[CreateAssetMenu(fileName = "New Weapon", menuName = "Game/Weapon Data")]
// An enumeration to define the different ways a weapon can behave.
public enum AttackType { Melee, Ranged, Laser }

public class WeaponData : ScriptableObject
{
    [Header("Weapon Type")]
    public AttackType attackType = AttackType.Melee;

    [Header("Weapon Stats")]
    // The time between attacks in a combo
    public float attackCooldown = 0.5f;

    // The time before the combo sequence resets
    public float comboResetTime = 0.7f;

    // How far in front of the player the attack spawns
    public float attackOffset = 1.0f;

    [Header("Combo Attacks")]
    // The array of prefabs for each attack in the combo sequence
    public GameObject[] attackPrefabs;
}
