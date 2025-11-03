using UnityEngine;

public class DestroyAfterTime : MonoBehaviour
{
    // The amount of time in seconds before the object is destroyed.
    public float lifetime = 0.25f;

    void Start()
    {
        // Tell Unity to destroy this GameObject after 'lifetime' seconds.
        Destroy(gameObject, lifetime);
    }
}
