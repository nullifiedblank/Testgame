using UnityEngine;

public class PlayerAttack : MonoBehaviour
{
    public GameObject attackPrefab;
    public float attackCooldown = 0.5f;
    public float attackOffset = 1.0f;

    private float lastAttackTime = -999f;

    void Update()
    {
        if (Time.time >= lastAttackTime + attackCooldown)
        {
            if (Input.GetMouseButtonDown(0)) // 0 is for the left mouse button
            {
                Attack();
                lastAttackTime = Time.time;
            }
        }
    }

    void Attack()
    {
        // Calculate the position to spawn the attack, right in front of the player.
        // We use transform.up because the player is rotated to face the mouse,
        // so its "up" vector points forward.
        Vector3 spawnPosition = transform.position + transform.up * attackOffset;

        // Create the attack object at the calculated position and with the same rotation as the player.
        Instantiate(attackPrefab, spawnPosition, transform.rotation);
    }
}
