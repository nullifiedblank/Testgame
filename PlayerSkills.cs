using System.Collections;
using UnityEngine;
using UnityEngine.InputSystem;

[RequireComponent(typeof(Rigidbody2D), typeof(PlayerStats))]
public class PlayerSkills : MonoBehaviour
{
    [Header("Dash Skill Settings")]
    public float dashSpeed = 20f;
    public float dashDuration = 0.15f;
    public float dashCooldown = 4f;
    public float dashEnergyCost = 15f;

    private Rigidbody2D rb;
    private PlayerStats playerStats;

    private float lastDashTime = -999f;
    private bool isDashing = false;

    private void Awake()
    {
        rb = GetComponent<Rigidbody2D>();
        playerStats = GetComponent<PlayerStats>();
    }

    // This method is called by the Input System when the "Skill1" action is performed
    public void OnDash(InputValue value)
    {
        // Check if the skill is off cooldown, the player has enough energy, and is not already dashing
        if (Time.time >= lastDashTime + dashCooldown && !isDashing)
        {
            if (playerStats.UseEnergy(dashEnergyCost))
            {
                StartCoroutine(PerformDash());
                lastDashTime = Time.time;
            }
        }
    }

    private IEnumerator PerformDash()
    {
        isDashing = true;
        playerStats.SetInvulnerable(true); // Make the player untargetable

        // The player's "forward" direction is transform.up because we rotate it to face the mouse
        Vector2 dashDirection = transform.up;
        rb.velocity = dashDirection * dashSpeed;

        // Wait for the dash duration
        yield return new WaitForSeconds(dashDuration);

        rb.velocity = Vector2.zero; // Stop the dash
        playerStats.SetInvulnerable(false); // Make the player targetable again
        isDashing = false;
    }
}
