● I'll create a concise Python vs Java cheat sheet tailored to the Annalyn's Infiltration exercise
    (focusing on boolean logic and basic syntax).

● Let me check the current directory structure first:

● I don't have permission to create files in that directory. Let me output the cheat sheet here
   instead:

   ---

   # **Python vs Java Cheat Sheet: Annalyn's Infiltration**

   ## **1. SYNTAX EQUIVALENTS**

   ### **Variables & Booleans**
   ```python
   # Python
   knight_awake = True   # Capitalized True/False
   ```
   ```java
   // Java
   boolean knightAwake = true;   // lowercase true/false, semicolons required
   ```

   ### **Functions/Methods**
   ```python
   # Python (snake_case)
   def can_fast_attack(knight_awake):
       return not knight_awake
   ```
   ```java
   // Java (camelCase, static methods in class)
   public static boolean canFastAttack(boolean knightAwake) {
       return !knightAwake;
   }
   ```

   ### **Boolean Operators**
   | Operation | Python | Java |
   |-----------|--------|------|
   | NOT | `not x` | `!x` |
   | AND | `x and y` | `x && y` |
   | OR | `x or y` | `x \|\| y` |

   ### **Conditionals**
   ```python
   # Python (no parentheses, colon, indentation)
   if archer and prisoner:
       return False
   elif not archer:
       return True
   ```
   ```java
   // Java (parentheses, braces)
   if (archer && prisoner) {
       return false;
   } else if (!archer) {
       return true;
   }
   ```

   ## **2. DATA STRUCTURES (DSA)**

   ### **List/Array**
   ```python
   # Python: dynamic list
   chars = ["knight", "archer"]
   chars.append("dog")
   ```
   ```java
   // Java: ArrayList (dynamic)
   List<String> chars = new ArrayList<>();
   chars.add("knight");
   ```

   ### **Dict/Map**
   ```python
   # Python
   status = {"knight": True}
   status["archer"] = False
   ```
   ```java
   // Java
   Map<String, Boolean> status = new HashMap<>();
   status.put("knight", true);
   ```

   ### **Set**
   ```python
   # Python
   awake = {"knight", "archer"}
   if "knight" in awake:
   ```
   ```java
   // Java
   Set<String> awake = new HashSet<>();
   if (awake.contains("knight")) {
   ```

   ### **Sorting**
   ```python
   # Python
   nums.sort()  # in-place
   sorted_nums = sorted(nums)  # new list
   ```
   ```java
   // Java
   Arrays.sort(nums);  // in-place
   Collections.sort(list);
   ```

   ## **3. KEY PITFALLS**

   ### **Naming** 🔥
   - Python: `snake_case` → Java: `camelCase`
   - Python: `True/False` → Java: `true/false`

   ### **Pass-by-Value** 🔥
   ```python
   # Python: lists passed by reference
   def modify(lst):
       lst.append(1)  # mutates original
   ```
   ```java
   // Java: primitives by value, objects by reference
   void modify(int x) { x = 5; }  // NO effect
   void modify(int[] arr) { arr[0] = 5; }  // mutates
   ```

   ### **String Mutability** 🔥
   ```python
   # Python: string immutable but unlimited size
   s = "a" * 10**6  # works fine
   ```
   ```java
   // Java: use StringBuilder in loops!
   StringBuilder sb = new StringBuilder();
   for (int i = 0; i < 1000; i++) {
       sb.append("a");  // efficient
   }
   ```

   ### **Integer Overflow** 🔥
   ```python
   # Python: no overflow (arbitrary precision)
   x = 10**100  # works
   ```
   ```java
   // Java: int overflows at 2^31-1
   int x = Integer.MAX_VALUE + 1;  // overflow → negative!
   ```

   ### **Char vs String** 🔥
   ```python
   # Python: no char type
   c = 'a'  # still a string
   ```
   ```java
   // Java: different types!
   char c = 'a';    // single quotes
   String s = "a";  // double quotes
   ```

   ## **4. ANNALYN EXAMPLES**

   ### **Task 1: Fast Attack**
   ```python
   return not knight_awake
   ```
   ```java
   return !knightAwake;
   ```

   ### **Task 2: Spy (any awake)**
   ```python
   return knight or archer or prisoner
   ```
   ```java
   return knight || archer || prisoner;
   ```

   ### **Task 3: Signal (prisoner awake AND archer sleeping)**
   ```python
   return prisoner_awake and not archer_awake
   ```
   ```java
   return prisonerAwake && !archerAwake;
   ```

   ### **Task 4: Free Prisoner**
   ```python
   if dog_present:
       return not archer
   return prisoner and not knight and not archer
   ```
   ```java
   if (dogPresent) {
       return !archer;
   }
   return prisoner && !knight && !archer;
   ```

   ## **5. QUICK REFERENCE**

   | Feature | Python | Java |
   |---------|--------|------|
   | Comments | `# text` | `// text` |
   | Print | `print(x)` | `System.out.println(x)` |
   | Null | `None` | `null` |
   | String concat | `"a" + "b"` | `"a" + "b"` |
   | Type check | `isinstance(x, int)` | `x instanceof Integer` |

   ## **6. COMPLEXITY**
   All Annalyn methods: **O(1) time**, **O(1) space** (simple boolean logic)

   ---
   **Key Takeaway**: For this exercise, focus on **operator syntax** (`not` → `!`, `and` → `&&`,
   `or` → `||`) and **naming conventions** (snake_case → camelCase).