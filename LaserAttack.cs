using UnityEngine;

[RequireComponent(typeof(LineRenderer))]
public class LaserAttack : MonoBehaviour
{
    [Header("Laser Settings")]
    public float damagePerSecond = 20f;
    public float energyCostPerSecond = 30f;
    public float maxRange = 15f;
    public LayerMask hitLayers; // Define which layers the laser can hit (e.g., "Enemies", "Terrain")

    private LineRenderer lineRenderer;
    private PlayerStats playerStats;

    // We store this to apply damage only once per second, not every frame
    private float damageTimer = 0f;
    private Health targetHealth; // The health component of the currently targeted enemy

    public void Initialize(PlayerStats stats)
    {
        playerStats = stats;
        lineRenderer = GetComponent<LineRenderer>();
        lineRenderer.useWorldSpace = true;
    }

    public void UpdateLaser(Vector3 startPoint, Vector3 direction)
    {
        if (playerStats == null) return;

        // Try to use energy. If we can't, disable the laser and exit.
        if (!playerStats.UseEnergy(energyCostPerSecond * Time.deltaTime))
        {
            gameObject.SetActive(false);
            return;
        }

        // Set the laser's start point
        lineRenderer.SetPosition(0, startPoint);

        RaycastHit2D hit = Physics2D.Raycast(startPoint, direction, maxRange, hitLayers);

        if (hit.collider != null)
        {
            // If we hit something, set the laser's end point to the hit location
            lineRenderer.SetPosition(1, hit.point);

            // --- DAMAGE LOGIC ---
            Health newTarget = hit.collider.GetComponent<Health>();
            if (newTarget != targetHealth)
            {
                // If we hit a new target, reset the damage timer
                targetHealth = newTarget;
                damageTimer = 0f;
            }

            if (targetHealth != null)
            {
                damageTimer += Time.deltaTime;
                if (damageTimer >= 1f)
                {
                    targetHealth.TakeDamage(damagePerSecond);
                    damageTimer = 0f; // Reset for the next second
                }
            }
        }
        else
        {
            // If we hit nothing, extend the laser to its maximum range
            lineRenderer.SetPosition(1, startPoint + direction * maxRange);
            targetHealth = null; // We are no longer hitting a target
        }
    }
}
// Note: This script requires a "Health" component on enemies to work.
// I will create a placeholder "Health.cs" script in the next step.
