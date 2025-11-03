using UnityEngine;
using System; // Required for the Action delegate

public class PlayerStats : MonoBehaviour
{
    [Header("Health")]
    public float maxHealth = 200f;
    // Use a public getter but a private setter to control modifications from other scripts
    public float currentHealth { get; private set; }
    public bool isInvulnerable { get; private set; } = false;

    [Header("Energy")]
    public float maxEnergy = 200f;
    public float currentEnergy { get; private set; }

    // Events that other scripts (like a UI Manager) can subscribe to.
    // They will pass the current and max values for easy UI updates.
    public event Action<float, float> OnHealthChanged;
    public event Action<float, float> OnEnergyChanged;

    private void Awake()
    {
        // Initialize health and energy when the game starts
        currentHealth = maxHealth;
        currentEnergy = maxEnergy;
    }

    // Public method to apply damage
    public void TakeDamage(float amount)
    {
        // Ignore damage if the player is currently invulnerable
        if (isInvulnerable) return;
        if (amount < 0) return; // Damage should be positive

        currentHealth -= amount;
        if (currentHealth < 0)
        {
            currentHealth = 0;
        }

        // Fire the event to notify listeners of the change
        OnHealthChanged?.Invoke(currentHealth, maxHealth);

        if (currentHealth <= 0)
        {
            Die();
        }
    }

    // Public method to restore health
    public void Heal(float amount)
    {
        if (amount < 0) return;

        currentHealth += amount;
        if (currentHealth > maxHealth)
        {
            currentHealth = maxHealth;
        }
        OnHealthChanged?.Invoke(currentHealth, maxHealth);
    }

    // Public method to allow other scripts to make the player invulnerable
    public void SetInvulnerable(bool status)
    {
        isInvulnerable = status;
    }

    // Public method to try and spend energy
    public bool UseEnergy(float amount)
    {
        if (amount < 0) return false;

        if (currentEnergy >= amount)
        {
            currentEnergy -= amount;
            OnEnergyChanged?.Invoke(currentEnergy, maxEnergy);
            return true; // Success
        }

        return false; // Not enough energy
    }

    // Public method to restore energy
    public void RestoreEnergy(float amount)
    {
        if (amount < 0) return;

        currentEnergy += amount;
        if (currentEnergy > maxEnergy)
        {
            currentEnergy = maxEnergy;
        }
        OnEnergyChanged?.Invoke(currentEnergy, maxEnergy);
    }

    private void Die()
    {
        // For now, we'll just log a message. Later, this could trigger a game over screen.
        Debug.Log("Player has been defeated.");
        // You could disable player controls here, for example.
        // GetComponent<PlayerMovement>().enabled = false;
    }
}
