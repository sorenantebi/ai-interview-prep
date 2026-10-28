---
topic: "OS & Networking"
---
# Operating Systems & Networking

Short-answer questions on the kernel, memory and the network stack, as asked in quant dev and HFT interviews.

## Why Virtual Memory · Easy

What is virtual memory, and why do operating systems use it instead of letting processes address physical RAM directly?

### Answer

Each process gets its own private address space that the MMU translates to physical frames through page tables. This gives isolation (one process cannot read or corrupt another), lets the OS place pages anywhere in RAM, share pages (libraries, copy-on-write after `fork`), lazily allocate memory and swap rarely used pages to disk. Programs can also be linked against a simple, uniform address layout.

## Page Fault Mechanism · Medium

What happens on a page fault, and what is the difference between a minor and a major fault?

### Answer

The MMU finds no valid mapping for the address, traps into the kernel, and the fault handler either fixes the mapping and restarts the instruction or sends SIGSEGV if the access is illegal. A minor fault is resolved without disk I/O (first touch of a zero page, page already in the page cache, copy-on-write) and costs roughly microseconds. A major fault must read the page from disk or swap and can cost milliseconds. Latency-critical code pre-faults memory at startup (touch every page, `mlockall`) so neither happens on the hot path.

## TLB Miss Handling · Medium

What is the TLB, what happens on a TLB miss, and how do huge pages help?

### Answer

The TLB is a small cache of recent virtual-to-physical translations inside the CPU. On a miss, the hardware (on x86) walks the multi-level page table in memory, which costs several memory accesses, then fills the TLB. With 4 KiB pages a TLB of ~1500 entries covers only a few MiB; 2 MiB or 1 GiB huge pages let the same number of entries cover far more memory, so large working sets (order books, hash tables) take far fewer misses and page walks are shorter.

## Context Switch Cost · Medium

What does a context switch cost, and why does it matter for low-latency code?

### Answer

The direct cost is roughly 1–5 µs (approximate): saving and restoring registers, switching kernel stacks and, for a process switch, the address space. The indirect cost is often bigger: caches, TLB and branch predictors are polluted by the other task, so the code runs slowly for a while after it resumes. Hot threads are therefore pinned to dedicated cores and never block, so they are never switched out.

## Process vs Thread · Easy

What is the difference between a process and a thread?

### Answer

A process has its own address space, file descriptor table and other resources; a thread is an execution context (registers, stack) that shares its process's address space with other threads. Threads communicate cheaply through shared memory but one bad thread can crash all of them; processes are isolated and need IPC to talk. On Linux both are tasks created by `clone` with different sharing flags.

## Fastest IPC · Medium

Which inter-process communication mechanism is usually fastest, why, and what happens to a POSIX shared memory segment when the last process using it exits?

### Answer

Shared memory: once mapped, data moves with plain loads and stores, no system calls or copies through the kernel (synchronisation is up to you, e.g. a lock-free ring buffer). A POSIX segment created with `shm_open` is kernel-persistent: it survives the last process exiting until someone calls `shm_unlink` or the machine reboots. After it has been unlinked, the memory is freed when the last mapping is removed.

## mmap MAP_SHARED · Medium

You `mmap` a file with `MAP_SHARED` and write to the mapping. What happens, and how does that differ from `MAP_PRIVATE`?

### Answer

With `MAP_SHARED` writes go to the page cache pages of the file, so other processes mapping the same file see them immediately and the kernel eventually writes them back to disk (`msync` forces it). With `MAP_PRIVATE` the first write to a page triggers copy-on-write, giving the process its own copy; changes are never visible to others nor written to the file.

## System Call Cost · Medium

Roughly how expensive is a system call and why do HFT systems try to avoid them on the hot path?

### Answer

A trivial syscall costs on the order of 100 ns to 1 µs (approximate), more with speculative-execution mitigations. The CPU switches privilege level, saves state, runs kernel code that evicts some of your cache lines, and may reschedule you. Calls like `read`/`send` also copy data and walk the network stack. Hot paths avoid them with shared memory, kernel bypass and vDSO-backed calls such as `clock_gettime`.

## CPU Affinity and isolcpus · Medium

What are CPU affinity and `isolcpus`, and why would a trading system use them?

### Answer

Affinity (`sched_setaffinity`, `taskset`) pins a thread to specific cores so it never migrates and keeps its caches warm. `isolcpus` (often with `nohz_full` and IRQ affinity changes) removes cores from the general scheduler so the OS will not put other tasks or most interrupts on them. Together they give a hot thread a core of its own, which removes scheduler jitter and cuts tail latency.

## ABI vs API · Easy

What is the difference between an API and an ABI?

### Answer

An API is the source-level contract: function names, types and semantics you compile against. An ABI is the binary-level contract: calling convention, struct layout, name mangling, sizes and alignment, vtable layout. You can keep an API stable while breaking the ABI (e.g. adding a member to a class), which forces all callers to be recompiled; this is why `std::string` changes in GCC 5 needed a dual ABI.

## TCP Three-way Handshake · Easy

Describe the TCP three-way handshake. Why three messages rather than two?

### Answer

Client sends SYN with its initial sequence number, server replies SYN-ACK with its own sequence number and acknowledges the client's, client sends ACK. Each side must announce its starting sequence number and have it acknowledged, which takes three messages when the server's SYN and ACK are combined. It also guards against old duplicate SYNs opening a stale connection.

## Flow vs Congestion Control · Medium

What is the difference between TCP flow control and congestion control?

### Answer

Flow control protects the receiver: the receiver advertises a window of how much buffer space it has, and the sender never has more unacknowledged data in flight than that. Congestion control protects the network: the sender keeps its own congestion window (slow start, AIMD, algorithms like CUBIC or BBR) that shrinks on loss or delay. The sender uses the minimum of the two windows.

## Nagle Algorithm Purpose · Medium

What does Nagle's algorithm do, and why do low-latency applications set `TCP_NODELAY`?

### Answer

Nagle holds back small segments while earlier data is still unacknowledged, coalescing them into fewer full-size packets to cut header overhead on slow links. For an order gateway this means a small order message can wait up to a round trip before being sent. `TCP_NODELAY` disables Nagle so each write goes out immediately.

## Nagle and Delayed ACK · Hard

Why can Nagle's algorithm combined with delayed ACKs cause latency spikes of tens of milliseconds?

### Answer

The sender writes a message in two small pieces: the first goes out, but Nagle holds the second until the first is acknowledged. The receiver uses delayed ACK and waits (often ~40 ms on Linux, up to 200 ms elsewhere) for more data or a reply to piggyback the ACK on, which never comes because the rest of the message is stuck at the sender. Both sides wait until the delayed-ACK timer fires. Fixes: `TCP_NODELAY`, write the whole message in one call, or `TCP_QUICKACK` on the receiver.

## Detecting Dead Peers · Medium

A TCP connection to an exchange looks open but the peer's machine lost power. How do you detect it?

### Answer

An idle TCP connection sends nothing, so without traffic you never learn the peer is gone. TCP keepalive (`SO_KEEPALIVE`, tuned with `TCP_KEEPIDLE`, `TCP_KEEPINTVL`, `TCP_KEEPCNT`) sends probes after idle time and resets the connection if they go unanswered, but the default idle time is two hours. In practice trading protocols use application-level heartbeats (e.g. FIX Heartbeat/TestRequest) with timeouts of seconds; `TCP_USER_TIMEOUT` also bounds how long unacknowledged data may sit.

## MTU and Fragmentation · Medium

What is the MTU, and what happens when an IP packet is larger than the MTU of a link on its path?

### Answer

The MTU is the largest packet a link can carry, typically 1500 bytes on Ethernet (9000 with jumbo frames). In IPv4, a router may fragment the packet if the Don't Fragment bit is clear; otherwise it drops it and sends ICMP "fragmentation needed", which Path MTU Discovery uses. IPv6 routers never fragment. Fragmentation hurts: losing any fragment loses the whole packet, and reassembly adds latency, so market data protocols keep messages under the MTU.

## TCP vs UDP for Market Data · Easy

Why do exchanges usually publish market data over UDP multicast instead of TCP?

### Answer

Multicast sends each packet once and the network replicates it to every subscriber, so all clients get the data at the same time and the exchange's load does not grow with the number of clients. UDP has no handshake, retransmission or head-of-line blocking, so one slow or lossy client cannot delay others. Loss is handled by the application: sequence numbers detect gaps, and A/B feeds or a TCP retransmission/snapshot service recover them.

## Joining a Multicast Group · Medium

How does a host start receiving an IP multicast feed?

### Answer

The application sets `IP_ADD_MEMBERSHIP` on a UDP socket bound to the group's port, giving the group address and the local interface. The kernel then sends an IGMP membership report, and switches (via IGMP snooping) and routers (via PIM) start forwarding that group's traffic to the host. The NIC also programs its multicast filter for the group's MAC address. Leaving sends an IGMP leave so traffic stops.

## Non-blocking Sockets · Easy

What does putting a socket in non-blocking mode change?

### Answer

Calls that would otherwise sleep, like `recv` with no data or `send` with a full buffer, return immediately with `EAGAIN`/`EWOULDBLOCK`. The program then polls the socket itself or uses a readiness API (`epoll`) to know when to retry. This lets one thread serve many sockets or spin on a socket without ever being descheduled.

## select vs poll vs epoll · Medium

Compare `select`, `poll` and `epoll`.

### Answer

`select` passes fixed-size bitsets (usually limited to 1024 descriptors) and both it and `poll` pass the whole interest set to the kernel on every call and scan it, so each call is O(n). `poll` removes the descriptor limit by using an array. `epoll` keeps the interest set in the kernel (`epoll_ctl`) and `epoll_wait` returns only ready descriptors, so the cost scales with activity rather than the number of sockets; it also supports edge-triggered mode.

## Kernel Bypass · Hard

What is kernel bypass networking (e.g. DPDK, Solarflare OpenOnload/ef_vi), and why does it reduce latency?

### Answer

The NIC's receive and transmit rings are mapped into user space, and the application (or a user-space TCP/UDP stack) polls them directly. This removes interrupts, system calls, data copies between kernel and user buffers, and the general-purpose kernel stack, cutting wire-to-application latency from several microseconds to around 1 µs or less (approximate). Onload does this transparently for existing socket code via `LD_PRELOAD`; DPDK and ef_vi expose raw packet APIs. The cost is a dedicated busy-polling core and a separate stack to manage.

## Interrupt Coalescing · Medium

What is NIC interrupt coalescing, and why do latency-sensitive systems often turn it off?

### Answer

The NIC waits for several packets or a short timer before raising one interrupt, reducing CPU overhead at high packet rates. The price is that a single packet can wait tens of microseconds before the kernel sees it. Low-latency hosts disable or minimise it (`ethtool -C`) or avoid interrupts entirely by busy polling or kernel bypass.
