using UnityEngine;
using UnityEngine.InputSystem; // Required for the new Input System

public class PlayerAim : MonoBehaviour
{
    private Camera mainCam;
    private Vector2 aimInput = Vector2.zero;

    void Start()
    {
        mainCam = Camera.main;
    }

    // This method is called by the Input System when the mouse position changes.
    public void OnAim(InputValue value)
    {
        aimInput = value.Get<Vector2>();
    }

    void Update()
    {
        // Convert the mouse's screen position to a world position
        Vector3 mouseWorldPos = mainCam.ScreenToWorldPoint(new Vector3(aimInput.x, aimInput.y, mainCam.nearClipPlane));

        // Calculate the direction from the player to the mouse
        Vector2 direction = mouseWorldPos - transform.position;

        // Calculate the angle and rotate the player. The -90f is an offset to make sure the 'up' of the sprite points at the cursor.
        float angle = Mathf.Atan2(direction.y, direction.x) * Mathf.Rad2Deg - 90f;
        transform.rotation = Quaternion.Euler(0, 0, angle);
    }
}
