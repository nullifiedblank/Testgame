using UnityEngine;

[RequireComponent(typeof(Rigidbody2D), typeof(Collider2D))]
public class Projectile : MonoBehaviour
{
    [Header("Projectile Settings")]
    public float speed = 20f;
    public float damage = 10f;
    public float maxLifetime = 5f; // Time in seconds before the projectile is destroyed

    private Rigidbody2D rb;

    private void Awake()
    {
        rb = GetComponent<Rigidbody2D>();
        // Ensure the collider is set to be a trigger so it doesn't physically push objects
        GetComponent<Collider2D>().isTrigger = true;
    }

    private void Start()
    {
        // Give the projectile an initial velocity in its "forward" direction.
        // As before, this is transform.up because it inherits the player's rotation.
        rb.velocity = transform.up * speed;

        // Destroy the projectile automatically after its lifetime expires to prevent it from flying forever.
        Destroy(gameObject, maxLifetime);
    }

    // This function is called by Unity when this object's trigger collider overlaps with another one.
    private void OnTriggerEnter2D(Collider2D other)
    {
        // We will need to create these tags in the Unity Editor later.

        // Check if the projectile hit a solid terrain object
        if (other.CompareTag("Terrain"))
        {
            // Destroy the projectile immediately
            Destroy(gameObject);
            return; // Stop further checks
        }

        // Check if the projectile hit an object with a Health component (e.g., an enemy)
        // We will need to create a simple Health script for enemies later.
        // For now, this code anticipates that.
        /*
        Health targetHealth = other.GetComponent<Health>();
        if (targetHealth != null)
        {
            targetHealth.TakeDamage(damage);

            // Destroy the projectile so it can't hit multiple targets (piercing would be a separate feature)
            Destroy(gameObject);
            return;
        }
        */

        // Placeholder for when we add enemies
        if (other.CompareTag("Enemy"))
        {
            Debug.Log("Hit an enemy for " + damage + " damage!");
            Destroy(gameObject);
            return;
        }
    }
}
