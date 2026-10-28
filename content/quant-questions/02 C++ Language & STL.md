---
topic: "C++ Language & STL"
---
# C++ Language & STL

Concept questions on the language, the object model and the standard library.

## Cost of a virtual call · Medium

How is a virtual call typically implemented, and what does it cost compared with a normal call?

### Answer

**One extra indirect load-and-jump, plus lost inlining.** Each polymorphic object holds a hidden vptr to its class's vtable (an array of function pointers); a call loads the vptr, loads the slot, and calls indirectly. The loads are cheap when cached, but the indirect branch can mispredict and, more importantly, the compiler usually cannot inline through it. Devirtualisation (`final`, known dynamic type) can remove the cost.

## Rule of zero, three, five · Easy

State the rule of three, the rule of five and the rule of zero.

### Answer

**Three:** if you define a destructor, copy constructor or copy assignment, you probably need all three. **Five:** add the move constructor and move assignment, since declaring any of the three suppresses the implicit moves. **Zero:** prefer classes that define none of them, letting members like `std::vector` and `std::unique_ptr` manage resources so the compiler-generated versions are correct.

## Why noexcept moves matter · Medium

A `std::vector<T>` grows past its capacity. When does it move the old elements and when does it copy them?

### Answer

**It moves only if `T`'s move constructor is `noexcept` (or `T` is not copyable).** `push_back` gives the strong exception guarantee: if relocation throws halfway, the original buffer must be intact. A throwing move would leave moved-from elements behind, so `std::move_if_noexcept` falls back to copying. Forgetting `noexcept` on a user-written move constructor silently makes growth copy everything.

## Perfect forwarding · Medium

```cpp
template <class T>
void wrapper(T&& arg) { target(std::forward<T>(arg)); }
```

What is `T&&` here and what does `std::forward` do?

### Answer

**`T&&` is a forwarding (universal) reference, and `std::forward<T>` restores the argument's original value category.** With an lvalue argument `T` deduces to `U&` and reference collapsing makes the parameter `U&`; with an rvalue `T` is `U`. Inside the function `arg` is always an lvalue (it has a name), so `std::forward` casts back to an rvalue only when `T` is a non-reference type. This lets `target` pick its move overload when appropriate.

## RVO versus NRVO · Easy

What is the difference between RVO and NRVO, and which is guaranteed?

### Answer

**RVO (returning a prvalue, `return T(...);`) is guaranteed since C++17; NRVO (returning a named local) is optional.** With RVO the object is constructed straight into the caller's storage and no copy/move constructor is even required to exist. NRVO is done by all major compilers in simple cases, but not when different named objects can be returned on different paths. If NRVO does not happen, the return is an implicit move. Don't write `return std::move(local);` — it blocks NRVO.

## make_shared or new · Medium

Why prefer `std::make_shared<T>(args)` over `std::shared_ptr<T>(new T(args))`? Is there a downside?

### Answer

**One allocation instead of two, better locality, and exception safety.** `make_shared` places the object and the control block in a single allocation. The downside: the memory for `T` cannot be freed until all `weak_ptr`s are gone too, since it shares the block with the weak count — bad for large objects with long-lived weak references. It also cannot take a custom deleter.

## Reference cycles · Easy

Two objects hold `std::shared_ptr`s to each other. What goes wrong and how do you fix it?

### Answer

**They leak.** Each keeps the other's use count at 1, so neither destructor ever runs, even after all external owners are gone. Make one direction (usually child-to-parent or observer links) a `std::weak_ptr` and `lock()` it when needed.

## Is shared_ptr thread-safe? · Medium

Is `std::shared_ptr` thread-safe?

### Answer

**The control block is; the pointer object and the pointee are not.** Different threads can copy and destroy *different* `shared_ptr` instances sharing one object safely — the reference counts are atomic. But concurrent writes to the *same* `shared_ptr` variable (assign/reset while another thread reads it) are a data race; use `std::atomic<std::shared_ptr<T>>` (C++20) or a mutex. Access to the pointed-to object needs its own synchronisation.

## Placement new · Medium

What does placement new do, and what must you remember when using it?

### Answer

**It constructs an object in memory you already own, without allocating:** `T* p = new (buf) T(args);`. The buffer must be suitably sized and aligned (`alignas(T) std::byte buf[sizeof(T)]`). You must call the destructor explicitly (`p->~T()` or `std::destroy_at(p)`) and must not `delete` it. It is the basis of `std::vector`, `std::optional`, memory pools and arenas.

## CRTP versus virtual · Medium

What is CRTP, and when would you use it instead of virtual functions?

### Answer

**The Curiously Recurring Template Pattern: `class Derived : public Base<Derived>`, where `Base` calls `static_cast<Derived*>(this)->impl()`.** Dispatch is resolved at compile time, so calls can be inlined and objects carry no vptr. Use it in hot paths where the concrete type is known at compile time. The cost: no heterogeneous containers of `Base*`, more template code and longer compile times.

## SFINAE versus concepts · Medium

What is SFINAE, and what do C++20 concepts improve?

### Answer

**"Substitution failure is not an error": if substituting template arguments into a declaration produces invalid code, that overload is silently dropped rather than causing a hard error.** It was used (via `std::enable_if`, `decltype` tricks) to constrain templates. Concepts and `requires` clauses express the same constraints directly, give readable error messages, and support subsumption so the more constrained overload wins without hacks.

## constexpr, consteval, if constexpr · Medium

Distinguish `constexpr` function, `consteval` function and `if constexpr`.

### Answer

**`constexpr` function:** *may* be evaluated at compile time when used in a constant expression, otherwise runs at runtime. **`consteval`:** an immediate function that *must* be evaluated at compile time; any runtime call is an error. **`if constexpr`:** a compile-time branch inside a template where the discarded branch is not instantiated, so it may contain code that would not compile for the current type.

## inline and the ODR · Medium

What does `inline` mean on a function or variable in modern C++?

### Answer

**It means "may be defined in multiple translation units", not "inline this call".** The One Definition Rule normally allows exactly one definition of a non-inline function or variable in the program; `inline` permits identical definitions in every TU that includes the header, and the linker merges them. Inlining decisions are the optimiser's. Class-body member functions, templates and `constexpr` functions are implicitly inline; C++17 added `inline` variables.

## Container complexity · Easy

Give the complexity of: `std::deque` random access, `std::vector::push_back`, `std::map::find`, `std::unordered_map::find`, `std::vector::insert` at the front.

### Answer

**deque index: O(1); vector push_back: amortised O(1); map find: O(log n); unordered_map find: average O(1), worst O(n); vector front insert: O(n).** Vector growth multiplies capacity (1.5x or 2x), so total copy work is linear. `std::map` is a red-black tree; `unordered_map` degrades under many hash collisions.

## Which iterators survive? · Medium

After each operation, which iterators remain valid: `vector::push_back`, `vector::erase`, `deque::push_back`, `list::erase`, `unordered_map::insert`?

### Answer

**vector push_back:** all invalidated on reallocation, otherwise only `end()`. **vector erase:** those at and after the erased point. **deque push_back:** all iterators invalidated, but references and pointers to elements stay valid. **list erase:** only the erased element's iterators. **unordered_map insert:** iterators invalidated on rehash, but references/pointers to elements always stay valid (node-based).

## list versus vector traversal · Easy

Summing 10 million ints in `std::list` vs `std::vector`: both O(n). Why is the vector typically many times faster?

### Answer

**Cache and prefetching.** Vector elements are contiguous, so each 64-byte cache line brings 16 ints and the hardware prefetcher streams ahead; the loop can also be vectorised. List nodes are separate heap allocations scattered in memory, so each step is a dependent pointer load and often a cache miss. The extra 16 bytes of links per node also waste bandwidth.

## reserve versus resize · Easy

What is the difference between `v.reserve(100)` and `v.resize(100)`?

### Answer

**`reserve` changes capacity only; `resize` changes size.** After `reserve(100)` the vector is still empty and `v[0]` is UB, but the next 100 `push_back`s will not reallocate. After `resize(100)` there are 100 value-initialised elements and further `push_back`s append after them. A common bug is `reserve` followed by indexed writes.

## emplace_back versus push_back · Easy

When does `emplace_back` actually beat `push_back`?

### Answer

**When you pass constructor arguments rather than an existing object.** `emplace_back(args...)` constructs the element in place, avoiding a temporary plus move; `push_back(T(args))` and `emplace_back(T(args))` behave the same. Beware that `emplace_back` uses explicit constructors, so `std::vector<std::unique_ptr<X>> v; v.emplace_back(raw)` compiles where `push_back(raw)` would not, and may leak if growth throws.

## optional and variant · Easy

What are `std::optional<T>` and `std::variant<A, B>`, and do they allocate?

### Answer

**`optional` holds a `T` or nothing; `variant` holds exactly one of its alternatives (a type-safe union). Neither allocates.** Both store the value inline plus a flag/index, so `sizeof` is roughly the largest alternative plus a discriminator rounded to alignment. Access a variant with `std::visit` or `std::get_if`; `std::get` throws `bad_variant_access` on the wrong alternative.

## Throwing from constructors and destructors · Medium

What happens if a constructor throws? If a destructor throws?

### Answer

**Constructor: the object never existed** — its destructor is not run, but already-constructed members and bases are destroyed and memory from `new` is freed. So raw resources acquired earlier in the constructor body leak unless held by RAII members. **Destructor:** destructors are implicitly `noexcept`, so a throw calls `std::terminate`; even with `noexcept(false)`, throwing during stack unwinding terminates.

## When to dynamic_cast · Easy

What does `dynamic_cast` do and what does it cost?

### Answer

**A checked downcast (or cross-cast) using RTTI; it returns `nullptr` for pointers or throws `std::bad_cast` for references when the object is not of the target type.** It needs a polymorphic base. The check walks type information at runtime and can be expensive with deep or multiple inheritance, so it is avoided in hot paths; frequent use often signals that a virtual function or `std::variant` would fit better.

## Type erasure · Hard

What is type erasure? Give a standard-library example and sketch how it works.

### Answer

**Hiding a concrete type behind a uniform interface without requiring it to inherit from a common base.** Examples: `std::function`, `std::any`, `std::shared_ptr`'s deleter. Internally, a non-template wrapper holds a pointer to an internal abstract "concept" class, and a templated "model<T>" derived class stores the real object and forwards calls virtually (or via a hand-written table of function pointers). Small-buffer optimisation avoids heap allocation for small callables.

## Policy-based design · Medium

What is a policy class? Give an example from the standard library.

### Answer

**A template parameter that injects a piece of behaviour at compile time.** The host class delegates part of its work to the policy, so you combine behaviours without virtual calls. Standard examples: the allocator in containers, the deleter in `std::unique_ptr`, the comparator in `std::map`, the hash in `unordered_map`. In trading code, locking or logging policies (e.g. a no-op mutex for single-threaded builds) are common.

## Pimpl · Easy

What is the pimpl idiom and why use it?

### Answer

**"Pointer to implementation": the public class holds only a `std::unique_ptr<Impl>` to a class defined in the .cpp file.** Private members and their headers disappear from the public header, so changing them does not recompile clients and the ABI stays stable. Costs: an extra heap allocation and indirection on every call, and the destructor must be defined in the .cpp where `Impl` is complete.

## Static or dynamic polymorphism · Easy

Compare static polymorphism (templates/CRTP/concepts) with dynamic polymorphism (virtual functions).

### Answer

**Static: resolved at compile time — inlinable and zero-overhead, but a separate instantiation per type (code bloat, compile time) and no runtime heterogeneity. Dynamic: resolved at runtime via the vtable — one compiled body, heterogeneous containers and plugins, but an indirect call that blocks inlining.** Low-latency code prefers static polymorphism on hot paths and keeps virtuals for configuration and setup code.
