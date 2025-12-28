● # Annalyn's Infiltration - Study Guide

   ## What the Exercise Wants

   You need to implement **4 static methods** in the `AnnalynsInfiltration` class. Each method
   evaluates **boolean logic** conditions to determine if certain rescue actions are feasible:

   1. **`canFastAttack(knightIsAwake)`** - Returns `true` only if knight is sleeping
   2. **`canSpy(knightIsAwake, archerIsAwake, prisonerIsAwake)`** - Returns `true` if **at least
   one** person is awake
   3. **`canSignalPrisoner(archerIsAwake, prisonerIsAwake)`** - Returns `true` if prisoner is awake
    **AND** archer is sleeping
   4. **`canFreePrisoner(knightIsAwake, archerIsAwake, prisonerIsAwake, petDogIsPresent)`** -
   Complex logic with two success paths:
      - **With dog**: Archer must be asleep (knight status doesn't matter)
      - **Without dog**: Prisoner awake AND both knight/archer asleep

   ---

   ## What the Tests Enforce

   ### Task 1: `canFastAttack` (2 tests)
   - ✅ Knight awake → `false`
   - ✅ Knight sleeping → `true`

   ### Task 2: `canSpy` (8 tests - exhaustive!)
   - Tests all combinations **except** everyone sleeping
   - Key insight: "At least one awake" = use `||` (OR)

   ### Task 3: `canSignalPrisoner` (4 tests - truth table)
   | Archer Awake | Prisoner Awake | Result |
   |--------------|----------------|--------|
   | false        | true           | **true** |
   | true         | false          | false  |
   | false        | false          | false  |
   | true         | true           | false  |

   ### Task 4: `canFreePrisoner` (16 tests!)
   The most complex. Tests validate:
   - **With dog + archer asleep** → `true` (regardless of others)
   - **Without dog + prisoner awake + both guards asleep** → `true`
   - All other cases → `false`

   ---

   ## Key Java Concepts

   ### 1. **Boolean Operators**
   ```java
   !    // NOT - flips true/false
   &&   // AND - both must be true
   ||   // OR - at least one must be true
   ```

   ### 2. **Static Methods**
   Methods belong to the **class**, not instances:
   ```java
   public static boolean canFastAttack(boolean knightIsAwake) {
       // No need to create an object
   }
   // Called as: AnnalynsInfiltration.canFastAttack(true)
   ```

   ### 3. **Operator Precedence**
   `!` binds tighter than `&&`, which binds tighter than `||`:
   ```java
   !a && b || c  // Evaluated as: ((!a) && b) || c
   ```

   ### 4. **Short-Circuit Evaluation**
   Java evaluates left-to-right and stops early:
   ```java
   false && expensiveCheck()  // expensiveCheck() never runs
   true || expensiveCheck()   // expensiveCheck() never runs
   ```

   ---

   ## Edge Cases

   1. **Task 1**: Simple negation - watch out for double negatives
   2. **Task 2**: All sleeping → `false` (only failure case)
   3. **Task 3**: Both awake → `false` (archer intercepts signal!)
   4. **Task 4**:
      - Dog sleeping doesn't matter (boolean is about *presence*)
      - Prisoner sleeping with dog → still fails (can't wake prisoner)
      - Archer awake with dog → fails (archer reacts too fast)

   ---

   ## DSA Pattern

   **Pattern**: **Boolean Algebra / Logic Gates**
   - Not a traditional DSA problem (no arrays/trees/graphs)
   - Focuses on **propositional logic** and **truth tables**
   - Similar to circuit design or state machines

   **Complexity**:
   - **Time**: O(1) - Fixed number of boolean operations
   - **Space**: O(1) - No data structures, just primitive checks

   ---

   ## Python → Java Mapping

   | Python | Java | Notes |
   |--------|------|-------|
   | `not` | `!` | Logical NOT |
   | `and` | `&&` | Logical AND |
   | `or` | `\|\|` | Logical OR |
   | `True` / `False` | `true` / `false` | Lowercase in Java! |
   | `def canFastAttack(knight):` | `public static boolean canFastAttack(boolean knight) {` | Type
   declarations required |
   | `return not knight` | `return !knight;` | Semicolons required |
   | No `static` keyword needed | `static` for class-level methods | Java requires explicit
   `static` |

   **Key Differences**:
   ```python
   # Python
   def can_spy(k, a, p):
       return k or a or p

   # Java
   public static boolean canSpy(boolean k, boolean a, boolean p) {
       return k || a || p;
   }
   ```

   ---

   ## Hint Ladder

   ### Task 1: `canFastAttack`
   **🪜 Hint 1**: What's the opposite of "awake"?
   **🪜 Hint 2**: Use the `!` operator
   **🪜 Hint 3**: `return !knightIsAwake;`

   ---

   ### Task 2: `canSpy`
   **🪜 Hint 1**: "At least one" means...?
   **🪜 Hint 2**: Use `||` to chain conditions
   **🪜 Hint 3**: Pseudocode:
   ```
   if knight OR archer OR prisoner is awake
       return true
   else
       return false
   ```
   **🪜 Hint 4**: Can simplify to single expression!

   ---

   ### Task 3: `canSignalPrisoner`
   **🪜 Hint 1**: Both conditions must be satisfied (think `&&`)
   **🪜 Hint 2**: Prisoner awake is required, archer awake is forbidden
   **🪜 Hint 3**: Pseudocode:
   ```
   return (prisoner is awake) AND (archer is NOT awake)
   ```

   ---

   ### Task 4: `canFreePrisoner`
   **🪜 Hint 1**: Two separate success scenarios - use `||` between them
   **🪜 Hint 2**: Path A (with dog): `petDogIsPresent && !archerIsAwake`
   **🪜 Hint 3**: Path B (sneaky): All three must be true:
   - Prisoner awake
   - Knight sleeping
   - Archer sleeping

   **🪜 Hint 4**: Structure:
   ```java
   return (dogPath) || (sneakyPath);
   ```

   **🪜 Hint 5**: Full pseudocode:
   ```
   WITH_DOG = petDogIsPresent AND archer is asleep
   SNEAKY = prisoner awake AND knight asleep AND archer asleep
   return WITH_DOG OR SNEAKY
   ```

   ---

   ## Practice Variations

   ### Variation 1: **Guard Tower** (Similar logic)
   Annalyn can climb a tower if:
   - Ladder is available OR (rope is available AND knot skill is true)
   - Guard is NOT looking up

   ```java
   public static boolean canClimbTower(boolean hasLadder, boolean hasRope,
                                        boolean knowsKnots, boolean guardLookingUp) {
       // Your implementation
   }
   ```

   ---

   ### Variation 2: **Treasure Chest** (Nested conditions)
   Open chest if:
   - Has key OR (has lockpick AND dexterity > 5)
   - Trap is disabled OR has trapfinding skill

   ```java
   public static boolean canOpenChest(boolean hasKey, boolean hasLockpick,
                                       int dexterity, boolean trapDisabled,
                                       boolean hasTrapfinding) {
       // Your implementation
   }
   ```

   ---

   ### Variation 3: **Bridge Crossing** (XOR pattern)
   Can cross bridge if:
   - EXACTLY one of: has wings OR has boat (not both, not neither)
   - Troll is asleep OR has gold to bribe

   ```java
   public static boolean canCrossBridge(boolean hasWings, boolean hasBoat,
                                         boolean trollAsleep, boolean hasGold) {
       // Hint: XOR in Java is ^, or use != for booleans
   }
   ```

   ---

   ## Testing Your Solution

   Once implemented, run tests:
   ```bash
   cd annalyns-infiltration
   # Windows
   .\gradlew.bat test

   # Or if you have Gradle installed
   gradle test
   ```

   Good luck! 🎯