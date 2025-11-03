using UnityEngine;

public class PlayerAttack : MonoBehaviour
{
    // A slot to hold the currently equipped weapon's data.
    public WeaponData currentWeapon;

    private int comboCounter = 0;
    private float lastAttackTime = -999f;

    void Update()
    {
        // First, make sure a weapon is equipped.
        if (currentWeapon == null)
        {
            return; // Do nothing if there's no weapon.
        }

        // Check for the left mouse click.
        if (Input.GetMouseButtonDown(0))
        {
            // Check if the attack is off cooldown.
            if (Time.time >= lastAttackTime + currentWeapon.attackCooldown)
            {
                // If too much time has passed since the last attack, reset the combo.
                if (Time.time > lastAttackTime + currentWeapon.comboResetTime)
                {
                    comboCounter = 0;
                }

                Attack();
                lastAttackTime = Time.time;
            }
        }
    }

    void Attack()
    {
        // Make sure the weapon has attack prefabs assigned.
        if (currentWeapon.attackPrefabs == null || currentWeapon.attackPrefabs.Length == 0)
        {
            Debug.LogError("The current weapon has no attack prefabs assigned!");
            return;
        }

        // Calculate spawn position using the offset from the weapon data.
        Vector3 spawnPosition = transform.position + transform.up * currentWeapon.attackOffset;

        // Instantiate the correct prefab based on the combo count.
        Instantiate(currentWeapon.attackPrefabs[comboCounter], spawnPosition, transform.rotation);

        // Advance the combo counter.
        comboCounter++;

        // If the combo has reached the end, loop back to the start.
        if (comboCounter >= currentWeapon.attackPrefabs.Length)
        {
            comboCounter = 0;
        }
    }
}
