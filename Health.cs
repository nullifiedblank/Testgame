using UnityEngine;
using System;

public class Health : MonoBehaviour
{
    public float maxHealth = 50f;
    public float currentHealth { get; private set; }

    public event Action OnDeath;

    private void Awake()
    {
        currentHealth = maxHealth;
    }

    public void TakeDamage(float amount)
    {
        if (amount < 0) return;

        currentHealth -= amount;
        if (currentHealth <= 0)
        {
            currentHealth = 0;
            Die();
        }
    }

    private void Die()
    {
        // Fire the event to notify other components that this object has died
        OnDeath?.Invoke();

        // For now, we'll just destroy the object.
        // A more advanced system might play an animation or spawn loot first.
        Destroy(gameObject);
    }
}
