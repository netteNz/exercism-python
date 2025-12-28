Here is your study guide for the **Lasagna** exercise.

### 1. Exercise Breakdown
**Goal:** Create a class to manage cooking timings for a lasagna.
**Core Logic:** You need to implement 4 methods that perform basic arithmetic calculations based on fixed rules (e.g., 2 minutes per layer) or inputs (e.g., how long it's been in the oven).

### 2. Test Analysis
The tests in `LasagnaTest.java` enforce the following strict rules:
*   **Signature Compliance:** Methods must be named exactly as specified (`expectedMinutesInOven`, etc.), be `public`, and return `int`.
*   **Logic Verification:**
    *   `expectedMinutesInOven`: Must always return `40`.
    *   `remainingMinutesInOven(25)`: Must return `15` (40 - 25).
    *   `preparationTimeInMinutes(1)`: Must return `2` (1 layer * 2 mins).
    *   `totalTimeInMinutes(3, 20)`: Must return `26` (3 layers * 2 mins + 20 mins in oven).

### 3. Key Concepts & Patterns
*   **Method Anatomy:** `access_modifier return_type method_name(parameter_type parameter_name) { ... }`
*   **Primitives:** Using `int` for integer mathematics.
*   **Scope:** Variables defined inside a method are local to that method.
*   **Composition:** `totalTimeInMinutes` conceptually combines logic from the other methods.

### 4. Edge Cases & Complexity
*   **Edge Cases:**
    *   *Negative inputs:* technically possible (e.g., -5 layers), but for this specific exercise, you can assume valid positive integers.
    *   *Zero inputs:* 0 layers means 0 preparation time.
*   **Complexity:**
    *   **Time:** O(1) - Simple arithmetic operations take constant time.
    *   **Space:** O(1) - No data structures are used, just a few integers.

### 5. Python -> Java Mapping
| Feature | Python | Java |
| :--- | :--- | :--- |
| **Function Definition** | `def my_func(arg):` | `public int myFunc(int arg) { ... }` |
| **Return** | `return 40` | `return 40;` (semicolon required) |
| **Variables** | `mins = 40` | `int mins = 40;` |
| **Constants** | `EXPECTED_MINS = 40` | `static final int EXPECTED_MINS = 40;` |

### 6. Hints & Pseudocode

**Step 1: Define the expected time**
*   **Hint:** The problem states the lasagna should be in the oven for 40 minutes.
*   **Snippet:**
    ```java
    public int expectedMinutesInOven() {
        return 40;
    }
    ```

**Step 2: Calculate remaining time**
*   **Hint:** Subtract the `actualMinutes` (passed as an argument) from the expected minutes.
*   **Pseudocode:** `return 40 - actualMinutes`

**Step 3: Calculate prep time**
*   **Hint:** Each layer takes 2 minutes. Multiply the number of layers by 2.
*   **Pseudocode:** `return layers * 2`

**Step 4: Total working time**
*   **Hint:** This is the sum of the preparation time and the time already spent in the oven.
*   **Pseudocode:** `return (layers * 2) + minutesInOven`
    *   *Advanced:* You can reuse `preparationTimeInMinutes(layers)` inside this method!

### 7. Practice Variations
1.  **Variable Prep Time:** Modify `preparationTimeInMinutes` to take a second argument `minutesPerLayer` allowing custom prep speeds.
2.  **Status Check:** Add a method `isReady(int actualMinutes)` returning a `boolean` if `remainingMinutesInOven` is <= 0.
3.  **Unit Conversion:** Add a method to return total seconds instead of minutes.

---

**Would you like me to walk through implementing any specific method, or are you ready to try writing the code?**