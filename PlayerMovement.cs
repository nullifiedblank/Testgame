using UnityEngine;
using UnityEngine.InputSystem; // Required for the new Input System

public class PlayerMovement : MonoBehaviour
{
    public float speed = 5f;
    private Rigidbody2D rb;
    private Vector2 moveInput = Vector2.zero;

    void Start()
    {
        rb = GetComponent<Rigidbody2D>();
    }

    // The new Input System can call this method directly when the "Move" action is triggered.
    // This is more efficient than checking for input every frame in Update().
    public void OnMove(InputValue value)
    {
        moveInput = value.Get<Vector2>();
    }

    // We use FixedUpdate for physics calculations to ensure smooth and consistent movement.
    void FixedUpdate()
    {
        rb.velocity = moveInput * speed;
    }
}
