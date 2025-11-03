using UnityEngine;
using UnityEngine.UI; // Required for UI components like Slider

public class UIManager : MonoBehaviour
{
    [Header("UI Sliders")]
    public Slider healthSlider;
    public Slider energySlider;

    [Header("Player Reference")]
    // We can assign this in the Inspector to avoid searching for it
    public PlayerStats playerStats;

    private void Start()
    {
        // If the playerStats reference isn't set in the Inspector, try to find it.
        if (playerStats == null)
        {
            playerStats = FindObjectOfType<PlayerStats>();
        }

        // Subscribe our UI update methods to the events in PlayerStats
        if (playerStats != null)
        {
            playerStats.OnHealthChanged += UpdateHealthUI;
            playerStats.OnEnergyChanged += UpdateEnergyUI;

            // Call the methods once at the start to set the initial UI values
            UpdateHealthUI(playerStats.currentHealth, playerStats.maxHealth);
            UpdateEnergyUI(playerStats.currentEnergy, playerStats.maxEnergy);
        }
        else
        {
            Debug.LogError("UIManager could not find the PlayerStats component in the scene!");
        }
    }

    // This method will be called automatically whenever the health changes
    private void UpdateHealthUI(float currentHealth, float maxHealth)
    {
        if (healthSlider != null)
        {
            // The slider's value is a ratio from 0 to 1, so we divide current by max.
            healthSlider.value = currentHealth / maxHealth;
        }
    }

    // This method will be called automatically whenever the energy changes
    private void UpdateEnergyUI(float currentEnergy, float maxEnergy)
    {
        if (energySlider != null)
        {
            energySlider.value = currentEnergy / maxEnergy;
        }
    }

    // It's good practice to unsubscribe from events when the object is destroyed
    private void OnDestroy()
    {
        if (playerStats != null)
        {
            playerStats.OnHealthChanged -= UpdateHealthUI;
            playerStats.OnEnergyChanged -= UpdateEnergyUI;
        }
    }
}
