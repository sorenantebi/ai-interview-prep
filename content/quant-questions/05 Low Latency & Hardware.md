---
topic: "Low Latency & Hardware"
---
# Low Latency & Hardware

Questions on how CPUs, caches and compilers shape the speed of C++ code on a trading hot path.

## Memory Hierarchy Numbers · Easy

Give rough latencies for an L1 hit, L2 hit, L3 hit and a main memory access on a modern x86 server.

### Answer

Approximate orders of magnitude: L1 ~1 ns (about 4 cycles), L2 ~3–5 ns (~12 cycles), L3 ~10–20 ns (~40 cycles), DRAM ~60–100 ns (hundreds of cycles). A cross-socket (remote NUMA) access adds more again. The point is that a cache miss to DRAM costs about 100x an L1 hit, so data layout often matters more than instruction count.

## Cache Lines · Easy

What is a cache line, and how big is it on x86?

### Answer

The cache line is the unit the caches move and track, 64 bytes on x86 (Apple M-series uses 128). Touching one byte brings the whole line in, so data accessed together should live together. Sequential access also triggers the hardware prefetcher, which is why scanning an array is much faster than chasing pointers.

## Loop Order · Easy

```cpp
double a[4096][4096];
double sum = 0;
for (int j = 0; j < 4096; ++j)
    for (int i = 0; i < 4096; ++i)
        sum += a[i][j];
```

Why is this slow, and what is the fix?

### Answer

C++ arrays are row-major, so `a[i][j]` and `a[i+1][j]` are 32 KiB apart; the inner loop touches a new cache line (and often a new page) on every iteration and uses 8 of its 64 bytes. Swapping the loops so `j` is innermost walks memory sequentially, uses every byte of each line and lets the prefetcher help, typically several times faster.

## Struct Padding · Medium

```cpp
struct A { char c1; double d; char c2; };
struct B { double d; char c1; char c2; };
```

What are `sizeof(A)` and `sizeof(B)` on x86-64?

### Answer

`sizeof(A) == 24`, `sizeof(B) == 16`. In `A`, `d` must be 8-byte aligned so 7 padding bytes follow `c1`, and the struct is padded to a multiple of 8 after `c2` (1 + 7 + 8 + 1 + 7). In `B` the two chars fit after `d` with 6 bytes of tail padding. Ordering members from largest to smallest alignment usually minimises padding; the compiler may not reorder them for you.

## False Sharing · Medium

Two threads each increment their own counter in a loop, and the counters sit next to each other in a struct. Why does this scale badly, and how do you fix it?

### Answer

Both counters are on the same cache line, so each write by one core invalidates the line in the other core's cache and the line ping-pongs between cores through the coherence protocol, even though the threads never share data logically. Fix it by putting each counter on its own line, e.g. `alignas(64)` (or `std::hardware_destructive_interference_size`), or by accumulating in a local variable and writing once at the end.

## Branch Prediction · Medium

Why can summing the elements greater than 128 in a random array be much faster once the array is sorted? How could you make the unsorted case fast too?

### Answer

The CPU predicts branches and speculatively executes ahead; a misprediction flushes the pipeline, costing roughly 15–20 cycles. On random data the `if (x > 128)` is a coin flip, so it mispredicts about half the time; on sorted data it is almost perfectly predictable. A branchless form such as `sum += (x > 128) * x;` or a conditional move removes the branch, so speed no longer depends on the data.

## likely and unlikely · Easy

What do `[[likely]]`/`[[unlikely]]` (or `__builtin_expect`) actually do?

### Answer

They tell the compiler which path is expected, so it lays out the hot path as straight-line fall-through code and moves the cold path (error handling, rare events) out of the way, improving instruction-cache use and fetch. They do not directly program the hardware branch predictor on modern x86. Wrong hints can make code slower, and profile-guided optimisation usually gives the same benefit from real data.

## Virtual Call Cost · Medium

What does a virtual function call cost compared with a direct call, and how can the compiler or programmer avoid it?

### Answer

A virtual call loads the vtable pointer, loads the function pointer, then makes an indirect call; that is a couple of loads plus a possible indirect-branch mispredict, and above all it blocks inlining. The compiler devirtualises when it can prove the dynamic type, helped by `final` on classes or functions, LTO and PGO. In hot code, programmers often replace runtime polymorphism with templates/CRTP or `std::variant` so the call is resolved at compile time.

## Inlining · Easy

What are the benefits and costs of inlining a function?

### Answer

Inlining removes call overhead and, more importantly, exposes the function body to the caller's optimisations (constant propagation, dead code removal, vectorisation). The cost is larger code, which can hurt the instruction cache and slow things down if overdone. The `inline` keyword is mostly about the one-definition rule; the compiler decides, though `__attribute__((always_inline))`/`noinline` can force it.

## Heap Allocation on the Hot Path · Medium

Why do low-latency systems avoid `new`/`malloc` on the hot path?

### Answer

A general-purpose allocator has variable cost: it may take locks, search free lists, and occasionally call `mmap`/`brk`, which means a system call and page faults on first touch. That gives unpredictable tail latency and scattered memory that misses cache. Hot paths preallocate at startup and reuse objects through pools, ring buffers or fixed-capacity containers.

## Memory Pools · Medium

How does a fixed-size object pool work, and why is it fast?

### Answer

At startup it allocates one contiguous block of N slots and links the free slots into a free list. Allocation pops the head and deallocation pushes the slot back, both O(1) with no system call or lock (for a single-threaded pool). Objects stay close together in memory, so they are more cache friendly, and the memory is pre-faulted, so there are no page faults later.

## Software Prefetching · Medium

What does `__builtin_prefetch` do, and when is it useful?

### Answer

It hints the CPU to start loading a cache line before it is needed, without blocking. It helps for access patterns the hardware prefetcher cannot predict, such as walking a linked structure or hash table where you know the next address a little in advance. Prefetching too late does nothing and too early or too much evicts useful data, so it must be measured.

## NUMA · Medium

What is NUMA, and what should a trading application do about it?

### Answer

On a multi-socket server each socket has its own memory controller; memory attached to the other socket is reachable but slower and travels over the inter-socket link. Linux places a page on the node of the thread that first touches it. A trading process should pin its threads and allocate (and first-touch) its memory on the same node, and put the NIC's node on the same socket as the threads handling its traffic (`numactl`, `libnuma`).

## SIMD Basics · Medium

What is SIMD, and how do you get it in C++?

### Answer

Single Instruction, Multiple Data: one instruction operates on a whole vector register, e.g. 8 floats at once with AVX2 or 16 with AVX-512. You get it through compiler auto-vectorisation (helped by `-O3`, `-march=native`, simple loops, contiguous data and no aliasing), intrinsics like `_mm256_add_ps`, or libraries. Data laid out as struct-of-arrays vectorises far more easily than array-of-structs.

## Measuring Latency · Hard

You need to measure the latency of a function that takes ~200 ns. How do you do it properly, and what statistics do you report?

### Answer

Use a cheap, high-resolution clock such as `rdtsc`/`rdtscp` (invariant TSC, converted using the measured frequency, with fences to stop reordering) or `clock_gettime(CLOCK_MONOTONIC)` via vDSO. Warm up first so caches, branch predictors and lazily faulted pages reach steady state, pin the thread, and record each sample into a preallocated histogram. Report percentiles (median, p99, p99.9, max) rather than only the mean, because trading cares about tail latency and a mean hides rare large spikes.

## Busy Polling vs Blocking · Medium

What is the trade-off between busy polling and blocking while waiting for data?

### Answer

Blocking (e.g. `epoll_wait` with a timeout, or a condition variable) puts the thread to sleep, saving CPU, but waking it costs an interrupt, scheduler work and a context switch, adding microseconds and jitter, with cold caches afterwards. Busy polling spins on the socket or queue so it reacts within nanoseconds, at the cost of burning a whole core at 100%. Trading hot paths spin on isolated cores; non-critical threads block.

## Logging off the Hot Path · Medium

How should a low-latency trading thread do logging?

### Answer

Never format strings or do file I/O on the hot thread. Write a small binary record (timestamp, format-string id, raw arguments) into a preallocated lock-free single-producer ring buffer, and let a background thread on another core format and write it. This keeps the hot-path cost to tens of nanoseconds and avoids system calls and blocking on disk.

## Tick to Trade · Easy

What is "tick-to-trade" latency?

### Answer

The time from a market data packet arriving at your system (usually measured at the NIC, i.e. on the wire) to the resulting order packet leaving it. It covers packet receive, feed decoding, book update, strategy decision, risk checks, order encoding and send. Software systems are typically single-digit microseconds; FPGA systems reach tens to hundreds of nanoseconds (approximate).

## Compiler Flags · Medium

What do `-O2`, `-O3`, `-march=native`, LTO and PGO each give you?

### Answer

`-O2` enables most standard optimisations; `-O3` adds more aggressive inlining, loop unrolling and vectorisation, which is usually but not always faster. `-march=native` lets the compiler use every instruction set of the build machine (AVX2, AVX-512, BMI), so the binary may not run on older CPUs. LTO (`-flto`) optimises across translation units, enabling cross-file inlining and devirtualisation. PGO compiles with instrumentation, runs a representative workload, then recompiles using the profile to guide inlining, block layout and branch hints.

## std::endl vs newline · Easy

Why is `std::cout << x << std::endl;` slower than `std::cout << x << '\n';` in a loop?

### Answer

`std::endl` writes a newline and then flushes the stream, forcing a `write` system call on every line. `'\n'` only appends to the buffer, which is flushed when it fills, so many lines share one system call. Use `std::flush` or `std::endl` only when the output must be visible immediately.

## Hyper-threading · Medium

Why do many low-latency setups disable hyper-threading (SMT) or leave the sibling thread idle?

### Answer

Two hardware threads on one core share its execution units, L1/L2 caches, TLB and branch predictors. Work on the sibling thread therefore steals resources and evicts data from the hot thread unpredictably, increasing jitter. Disabling SMT, or isolating the sibling and leaving it unused, gives the critical thread the whole core.

## Power States and Frequency · Medium

How can CPU power management hurt latency, and what is done about it?

### Answer

Idle cores drop into deep C-states, and waking from them can take tens of microseconds; frequency scaling (P-states) can also leave a core running slowly when work arrives. Low-latency hosts set the performance governor, limit C-states (BIOS settings, `intel_idle.max_cstate`, `processor.max_cstate`, or holding `/dev/cpu_dma_latency` at 0) and often fix the frequency. Busy polling also keeps the core awake.
