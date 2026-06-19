The worst case is O(n) however, we are performing early exit by actively cheking if the value is greater than 1 as we do the inputs in the dictionary.

```python
for i in nums:
    hash[i] = hash.get(i, 0) + 1
        if hash[i] > 1:
            return True
return False
```

edge cases like empty list is also handled here as it will directly return `False` as there is no element to iterate upon.

### Using Sets

This is much faster than the hashmap solution, i.e., solution_v2.py
The fastest one is solution_v3.py