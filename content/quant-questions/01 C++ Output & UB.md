---
topic: "C++ Output & UB"
---
# C++ Output & Undefined Behaviour

What does the code print, or is it undefined behaviour?

## Unsigned wrap-around · Easy

```cpp
unsigned int a = 0;
a = a - 1;
std::cout << (a > 0) << '\n';
```

What is printed?

### Answer

`1`. Unsigned arithmetic is modulo 2^N, so `0 - 1` wraps to `UINT_MAX`, which is greater than zero. This is well defined, unlike signed overflow.

## Counting past the top · Medium

```cpp
int count = 0;
for (int i = INT_MAX - 2; i > 0; ++i)
    ++count;
std::cout << count << '\n';
```

How many iterations run, and what is printed?

### Answer

**Undefined behaviour.** Incrementing `i` past `INT_MAX` is signed overflow, which is UB, not wrap-around. Because overflow "cannot happen", the optimiser may assume `i > 0` stays true forever and turn this into an infinite loop, or print 3, or anything else. Use an unsigned type or a bound that cannot overflow.

## Plus-plus on both sides · Easy

```cpp
int i = 1;
int r = i++ + ++i;
std::cout << r << '\n';
```

What is printed?

### Answer

**Undefined behaviour.** The two modifications of `i` are unsequenced relative to each other (the operands of `+` are not ordered), and modifying a scalar twice without sequencing is UB. Compilers really do give different answers here. Even C++17's tightened evaluation rules do not cover `+`.

## The bigger of two temporaries · Medium

```cpp
const std::string& s = std::max(std::string("apple"), std::string("pear"));
std::cout << s << '\n';
```

What is printed?

### Answer

**Undefined behaviour (dangling reference).** `std::max` takes and returns `const T&`, so it returns a reference to one of the two temporaries. Those die at the end of the full-expression; lifetime extension only applies when a temporary binds *directly* to the reference, not through a function's return value. Take the result by value: `std::string s = std::max(...)`.

## Reference to a local · Easy

```cpp
const int& smallest(int a, int b) {
    int m = a < b ? a : b;
    return m;
}
int main() { std::cout << smallest(3, 4) << '\n'; }
```

What is printed?

### Answer

**Undefined behaviour.** `m` is destroyed when the function returns, so the caller reads through a dangling reference. It may happen to print 3 at -O0, but nothing is guaranteed. Most compilers warn (`-Wreturn-stack-address` / `-Wreturn-local-addr`); return by value instead.

## Editing a literal · Easy

```cpp
char* p = const_cast<char*>("hello");
p[0] = 'j';
std::cout << p << '\n';
```

What is printed?

### Answer

**Undefined behaviour.** A string literal has type `const char[N]` and may live in read-only memory (it typically segfaults). The `const_cast` compiles but writing through it modifies a const object. Since C++11, `char* p = "hello";` is ill-formed anyway; copy into a `char buf[] = "hello";` if you need to modify it.

## Minus one versus one · Easy

```cpp
int a = -1;
unsigned b = 1;
std::cout << (a < b) << '\n';
```

What is printed?

### Answer

`0`. The usual arithmetic conversions convert `a` to `unsigned`, so `-1` becomes `UINT_MAX`, and `UINT_MAX < 1` is false. Well defined but surprising; `-Wsign-compare` catches it, and C++20's `std::cmp_less(a, b)` compares correctly.

## Dangerous for-loops · Easy

```cpp
std::vector<int> v = {1, 2, 3};
for (std::size_t i = v.size() - 1; i >= 0; --i)
    std::cout << v[i] << ' ';
```

What happens?

### Answer

**Undefined behaviour (out-of-bounds read).** `i >= 0` is always true for an unsigned type, so after printing `3 2 1` the decrement wraps `i` to `SIZE_MAX` and `v[i]` reads far out of bounds. A related trap is `i < v.size() - 1` on an empty vector. Write `for (std::size_t i = v.size(); i-- > 0;)` or use reverse iterators.

## Small ints, big sums · Easy

```cpp
std::uint8_t a = 200, b = 100;
std::uint8_t c = 65;
std::cout << a + b << ' ' << sizeof(a + b) << ' ' << c << '\n';
```

What is printed (typical 32-bit `int`)?

### Answer

`300 4 A`. Integer promotion turns both `uint8_t` operands into `int` before the addition, so there is no wrap at 256 and the result has type `int`. But `c` itself is printed as a character because `uint8_t` is an alias for `unsigned char`, which `operator<<` treats as a char. Cast to `int` to print the number.

## Growing while walking · Medium

```cpp
std::vector<int> v = {1, 2, 3};
for (int x : v)
    if (x == 2) v.push_back(4);
std::cout << v.size() << '\n';
```

Is this OK?

### Answer

**Undefined behaviour.** The range-for holds iterators into `v`; if `push_back` reallocates (likely, since capacity is probably 3) every iterator is invalidated and the loop keeps reading freed memory. Even without reallocation, the cached `end()` is invalidated. Iterate by index, or collect additions and append after the loop.

## Passing by value · Easy

```cpp
struct Base { virtual std::string name() const { return "Base"; } };
struct Derived : Base { std::string name() const override { return "Derived"; } };
void print(Base b) { std::cout << b.name() << '\n'; }

print(Derived{});
```

What is printed?

### Answer

`Base`. Passing by value copies only the `Base` subobject into a new `Base` (object slicing), so its dynamic type is `Base` and the virtual call resolves to `Base::name`. Take `const Base&` to keep polymorphism.

## Virtual call during construction · Medium

```cpp
struct B { B() { hello(); } virtual void hello() { std::cout << "B\n"; } };
struct D : B { void hello() override { std::cout << "D\n"; } };

D d;
```

What is printed?

### Answer

`B`. While `B`'s constructor runs, the object's dynamic type is `B` (the vptr points to `B`'s vtable), because `D`'s members are not yet constructed. Virtual calls from constructors and destructors dispatch to the class currently being built. If `hello` were pure virtual in `B`, the call would be undefined behaviour.

## Globals in two files · Medium

```cpp
// a.cpp
std::string prefix = "px_";
// b.cpp
extern std::string prefix;
std::string name = prefix + "orders";
```

What is `name` after static initialisation?

### Answer

**It is not guaranteed** — the static initialisation order fiasco. Dynamic initialisation order of globals across different translation units is unspecified, so `name` may be built from a not-yet-constructed `prefix`, which is undefined behaviour. Within one TU, order is top to bottom. Fix with a function-local static (`const std::string& prefix() { static std::string p = "px_"; return p; }`) or `constinit`/`constexpr` where possible.

## Reading garbage · Easy

```cpp
int x;
if (x == 0) std::cout << "zero\n";
else        std::cout << "nonzero\n";
```

What is printed?

### Answer

**Undefined behaviour** (in C++20). Reading the indeterminate value of an uninitialised automatic variable is UB, so the compiler may print either line, both, or neither. (C++26 reclassifies this as "erroneous behaviour", but you should still initialise.) Globals and statics are zero-initialised, which is why this bug hides.

## Shifting too far · Easy

```cpp
unsigned x = 1;
int n = 32;
std::cout << (x << n) << '\n';
```

With 32-bit `unsigned`, what is printed?

### Answer

**Undefined behaviour.** Shifting by a count greater than or equal to the bit width of the (promoted) left operand is UB, even for unsigned types. On x86 the hardware masks the count to 5 bits so you often see `1`, while ARM gives `0`, and the optimiser can do anything. Use a 64-bit type or special-case `n >= 32`.

## Peeking at float bits · Medium

```cpp
float f = 1.0f;
std::uint32_t bits = *reinterpret_cast<std::uint32_t*>(&f);
std::cout << std::hex << bits << '\n';
```

Is this well defined?

### Answer

**No — it violates strict aliasing (undefined behaviour).** You may only access an object through its own type, a signed/unsigned variant, `char`, `unsigned char` or `std::byte`. It will usually print `3f800000`, but the optimiser is allowed to assume the two pointers do not alias. Use `std::bit_cast<std::uint32_t>(f)` (C++20) or `std::memcpy`.

## Copy constructor, maybe · Medium

```cpp
struct T {
    T()          { std::cout << "ctor "; }
    T(const T&)  { std::cout << "copy "; }
    T(T&&)       { std::cout << "move "; }
    ~T()         { std::cout << "dtor "; }
};
T make()  { return T(); }
T make2() { T t; return t; }

{ T a = make();  } std::cout << '\n';
{ T b = make2(); } std::cout << '\n';
```

What is printed?

### Answer

Line 1 is **guaranteed** `ctor dtor`; line 2 is **usually** `ctor dtor` but may be `ctor move dtor dtor`. Returning a prvalue has mandatory copy elision since C++17: `T()` initialises `a` directly. Returning a named local is NRVO, which is permitted but not required; if not elided, the local is treated as an rvalue, so the move constructor (not copy) is used.

## Most vexing parse · Easy

```cpp
struct W { W() { std::cout << "W"; } };

int main() {
    W w();
    std::cout << "done\n";
}
```

What is printed?

### Answer

`done`. `W w();` declares a function named `w` taking no arguments and returning `W`; no object is created, so the constructor never runs. Use `W w;` or `W w{};`.

## Moving a const · Medium

```cpp
struct S {
    S() = default;
    S(const S&) { std::cout << "copy\n"; }
    S(S&&)      { std::cout << "move\n"; }
};
const S s;
S s2 = std::move(s);
```

What is printed?

### Answer

`copy`. `std::move(s)` yields `const S&&`, which cannot bind to `S&&`, so overload resolution falls back to `S(const S&)`. `std::move` is only a cast; it does not force a move. This silently happens with `const` members and with returning `const` locals.

## Default arguments and overrides · Medium

```cpp
struct P { virtual void f(int x = 1) { std::cout << "P " << x << '\n'; } };
struct Q : P { void f(int x = 2) override { std::cout << "Q " << x << '\n'; } };

Q q;
P& p = q;
p.f();
q.f();
```

What is printed?

### Answer

```
Q 1
Q 2
```

The function body is chosen at runtime (dynamic type `Q`), but default arguments are filled in at compile time from the static type of the expression. Through `P&` the default is `1`; through `Q` it is `2`. Avoid redefining defaults in overrides.

## Even or odd? · Easy

```cpp
int v = 6;
if (v & 1 == 0) std::cout << "even\n";
else            std::cout << "odd\n";
```

What is printed?

### Answer

`odd`. `==` binds tighter than `&`, so this is `v & (1 == 0)`, i.e. `6 & 0`, which is `0` (false). Write `(v & 1) == 0`. The same trap exists with `|`, `^` and with `<<` versus `+` (`1 << n + 1` is `1 << (n + 1)`).

## sizeof an array parameter · Easy

```cpp
void g(int a[10]) { std::cout << sizeof(a) << '\n'; }

int z[10];
std::cout << sizeof(z) << ' ';
g(z);
```

What is printed on a 64-bit platform with 4-byte `int`?

### Answer

`40 8`. In the caller, `z` is a real array of 10 ints. An array parameter is adjusted to a pointer (`int* a`), so `sizeof(a)` is the pointer size; the `10` is ignored. Pass `std::span<int>` or `std::array<int, 10>&` to keep the size.

## Wrong delete · Easy

```cpp
std::string* p = new std::string[3];
delete p;
```

What happens?

### Answer

**Undefined behaviour.** Memory from `new[]` must be released with `delete[]` (and `new` with `delete`). In practice only one destructor runs and the allocator receives the wrong pointer (array cookies), often crashing. Use `std::vector` or `std::unique_ptr<std::string[]>`.

## Two owners, one pointer · Medium

```cpp
int* raw = new int(42);
std::shared_ptr<int> a(raw);
std::shared_ptr<int> b(raw);
std::cout << a.use_count() << '\n';
```

What is printed, and what happens at the end of scope?

### Answer

`1` is printed, then **undefined behaviour (double delete)** at scope exit. Each constructor from a raw pointer creates a separate control block, so each thinks it is the sole owner and both delete `raw`. Copy the first `shared_ptr` instead, use `std::make_shared`, or `enable_shared_from_this` when `this` is involved.

## Custom deleter magic? · Medium

```cpp
auto del = [](int* p) { delete p; };
std::cout << sizeof(std::unique_ptr<int>) << ' '
          << sizeof(std::unique_ptr<int, decltype(del)>) << ' '
          << sizeof(std::unique_ptr<int, void(*)(int*)>) << ' '
          << sizeof(std::shared_ptr<int>) << '\n';
```

What is printed on a typical 64-bit implementation?

### Answer

`8 8 16 16`. A stateless deleter (empty lambda or `std::default_delete`) is stored via the empty-base / `[[no_unique_address]]` optimisation and costs nothing. A function-pointer deleter must be stored, adding 8 bytes. `shared_ptr` is two pointers (object and control block) regardless of deleter, since the deleter lives in the control block. The exact sizes are implementation details, but these hold on libstdc++, libc++ and MSVC.

## Casting away const · Medium

```cpp
const int limit = 10;
int& r = const_cast<int&>(limit);
r = 20;
std::cout << limit << ' ' << r << '\n';
```

What is printed?

### Answer

**Undefined behaviour.** Modifying an object that was *defined* `const` is UB, regardless of the cast. Typically you see `10 20` because the compiler folds `limit` to the constant 10, but this is not guaranteed. `const_cast` is only safe for removing const from a reference/pointer to an object that is not itself const.
