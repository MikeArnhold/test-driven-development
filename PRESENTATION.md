# Test Driven Development


### What is it?

- strategy for developers to:
    - make self-contained components/modules
    - reduce/control side effects
    - increase reliabilty and robustness


### TDD Pattern

| step | description |
| -: | - |
| <span style="color:#800000">**red**</span> | write a test that <u>*expectedly*</u> fails |
| <span style="color:#228B22">**green**</span> | implemented the functionality |
| <span style="color:#663399">**refactor**</span> | maintain, simplify, optimize |


### Pros

- code based on needs (expressed via tests)
- modular design
- internal refactoring (without changing interfaces) is easier
- no/less need for aditional testing
- indirect code documentation through test cases


### Cons

- slow process (in the beginning)
- requires team wide compliance
- interface changes may require refactoring of tests



### Implementing a sum function


```python
def test_five(self) -> None:
    self.assertEqual(5, my_sum(4, 1))
```
```python
def my_sum(*numbers: int) -> int:
    """Sums up all prvided integers"""
    pass
```


```console
> python -m unittest
F
======================================================================
FAIL: test_five (tests.MySumTests)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/proone/presentations/TDD/tests.py", line 8, in test_five
    self.assertEqual(5, my_sum(4, 1))
AssertionError: 5 != None

----------------------------------------------------------------------
Ran 1 test in 0.000s

FAILED (failures=1)
```


```python
def my_sum(*numbers: int) -> int:
    """Sums up all prvided integers"""
    return 5
```


```console
python -m unittest
.
----------------------------------------------------------------------
Ran 1 test in 0.000s

OK
```


```python
def test_seven(self) -> None:
    self.assertEqual(7, my_sum(2, 5))
```


```console
> python -m unittest
.F
======================================================================
FAIL: test_seven (tests.MySumTests)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/proone/presentations/TDD/tests.py", line 11, in test_seven
    self.assertEqual(7, my_sum(2, 5))
AssertionError: 7 != 5

----------------------------------------------------------------------
Ran 2 tests in 0.000s

FAILED (failures=1)
```


```python
def my_sum(*numbers: int) -> int:
    """Sums up all prvided integers"""
    return numbers[0] + numbers[1]
```


```console
> python -m unittest
..
----------------------------------------------------------------------
Ran 2 tests in 0.000s

OK
```


```python
def test_42_from_3_numbers(self) -> None:
    self.assertEqual(42, my_sum(20, 9, 13))
```


```console
> python -m unittest
F..
======================================================================
FAIL: test_42_from_3_numbers (tests.MySumTests)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/proone/presentations/TDD/tests.py", line 14, in test_42_from_3_numbers
    self.assertEqual(42, my_sum(20, 9, 13))
AssertionError: 42 != 29

----------------------------------------------------------------------
Ran 3 tests in 0.000s

FAILED (failures=1)
```


```python
def my_sum(*numbers: int) -> int:
    """Sums up all prvided integers"""
    _sum = 0
    for number in numbers:
        _sum += number
    return _sum
```


```console
> python -m unittest
...
----------------------------------------------------------------------
Ran 3 tests in 0.000s

OK
```


```python
def my_sum(*numbers: int) -> int:
    """Sums up all prvided integers"""

    def add(last: int, current: int) -> int:
        return last + current

    return reduce(add, numbers, 0)
```


```console
> python -m unittest
...
----------------------------------------------------------------------
Ran 3 tests in 0.000s

OK
```



### When to use TDD

<span style="font-size:0.6em">*control (horizontal) vs. complexity (vertical)*<span>

| | limited | full |
| -: | :-: | :-: |
| **low** | <span style="color:#F4A460">maybe... not...</span> |  <span style="color:#20B2AA">yes</span> |
| **high** | <span style="color:#20B2AA">yes</span> | <span style="color:#228B22">**yes, yes, YEEES!!!!**</span> |


### When do I use TDD

<span style="font-size:0.6em">*control (horizontal) vs. complexity (vertical)*<span>

| | limited | full |
| -: | :-: | :-: |
| **low** | <span style="color:#228B22">**yes, yes, YEEES!!!!**</span> |  <span style="color:#228B22">**yes, yes, YEEES!!!!**</span> |
| **high** | <span style="color:#228B22">**yes, yes, YEEES!!!!**</span> | <span style="color:#228B22">**yes, yes, YEEES!!!!**</span> |



### Types of tests

- **unit test**
    - test isolated modules
    - mock dependencies

- **integration test**
    - test interaction of modules



### ATDD and BDD

| | |
| --: | :-- |
| Given | Book that has not been checked out |
| And | User who is registered on the system |
| When | User checks out a book |
| Then | Book is marked as checked out |
