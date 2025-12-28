Here is a concise Python vs Java cheat sheet for the **testing-gemini-cli** topic, formatted for your notes.

---

# **Python vs Java Cheat Sheet: Testing Gemini CLI**

## **1. SYNTAX EQUIVALENTS**

### **Variables & Types**
```python
# Python: Dynamic, snake_case
count = 42
is_active = True
name = "Gemini"
```
```java
// Java: Static, camelCase
int count = 42;
boolean isActive = true;
String name = "Gemini";
```

### **Conditionals**
```python
# Python
if count > 10:
    res = "High"
elif count == 0:
    res = "Zero"
else:
    res = "Low"
```
```java
// Java
if (count > 10) {
    res = "High";
} else if (count == 0) {
    res = "Zero";
} else {
    res = "Low";
}
```

### **Loops**
```python
# Python: Range & For-Each
for i in range(5):
    print(i)

for item in items:
    print(item)
```
```java
// Java: C-Style & For-Each
for (int i = 0; i < 5; i++) {
    System.out.println(i);
}

for (String item : items) {
    System.out.println(item);
}
```

### **Functions**
```python
# Python: def, snake_case
def calculate_total(a, b):
    return a + b
```
```java
// Java: typed, camelCase
public int calculateTotal(int a, int b) {
    return a + b;
}
```

## **2. COMMON DSA CONSTRUCTS**

### **List / Array**
```python
# Python: List
lst = [1, 2]
lst.append(3)
val = lst[0]
len(lst)
```
```java
// Java: ArrayList
List<Integer> lst = new ArrayList<>();
lst.add(1);
lst.add(2);
lst.add(3);
int val = lst.get(0);
lst.size();
```

### **Dict / Map**
```python
# Python: Dict
map = {"key": "val"}
map["new"] = "val2"
v = map.get("key")
```
```java
// Java: HashMap
Map<String, String> map = new HashMap<>();
map.put("key", "val");
map.put("new", "val2");
String v = map.get("key");
```

### **Set**
```python
# Python: Set
s = {1, 2}
s.add(3)
exists = 1 in s
```
```java
// Java: HashSet
Set<Integer> s = new HashSet<>();
s.add(1);
s.add(2);
s.add(3);
boolean exists = s.contains(1);
```

### **Stack / Queue**
```python
# Python: deque
from collections import deque
d = deque()
d.append(1)      # push
d.pop()          # pop stack
d.popleft()      # pop queue
```
```java
// Java: Deque
Deque<Integer> d = new ArrayDeque<>();
d.push(1);       // push stack
d.pop();         // pop stack
d.poll();        // poll queue
```

## **3. KEY PITFALLS**

### **Equality** 🔥
```python
# Python
if a == b:  # Value equality
if a is b:  # Reference equality
```
```java
// Java
if (a.equals(b)) { // Value equality (Objects)
if (a == b) {      // Reference equality (Objects)
```

### **Integer Overflow** 🔥
*   **Python**: No overflow (arbitrary precision).
*   **Java**: `int` overflows at $2^{31}-1$. Use `long` or `BigInteger`.

### **String Mutability** 🔥
*   **Python**: Strings are immutable. `s += "a"` creates a NEW string.
*   **Java**: Strings are immutable. Use `StringBuilder` for loops.

### **Char Type** 🔥
*   **Python**: No char type. `'a'` is a string of length 1.
*   **Java**: `char` is a 16-bit integer. `'a' + 1` results in `98`, not `"ab"`.

## **4. TINY EXAMPLES**

### **Filter & Map**
```python
# Python: List Comprehension
evens = [x * 2 for x in nums if x % 2 == 0]
```
```java
// Java: Streams
List<Integer> evens = nums.stream()
    .filter(x -> x % 2 == 0)
    .map(x -> x * 2)
    .collect(Collectors.toList());
```

### **Swap Variables**
```python
# Python
a, b = b, a
```
```java
// Java
int temp = a;
a = b;
b = temp;
```

## **5. QUICK REFERENCE**

| Concept | Python | Java |
| :--- | :--- | :--- |
| **Null** | `None` | `null` |
| **Logic** | `and`, `or`, `not` | `&&`, `\|\|`, `!` |
| **Length** | `len(x)` | `x.length` / `x.size()` |
| **Print** | `print(x)` | `System.out.println(x)` |