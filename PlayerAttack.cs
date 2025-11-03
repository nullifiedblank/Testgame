using UnityEngine;
using UnityEngine.InputSystem;

public class PlayerAttack : MonoBehaviour
{
    public WeaponData currentWeapon;
    private PlayerStats playerStats;

    // --- MELEE/RANGED VARS ---
    private int comboCounter = 0;
    private float lastAttackTime = -999f;

    // --- LASER VARS ---
    private bool isLaserActive = false;
    private LaserAttack activeLaser;

    private void Awake()
    {
        playerStats = GetComponent<PlayerStats>();
    }

    // This is called by the Input System. It now has different behavior based on the weapon.
    public void OnAttack(InputValue value)
    {
        if (currentWeapon == null) return;

        if (currentWeapon.attackType == AttackType.Laser)
        {
            // For lasers, the button press toggles the beam on and off.
            isLaserActive = value.isPressed;
        }
        else // For Melee and Ranged weapons
        {
            // Only trigger on the "press down" action
            if (value.isPressed)
            {
                // Check cooldown from the last attack
                if (Time.time >= lastAttackTime + currentWeapon.attackCooldown)
                {
                    // Check for combo reset
                    if (Time.time > lastAttackTime + currentWeapon.comboResetTime)
                    {
                        comboCounter = 0;
                    }

                    PerformMeleeOrRangedAttack();
                    lastAttackTime = Time.time;
                }
            }
        }
    }

    private void Update()
    {
        // The laser is a continuous attack that needs to be updated every frame.
        if (currentWeapon != null && currentWeapon.attackType == AttackType.Laser)
        {
            HandleLaserAttack();
        }
    }

    private void HandleLaserAttack()
    {
        // The first prefab in a laser weapon's list is the laser beam itself.
        GameObject laserPrefab = currentWeapon.attackPrefabs[0];
        if (laserPrefab == null) return;

        if (isLaserActive && activeLaser == null)
        {
            // If the player wants to fire and there's no active laser, create one.
            GameObject laserInstance = Instantiate(laserPrefab, transform.position, transform.rotation);
            activeLaser = laserInstance.GetComponent<LaserAttack>();
            activeLaser.Initialize(playerStats);
        }
        else if (!isLaserActive && activeLaser != null)
        {
            // If the player stops firing, destroy the laser.
            Destroy(activeLaser.gameObject);
            activeLaser = null;
        }

        if (activeLaser != null)
        {
            // If the laser is active, update its position and direction.
            activeLaser.UpdateLaser(transform.position, transform.up);
        }
    }

    private void PerformMeleeOrRangedAttack()
    {
        if (currentWeapon.attackPrefabs == null || currentWeapon.attackPrefabs.Length == 0) return;

        if (currentWeapon.attackType == AttackType.Ranged)
        {
            // Fire the prefab as a projectile
            Instantiate(currentWeapon.attackPrefabs[comboCounter], transform.position, transform.rotation);
        }
        else // Melee
        {
            // Spawn the attack visual in front of the player
            Vector3 spawnPosition = transform.position + transform.up * currentWeapon.attackOffset;
            Instantiate(currentWeapon.attackPrefabs[comboCounter], spawnPosition, transform.rotation);
        }

        // Advance the combo counter for the next attack
        comboCounter++;
        if (comboCounter >= currentWeapon.attackPrefabs.Length)
        {
            comboCounter = 0;
        }
    }
}
