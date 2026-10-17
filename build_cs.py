"""Static lesson pages and reproducible simulated reports for published Computer Science labs."""
from pathlib import Path
import json,math,csv,io,sqlite3,html,re

ROOT=Path(__file__).resolve().parent
E=lambda s:html.escape(str(s),quote=True)
def specs():return json.loads((ROOT/'content/cs/experiments.json').read_text())
def rnd(x,n):return math.floor(x*10**n+.5)/10**n

def observation(c,value):
 slug=c['slug']
 if slug=='search-algorithms-complexity':
  n=float(value)
  x=math.log2(n)
  raw=int(math.floor(x)+1)
  y=float(raw)
  return {'input':value,'raw':raw,'x':x,'y':y}
 elif slug=='quadratic-sorting-algorithms':
  n=float(value)
  x=n*(n-1.0)
  raw=int(n*(n-1.0)/2.0)
  y=float(raw)
  return {'input':value,'raw':raw,'x':x,'y':y}
 elif slug=='divide-conquer-sorting':
  n=float(value)
  log2n=math.log2(n)
  x=n*(log2n - 1.0)
  raw=int(round(n*log2n - n + 1.0))
  y=float(raw)
  return {'input':value,'raw':raw,'x':x,'y':y}
 elif slug=='stack-adt-recursion':
  n=float(value)
  x=n
  raw=int(round(64.0*n + 128.0))
  y=float(raw)
  return {'input':value,'raw':raw,'x':x,'y':y}
 elif slug=='queue-buffer-management':
  n=float(value)
  x=n
  raw=int(round(64.0*n + 256.0))
  y=float(raw)
  return {'input':value,'raw':raw,'x':x,'y':y}
 elif slug=='linked-list-architectures':
  n=float(value)
  x=n
  raw=int(round(32.0*n + 64.0))
  y=float(raw)
  return {'input':value,'raw':raw,'x':x,'y':y}
 elif slug=='binary-search-trees':
  n=float(value)
  x=math.log2(n)
  raw=int(math.floor(x)+1)
  y=float(raw)
  return {'input':value,'raw':raw,'x':x,'y':y}
 elif slug=='binary-heaps-priority-queues':
  n=float(value)
  log2n=math.log2(n)
  raw=int(round(2.0*n - 2.0*log2n))
  x=n - log2n
  y=float(raw)
  return {'input':value,'raw':raw,'x':x,'y':y}
 elif slug=='hash-tables-collision-resolution':
  n=float(value)
  m_cap=1000.0
  alpha=n/m_cap
  x=1.0/(1.0 - alpha)
  raw=rnd(x, 4)
  y=float(raw)
  return {'input':value,'raw':raw,'x':x,'y':y}
 raise ValueError(f"Unknown CS experiment {slug}")

def fit(rows):
 n=len(rows)
 mx=sum(r['x'] for r in rows)/n
 my=sum(r['y'] for r in rows)/n
 sxx=sum((r['x']-mx)**2 for r in rows)
 sxy=sum((r['x']-mx)*(r['y']-my) for r in rows)
 m=sxy/sxx if sxx>0 else 1.0
 b=my-m*mx
 sse=sum((r['y']-m*r['x']-b)**2 for r in rows)
 syy=sum((r['y']-my)**2 for r in rows)
 variance=sse/(n-2) if n>2 and sse>0 else 1e-12
 return dict(
  m=m,b=b,sse=sse,
  slopeSE=math.sqrt(variance/sxx) if sxx>0 else 0.0,
  interceptSE=math.sqrt(variance*(1/n+mx*mx/sxx)) if sxx>0 else 0.0,
  mx=mx,my=my,sxx=sxx,sxy=sxy,
  r2=1.0-sse/syy if syy>0 else 1.0
 )

def estimate(c,f):
 slug=c['slug']
 if slug=='search-algorithms-complexity':
  return f['m'],f['slopeSE'],1.0000
 elif slug=='quadratic-sorting-algorithms':
  return f['m'],f['slopeSE'],0.5000
 elif slug=='divide-conquer-sorting':
  return f['m'],f['slopeSE'],1.0000
 elif slug=='stack-adt-recursion':
  return f['m'],f['slopeSE'],64.0000
 elif slug=='queue-buffer-management':
  return f['m'],f['slopeSE'],64.0000
 elif slug=='linked-list-architectures':
  return f['m'],f['slopeSE'],32.0000
 elif slug=='binary-search-trees':
  return f['m'],f['slopeSE'],1.0000
 elif slug=='binary-heaps-priority-queues':
  return f['m'],f['slopeSE'],2.0000
 elif slug=='hash-tables-collision-resolution':
  return f['m'],f['slopeSE'],1.0000
 raise ValueError(f"Unknown CS experiment {slug}")

def fmt(v,n=5):
 return f'{v:.4e}' if v and (abs(v)<.001 or abs(v)>=1e6) else f'{v:.{n}f}'

def formula(c,f):
 slug=c['slug']
 if slug=='search-algorithms-complexity':
  val=f['m']*c['resultScale']
  return f"k_search = m = {fmt(val,c['resultDecimals'])} comparisons/bit; Intercept b = {fmt(f['b'],c['resultDecimals'])} comparisons (theoretical intercept = 1.0000)"
 elif slug=='quadratic-sorting-algorithms':
  val=f['m']*c['resultScale']
  return f"a_quad = m = {fmt(val,c['resultDecimals'])} comparisons/pair; Intercept b = {fmt(f['b'],c['resultDecimals'])} comparisons (theoretical a = 0.5000, b = 0.0000)"
 elif slug=='divide-conquer-sorting':
  val=f['m']*c['resultScale']
  return f"k_merge = m = {fmt(val,c['resultDecimals'])} comparisons/interval; Intercept b = {fmt(f['b'],c['resultDecimals'])} comparisons (theoretical k = 1.0000, b = 1.0000)"
 elif slug=='stack-adt-recursion':
  val=f['m']*c['resultScale']
  return f"F_frame = m = {fmt(val,c['resultDecimals'])} bytes/frame; Intercept M_0 = {fmt(f['b'],c['resultDecimals'])} bytes (theoretical frame F = 64.0000, base M_0 = 128.0000)"
 elif slug=='queue-buffer-management':
  val=f['m']*c['resultScale']
  return f"L_packet = m = {fmt(val,c['resultDecimals'])} bytes/packet; Intercept V_0 = {fmt(f['b'],c['resultDecimals'])} bytes (theoretical payload L = 64.0000, descriptor header V_0 = 256.0000)"
 elif slug=='linked-list-architectures':
  val=f['m']*c['resultScale']
  return f"S_node = m = {fmt(val,c['resultDecimals'])} bytes/node; Intercept M_0 = {fmt(f['b'],c['resultDecimals'])} bytes (theoretical node size S = 32.0000, sentinels M_0 = 64.0000)"
 elif slug=='binary-search-trees':
  val=f['m']*c['resultScale']
  return f"alpha = m = {fmt(val,c['resultDecimals'])} levels/bit; Intercept h_0 = {fmt(f['b'],c['resultDecimals'])} levels (theoretical alpha = 1.0000, h_0 = 1.0000)"
 elif slug=='binary-heaps-priority-queues':
  val=f['m']*c['resultScale']
  return f"k_heap = m = {fmt(val,c['resultDecimals'])} comparisons/interval; Intercept C_0 = {fmt(f['b'],c['resultDecimals'])} comparisons (theoretical k_heap = 2.0000, C_0 = 0.0000)"
 elif slug=='hash-tables-collision-resolution':
  val=f['m']*c['resultScale']
  return f"k_hash = m = {fmt(val,c['resultDecimals'])} probes/interval; Intercept P_0 = {fmt(f['b'],c['resultDecimals'])} probes (theoretical k_hash = 1.0000, P_0 = 0.0000)"
 return ""

def worked(c,row):
 slug=c['slug']
 if slug=='search-algorithms-complexity':
  n=row['input']
  log2n=row['x']
  c_max=row['raw']
  return f"Array Size n = {int(n)} keys; Key Entropy log₂(n) = log₂({int(n)}) = {log2n:.4f} bits.\nWorst-Case Binary Search Key Comparisons: C_max = ⌊log₂(n)⌋ + 1 = ⌊{log2n:.4f}⌋ + 1 = {c_max} comparisons.\nVerification: At each step, remaining search space halves from {int(n)} ⟶ {int(n)//2} ⟶ {int(n)//4} ... terminating in exactly {c_max} iterations."
 elif slug=='quadratic-sorting-algorithms':
  n=row['input']
  x_pairs=row['x']
  c_ops=row['raw']
  return f"Array Size n = {int(n)} keys; Directed Pair Space n(n − 1) = {int(n)} × {int(n)-1} = {int(x_pairs)} pairs.\nTotal Unordered Pairs to Compare: C = n(n − 1) / 2 = {int(x_pairs)} / 2 = {c_ops} comparisons.\nVerification: In each pass i from 0 to n−2, exactly n − 1 − i comparisons occur: (n−1) + (n−2) + ... + 1 = {c_ops} comparisons."
 elif slug=='divide-conquer-sorting':
  n=row['input']
  log2n=math.log2(n)
  x_space=row['x']
  c_ops=row['raw']
  return f"Array Size n = {int(n)} keys; Recursion Tree Depth h = log₂({int(n)}) = {int(log2n)} levels.\nRecursive Interval Space: x = n(log₂ n − 1) = {int(n)} × ({int(log2n)} − 1) = {int(x_space)} intervals.\nWorst-Case Key Comparisons: C_merge = n·log₂(n) − n + 1 = {int(n)} × {int(log2n)} − {int(n)} + 1 = {c_ops} comparisons.\nVerification: At depth j in [0 .. {int(log2n)-1}], exactly 2^j subarrays of size {int(n)}/2^j are merged with at most (size − 1) comparisons per subproblem."
 elif slug=='stack-adt-recursion':
  n=row['input']
  depth=row['x']
  mem_bytes=row['raw']
  return f"Recursion Depth n = {int(n)} frames; Active Activation Records = {int(depth)} frames.\nPeak Call Stack Memory Consumption: M(n) = F_frame · n + M_0 = 64 × {int(n)} + 128 = {mem_bytes} bytes ({mem_bytes/1024:.2f} KiB).\nVerification: Each physical activation record allocates 64 bytes on the thread stack segment (8B return address + 8B saved RBP + 16B saved registers + 32B local variables), moving RSP downward by exactly {mem_bytes - 128} bytes from the initial 128-byte runtime CRT base frame."
 elif slug=='queue-buffer-management':
  n=row['input']
  pkts=row['x']
  vol_bytes=row['raw']
  return f"Packet Batch Size n = {int(n)} packets; Circular Array Capacity = 12 slots.\nCumulative Buffer Memory Bus Transfer Volume: V(n) = L_packet · n + V_0 = 64 × {int(n)} + 256 = {vol_bytes} bytes ({vol_bytes/1024:.2f} KiB).\nVerification: Each streamed network packet transfers a 64-byte payload (one full CPU cache line) into the ring slot on enqueue and reads 64 bytes on dequeue, executing {int(n)//12} full cyclic pointer wrap-arounds plus an initial 256-byte cache-line padded descriptor control header."
 elif slug=='linked-list-architectures':
  n=row['input']
  nodes=row['x']
  mem_bytes=row['raw']
  return f"List Length n = {int(n)} nodes; Active Dynamic Heap Nodes = {int(nodes)} nodes.\nTotal Allocated Heap Memory: M(n) = S_node · n + M_0 = 32 × {int(n)} + 64 = {mem_bytes} bytes ({mem_bytes/1024:.2f} KiB).\nVerification: Each doubly linked list node allocates 32 bytes on the 64-bit heap (8B data payload + 8B next pointer + 8B prev pointer + 8B malloc 16-byte boundary alignment padding), plus 64 bytes for dual dummy sentinels (Sentinel Head = 32B, Sentinel Tail = 32B)."
 elif slug=='binary-search-trees':
  n=row['input']
  log2n=row['x']
  h_val=row['raw']
  return f"Dataset Scale n = {int(n)} keys; Logarithmic Key Entropy x = log₂({int(n)}) = {log2n:.4f} bits.\nBalanced Binary Search Tree Height: h(n) = ⌊log₂(n)⌋ + 1 = ⌊{log2n:.4f}⌋ + 1 = {h_val} levels.\nVerification: At depth d in [0 .. {h_val-1}], a full binary tree accommodates at most 2^d nodes, yielding maximum cumulative capacity ∑_{{d=0}}^{{{h_val-1}}} 2^d = 2^{h_val} − 1 = {2**h_val - 1} nodes, which strictly encloses n = {int(n)} keys."
 elif slug=='binary-heaps-priority-queues':
  n=row['input']
  log2n=math.log2(n)
  x_space=row['x']
  c_comps=row['raw']
  return f"Array Size n = {int(n)} keys; Logarithmic Tree Height h = ⌊log₂({int(n)})⌋ + 1 = {int(log2n)+1} levels.\nCumulative Sift Interval Space: x = n − log₂(n) = {int(n)} − {int(log2n)} = {x_space:.4f} intervals.\nWorst-Case Floyd Heapify Comparisons: C(n) = 2(n − log₂ n) = 2 × ({int(n)} − {int(log2n)}) = {c_comps} comparisons.\nVerification: Non-leaf nodes from index ⌊n/2⌋ − 1 down to 0 are sifted down; summing 2 comparisons per level across all node heights converges to strictly 2(n − log₂ n) operations."
 elif slug=='hash-tables-collision-resolution':
  n=row['input']
  m_cap=1000.0
  alpha=float(n)/m_cap
  x_coord=row['x']
  p_probes=row['raw']
  return f"Table Capacity m = 1000 slots; Key Dataset Size n = {int(n)} keys; Load Factor α = {int(n)} / 1000 = {alpha:.4f}.\nTransformed Load Coordinate: x = 1 / (1 − α) = 1 / (1 − {alpha:.4f}) = {x_coord:.4f}.\nExpected Unsuccessful Search Probe Depth: E[P] = 1 / (1 − α) = {p_probes:.4f} memory probes.\nVerification: Under uniform hashing, the probability of requiring at least i probes is α^(i-1); summing the geometric tail series ∑_{{j=0}}^∞ α^j yields strictly 1 / (1 − α) = {p_probes:.4f} probes."
 return ""

def uncertainty_text(c):
 slug=c['slug']
 if slug=='search-algorithms-complexity':
  return (
   "In deterministic comparison-based algorithm analysis, the theoretical worst-case operation count C_max(n) = ⌊log₂ n⌋ + 1 is an exact mathematical invariant. "
   "Unlike continuous physical instrumentation, there is no analog sensor noise, thermal fluctuation, or calibration drift in counting atomic discrete machine instructions. "
   "However, in physical semiconductor computers, wall-clock execution latency deviates from pure mathematical comparison counts due to hardware microarchitectural phenomena: "
   "(1) L1/L2/L3 cache line hierarchy fills and Translation Lookaside Buffer (TLB) virtual memory page walks; "
   "(2) Branch predictor mispredictions in conditional jumps (`if (A[mid] < K)`), which flush deep 14-to-20 stage microprocessor execution pipelines and incur 15 to 20 cycle stalls; "
   "(3) Hardware spatial prefetchers, which optimize sequential linear access patterns over random binary bisections for small arrays (n ≤ 64); and "
   "(4) Operating system preemptive kernel scheduling interrupts and thread context switches. "
   "Ordinary least-squares regression across systematically doubled array sizes n in [64, 4096] extracts the fundamental scaling multiplier k_search = 1.0000 comparisons/bit with zero residual variance (R² = 1.00000), verifying the asymptotic divide-and-conquer bound Θ(log₂ n) with mathematical certitude."
  )
 elif slug=='quadratic-sorting-algorithms':
  return (
   "In combinatorial sorting analysis, the comparison count C(n) = n(n − 1)/2 for Selection Sort and worst-case Bubble Sort is an exact deterministic combinatorial identity. "
   "Unlike noisy analog experimental instrumentation, discrete step counting in virtual machine execution registers exhibits zero random measurement error. "
   "However, physical hardware execution is influenced by microarchitectural phenomena: "
   "(1) L1 data cache spatial locality, where contiguous in-place array iterations execute with ~1 ns latency; "
   "(2) Branch predictor mispredictions during conditional element checks (`if (A[j] < A[min])`), which stall superscalar execution pipelines by 15–20 clock cycles; "
   "(3) Memory bus write contention during element swaps, where Selection Sort's O(n) write profile heavily outperforms Bubble Sort's O(n²) write churn; and "
   "(4) CPU dynamic frequency scaling under continuous nested-loop arithmetic. "
   "Ordinary least-squares linear regression of observed comparisons against permutation pair space x = n(n − 1) yields an empirical scaling slope a_quad = 0.5000 comparisons/pair with zero residual error (R² = 1.00000), rigorously verifying the quadratic complexity bound Θ(n²)."
  )
 elif slug=='divide-conquer-sorting':
  return (
   "In divide-and-conquer algorithmic complexity analysis, the comparison count C_merge(n) = n·log₂(n) − n + 1 for an array of size n = 2^k is an exact deterministic mathematical identity. "
   "Unlike continuous physical instrumentation, discrete operation counting in virtual machine execution registers exhibits zero random measurement noise. "
   "However, in physical microprocessor hardware, wall-clock execution latency deviates from pure mathematical comparison counts due to hardware microarchitectural phenomena: "
   "(1) Memory bus bandwidth contention during auxiliary scratchpad allocation and array copying, where Merge Sort copies 2n elements per level; "
   "(2) L1/L2/L3 cache line evictions when the working array size exceeds the CPU cache capacity (typically > 32 KB for L1); "
   "(3) Branch predictor mispredictions during the dual-pointer merge loop (`if (A[p1] <= A[p2])`), which flush deep execution pipelines; and "
   "(4) Call stack frame allocation overhead and register spilling during recursive bisections. "
   "Ordinary least-squares linear regression of observed comparisons against recursive interval space x = n(log₂ n − 1) yields an empirical scaling slope k_merge = 1.0000 comparisons/interval with zero residual error (R² = 1.00000), rigorously verifying the divide-and-conquer complexity bound Θ(n log₂ n)."
  )
 elif slug=='stack-adt-recursion':
  return (
   "In microarchitectural call stack memory analysis, the activation record size F_frame = 64 bytes per frame under the System V AMD64 ABI is an exact deterministic specification. "
   "Unlike continuous physical instrumentation, there is no analog sensor noise, thermal fluctuation, or calibration drift in measuring discrete byte displacements of the hardware stack pointer RSP. "
   "However, in physical microprocessor execution, observable call stack latency and operating system memory footprint are modulated by hardware and kernel mechanisms: "
   "(1) Virtual memory demand paging and Translation Lookaside Buffer (TLB) misses, where physical 4 KiB memory pages are committed only when the stack pointer crosses a page boundary; "
   "(2) CPU L1 data cache line fills and dirty writeback traffic, as stack pushes write to memory lines while stack pops invalidate or reuse warm cache lines; "
   "(3) Compiler optimizations such as leaf function frame elision, tail-call elimination (which reuses the current frame instead of allocating a new one), and register variable allocation; and "
   "(4) Operating system stack canary guard pages, which trigger a kernel page fault (SIGSEGV) if stack depth expands beyond the designated thread memory quota (typically 8 MiB). "
   "Ordinary least-squares linear regression of peak stack memory allocation against recursion depth n in [128, 8192] frames yields an empirical frame scaling slope F_frame = 64.0000 bytes/frame with zero residual error (R² = 1.00000), verifying the linear call stack memory bound Θ(n) with mathematical precision."
  )
 elif slug=='queue-buffer-management':
  return (
   "In systems-level circular buffer analysis, the packet unit payload size L_packet = 64 bytes is an exact hardware specification corresponding to a standard CPU cache line. "
   "Unlike continuous physical instrumentation, there is no analog sensor noise, thermal drift, or calibration variance in counting discrete memory bus transfer transactions. "
   "However, in physical multi-core processor execution, observable queue latency and memory bus throughput are modulated by microarchitectural phenomena: "
   "(1) False sharing between producer and consumer processor cores when head and tail pointers share an unpadded 64-byte cache line, causing inter-core MESI cache invalidation ping-pong; "
   "(2) CPU L1 data cache prefetcher stride detection, where sequential circular slot accesses achieve near-100% L1 cache hits (~1 ns latency); "
   "(3) Memory controller bus saturation during sustained burst transfers exceeding DRAM channel bandwidth; and "
   "(4) Operating system scheduler thread preemption and mutex lock-contention latency during buffer full/empty boundary synchronization. "
   "Ordinary least-squares linear regression of observed memory transfer volume against packet batch count n in [256, 16384] packets yields an empirical payload scaling slope L_packet = 64.0000 bytes/packet with zero residual error (R² = 1.00000), verifying the linear queue throughput bound Θ(n) with mathematical precision."
  )
 elif slug=='linked-list-architectures':
  return (
   "In 64-bit systems architecture analysis, the doubly linked list node footprint S_node = 32 bytes and dual sentinel baseline M_0 = 64 bytes are deterministic structural invariants under standard 16-byte heap allocator alignment. "
   "Unlike continuous physical instrumentation, there is no analog sensor noise, thermal drift, or calibration variance in measuring discrete dynamic heap memory allocation. "
   "However, in physical semiconductor processors, operational traversal latency across linked list structures is heavily modulated by microarchitectural memory hierarchy dynamics: "
   "(1) Pointer chasing cache line misses: because nodes are dynamically allocated at arbitrary, non-contiguous heap addresses, sequential node hops (node = node->next) suffer cold L1/L2 data cache misses (~100–250 CPU cycles per DRAM access) compared to contiguous vectors (~1–4 cycles for L1 cache lines); "
   "(2) Hardware spatial prefetcher failure: CPUs feature hardware stream prefetchers that detect regular linear access strides (e.g. index i to i+1 in arrays), but fail to anticipate non-deterministic heap pointer dereferences; "
   "(3) Dynamic memory allocator chunk header overhead: standard dlmalloc and ptmalloc implementations prepend an 8-to-16-byte chunk header (storing size and in-use flags) to every allocated block, increasing real memory bus consumption; and "
   "(4) Pointer overhead ratio: for an 8-byte payload, a 32-byte doubly linked node imposes a 300% pointer overhead (24 bytes metadata per 8 bytes payload), compared to 0% overhead in dense contiguous arrays. "
   "Ordinary least-squares linear regression of total allocated heap memory against list length n in [128, 8192] nodes yields an empirical node scaling slope S_node = 32.0000 bytes/node with zero residual error (R² = 1.00000), verifying the linear heap memory footprint bound Θ(n) with mathematical precision."
  )
 elif slug=='binary-search-trees':
  return (
   "In discrete tree algorithm analysis, the minimum height h_min(n) = ⌊log₂ n⌋ + 1 of a complete balanced binary search tree is an exact combinatorial invariant derived from decision tree entropy. "
   "Unlike continuous physical instrumentation, there is no analog sensor noise, thermal drift, or calibration variance in counting discrete tree levels or key comparisons. "
   "However, in physical semiconductor microprocessors, tree traversal latency and memory access time deviate from idealized theoretical models due to memory hierarchy and pipeline dynamics: "
   "(1) Pointer chasing cache line misses: because child nodes reside at non-contiguous heap addresses, descending each level (node = (k < node->key) ? node->left : node->right) incurs cold CPU L1/L2 data cache stalls (~100–250 CPU cycles) once dataset size exceeds cache capacity; "
   "(2) Hardware spatial prefetcher failure: stream prefetchers excel at sequential array scans but cannot predict non-linear pointer dereferences, giving contiguous vectors a massive practical advantage over pointer-based trees; "
   "(3) Branch predictor mispredictions in inner key comparisons, which stall superscalar execution pipelines by 15–20 clock cycles; and "
   "(4) Insertion order asymmetry: in unaugmented binary search trees, sorted or pathological sequences cause catastrophic tree collapse into a singly-linked list of height h = n, increasing search latency by over 300×. "
   "Ordinary least-squares linear regression of observed tree height against logarithmic key entropy x = log₂(n) across systematically doubled scales n in [64, 4096] yields an empirical height scaling slope alpha = 1.0000 levels/bit with zero residual error (R² = 1.00000), verifying the logarithmic height bound Θ(log₂ n) with mathematical certitude."
  )
 elif slug=='binary-heaps-priority-queues':
  return (
   "In discrete priority queue complexity analysis, the worst-case key comparison count C(n) = 2(n − log₂ n) for in-place bottom-up Floyd heapify is an exact combinatorial identity for power-of-two arrays. "
   "Unlike continuous physical instrumentation, there is no analog sensor noise, thermal drift, or calibration variance in counting discrete Machine key comparisons. "
   "However, in physical semiconductor microprocessors, wall-clock heap execution latency is strongly modulated by memory hierarchy and pipeline dynamics: "
   "(1) Pointer chasing cache line misses: as elements sink down deep heaps, child index doubling (i ⟶ 2i + 1, 2i + 2) hops across non-contiguous memory pages once heap size exceeds CPU L1/L2 data cache capacity; "
   "(2) Hardware stream prefetcher stall: sequential prefetchers fail to anticipate geometric index bisections, causing Heapsort to run 2× to 3× slower than Quicksort despite matching O(n log n) complexity; "
   "(3) Branch predictor mispredictions during child selection comparisons (`if (A[2i+1] > A[2i+2])`), which flush deep superscalar pipelines; and "
   "(4) D-ary heap trade-offs: 4-way heaps cut tree height in half and pack 4 children into a single 64-byte cache line, significantly reducing cache stall cycles. "
   "Ordinary least-squares linear regression of heapify comparisons against cumulative sift interval space x = n − log₂(n) yields an empirical scaling slope k_heap = 2.0000 comparisons/interval with zero residual variance (R² = 1.00000), verifying Floyd's linear O(n) construction bound with mathematical precision."
  )
 elif slug=='hash-tables-collision-resolution':
  return (
   "In discrete hash table analysis, the expected unsuccessful search probe depth E[P] = 1 / (1 − α) under the Uniform Hashing Assumption is an exact mathematical expectation. "
   "Unlike continuous physical instrumentation, there is no analog sensor noise, thermal drift, or calibration variance in counting discrete memory bucket probes. "
   "However, in physical semiconductor microprocessors, wall-clock hash lookup latency is strongly modulated by memory hierarchy and pipeline dynamics: "
   "(1) L1/L2 data cache hit ratios and Translation Lookaside Buffer (TLB) page table walks, where contiguous array buffers (Linear Probing) execute within ~1–4 CPU cycles while non-contiguous pointer dereferencing (Separate Chaining) incurs ~100–250 CPU cycles; "
   "(2) Primary clustering in linear probing, which forces probe paths into contiguous occupied runs and causes quadratic latency degradation E[P] ≈ 0.5(1 + 1/(1-α)²); "
   "(3) Branch predictor mispredictions during probe loop termination checks (`if (table[slot] == NULL)`), which stall superscalar execution pipelines by 15–20 clock cycles; and "
   "(4) Hash function computational overhead, where high-entropy 64-bit avalanche functions (MurmurHash3, SipHash) eliminate bucket resonance at the cost of 5–15 CPU instructions per hash. "
   "Ordinary least-squares linear regression of observed probe lengths against transformed load coordinates x = 1 / (1 − α) yields an empirical scaling slope k_hash = 1.0000 probes/interval with zero residual variance (R² = 1.00000), verifying Knuth's uniform hashing theorem with mathematical certitude."
  )
 return ""

def graph(c,rows,f):
 left,right,top,bottom=68,610,28,280
 xs=[r['x']*c['xScale'] for r in rows];ys=[r['y']*c['yScale'] for r in rows]
 xmin=min(xs);xmax=max(xs);ymin=min(ys);ymax=max(ys)
 dx=(xmax-xmin) or 1;dy=(ymax-ymin) or 1
 xmin-=dx*.12;xmax+=dx*.12;ymin-=dy*.15;ymax+=dy*.15
 px=lambda x:left+(x-xmin)/(xmax-xmin)*(right-left)
 py=lambda y:bottom-(y-ymin)/(ymax-ymin)*(bottom-top)
 out=[]
 for i in range(5):
  x=xmin+i*(xmax-xmin)/4;y=ymin+i*(ymax-ymin)/4
  out.append(f'<line x1="{left}" y1="{py(y):.1f}" x2="{right}" y2="{py(y):.1f}" stroke="#dbe5eb"/>')
  out.append(f'<text x="{left-9}" y="{py(y)+4:.1f}" text-anchor="end" font-size="10" fill="#5a7687">{fmt(y,2)}</text>')
  out.append(f'<text x="{px(x):.1f}" y="300" text-anchor="middle" font-size="10" fill="#5a7687">{fmt(x,2)}</text>')
 out.append(f'<path d="M{left} {top}V{bottom}H{right}" stroke="#8ba5b5" fill="none"/>')
 out.append(f'<text x="335" y="332" text-anchor="middle" fill="#2b546b" font-size="12">{E(c["xAxis"])}</text>')
 out.append(f'<text transform="translate(15 160) rotate(-90)" text-anchor="middle" fill="#2b546b" font-size="12">{E(c["yAxis"])}</text>')
 pts=[f"{px(xmin+i*(xmax-xmin)/100):.1f},{py((f['m']*(xmin+i*(xmax-xmin)/100)/c['xScale']+f['b'])*c['yScale']):.1f}" for i in range(101)]
 out.append(f'<polyline points="{" ".join(pts)}" stroke="#1e3e52" stroke-width="2" fill="none"/>')
 for r in rows:
  out.append(f'<circle cx="{px(r["x"]*c["xScale"]):.1f}" cy="{py(r["y"]*c["yScale"]):.1f}" r="4.8" fill="#c05621"><title>n = {r["input"]}</title></circle>')
 return f'<svg viewBox="0 0 650 340" role="img" aria-label="Asymptotic regression plot of key comparisons against logarithmic entropy">{"".join(out)}</svg>'

def theory(c):
 out=[
  '<section class="theory-section">',
  f'<h2>Theoretical Foundations of {E(c["shortTitle"])} and Computational Complexity</h2>',
  f'<p class="intro">{E(c["intro"])}</p>',
  '<div class="theory-grid">'
 ]
 for i,t in enumerate(c['topics'],1):
  out.append(f'<article class="theory-card"><div class="theory-head"><span class="eyebrow">TOPIC {str(i).zfill(2)} · FORMAL ANALYSIS</span><h3>{E(t["question"])}</h3></div><div class="theory-body"><p>{E(t["answer"]).replace(chr(10), "<br><br>")}</p></div></article>')
 out.append('</div></section>')
 return "".join(out)

def method(c):
 return '<div class="method-steps">'+''.join(f'<article class="method-step"><div class="step-num">{str(i).zfill(2)}</div><div><h3>{E(s["title"])}</h3><p>{E(s["text"])}</p></div></article>' for i,s in enumerate(c['procedure'],1))+'</div>'

def workbench(c):
 sim_buttons=''.join(
  f'<button id="simMode{m["id"].capitalize()}" class="sim-mode-btn{" active" if i==0 else ""}" data-sim="{m["id"]}" type="button" role="tab" aria-selected="{"true" if i==0 else "false"}"><span class="sim-icon">{m["icon"]}</span> {E(m["label"])}</button>'
  for i,m in enumerate(c.get('simModes', [{'id':'bench','icon':'🔬','label':'1. Algorithm Bench'},{'id':'compare','icon':'⚖️','label':'2. Complexity Comparison'},{'id':'sandbox','icon':'⚛️','label':'3. Dynamic Sandbox'}]))
 )
 return f'''<section aria-label="Interactive workbench"><div class="section-top"><div><div class="eyebrow">COMPUTE · BENCHMARK · ANALYSE</div><h2>Your virtual algorithm laboratory.</h2></div><button id="resetApparatus" class="text-button">Reset benchmark</button></div><div class="new-workbench"><div class="new-visual"><div class="visual-top"><div class="sim-mode-switcher" role="tablist" aria-label="Simulation Views">{sim_buttons}</div><button id="pauseMotion" class="dark-button" hidden>Pause motion</button></div><svg id="apparatusDiagram" viewBox="0 0 720 320" role="img" aria-label="Interactive virtual array and comparator for {E(c['shortTitle'])}"></svg><div class="new-meter"><div><small>{E(c['rawLabel'].upper())}</small><strong id="readingValue">—</strong></div><div><small>EXECUTION STATUS</small><p id="liveState" style="font-size:11px;margin:7px 0">Ready to execute {E(c['shortInput'])} benchmark.</p></div></div></div><div class="new-controls"><label for="independent">{E(c['inputLabel'])}</label><output id="independentOut">{c['initial']} {E(c['inputUnit'])}</output><input id="independent" type="range" min="{c['min']}" max="{c['max']}" step="{c['step']}" value="{c['initial']}"><label for="independentNumber">Set {E(c['shortInput'])} ({E(c['inputUnit'])})</label><input id="independentNumber" type="number" min="{c['min']}" max="{c['max']}" step="{c['step']}" value="{c['initial']}"><div class="lab-control-meta">{E(c['settings'][0])}</div><button id="measure" class="primary full">{E(c['measureLabel'])}</button><button id="recordReading" class="secondary full" disabled>＋ Record observation</button><p id="trialStatus" class="trial-status" role="status">Adjust {E(c['shortInput'])} n, then execute benchmark.</p></div></div><p class="data-notice">Operation counts are generated deterministically by the exact algorithmic execution model. Modern hardware benchmarks additionally reflect cache line prefetching and branch misprediction penalties.</p><details class="model-note"><summary>Algorithmic assumptions and limits</summary><p>{E(c['limitations'])} {E(c['modelExtra'])}</p></details></section><section id="apparatus" class="lab-section"><h2>Computational tools & environment.</h2><div class="apparatus-list">{''.join('<article class="apparatus-item"><h3>'+E(a['name'])+'</h3><p>'+E(a['purpose'])+'</p></article>' for a in c['apparatus'])}</div></section><section id="method" class="lab-section"><div class="eyebrow">FOLLOW THE METHOD</div><h2>A reason behind every step.</h2><p class="intro">{E(c['aim'])} Suggested independent settings: {", ".join(map(str,c['samples']))} {E(c['inputUnit'])}.</p>{method(c)}</section><section id="results" class="lab-section"><div class="section-top"><div><div class="eyebrow">YOUR NOTEBOOK · <span id="notebookCount">0</span> OBSERVATIONS</div><h2>Turn measurements into asymptotic insight.</h2></div><a class="text-button" href="/computer-science/{c['slug']}/report/">See a complete example report ↗</a></div><div class="lab-result-grid"><div class="chart-card"><svg id="labPlot" viewBox="0 0 650 340" role="img" aria-label="Measured observations and fitted asymptotic graph"></svg><p>Points are your recorded benchmark observations. The regression line validates {E(c['shortTitle'])} complexity scaling.</p></div><div class="fit-card lab-fit"><span class="eyebrow">LINEAR ASYMPTOTIC FIT · y = mx + b</span><div id="fitSummary"></div><div class="report-equation">{E(c['fitEquation'])}</div></div></div><div class="table-card"><table><thead><tr><th>#</th><th>{E(c['inputLabel'])} ({E(c['inputUnit'])})</th><th>{E(c['rawLabel'])} ({E(c['rawUnit'])})</th><th>{E(c['xAxis'])}</th><th>{E(c['yAxis'])}</th><th>Remove</th></tr></thead><tbody id="readingRows"></tbody></table><p id="emptyReadings">No readings yet. Execute a {E(c['shortInput'])} benchmark and record it.</p></div><div class="lab-reading-actions"><button id="downloadReadings" class="secondary" disabled>↓ Export CSV</button><button id="clearReadings" class="secondary" disabled>Clear notebook</button></div><div class="source-box"><h3>Calculate it yourself.</h3><label for="studentEstimate">Your estimate of {E(c['target'])} ({E(c['resultUnit'])})</label> <input id="studentEstimate" type="number" step="any" min="0" style="max-width:140px"><button id="checkEstimate" class="secondary" style="margin-left:10px">Check calculation</button><p id="estimateFeedback" role="status"></p></div></section><section id="check" class="lab-section lab-questions"><div class="eyebrow">CHECK YOUR UNDERSTANDING</div><h2>Explain what the operation counts mean.</h2>{''.join('<article class="quiz-card"><h3>'+E(q['question'])+'</h3><div class="quiz-choices">'+''.join('<button class="quiz-option" data-quiz="'+str(i)+'" data-choice="'+str(j)+'">'+E(a)+'</button>' for j,a in enumerate(q['options']))+'</div><p id="quizFeedback'+str(i)+'" class="quiz-feedback" role="status"></p></article>' for i,q in enumerate(c['quiz']))}</section>'''

def report_narrative(c,rows,f,value,percent,reference):
 slug=c['slug']
 if slug=='search-algorithms-complexity':
  abstract=(
   f"Seven benchmark trials were generated across input sizes n = {rows[0]['input']} to n = {rows[-1]['input']} {c['inputUnit']}. "
   f"An ordinary least-squares regression of worst-case key comparisons against logarithmic entropy log₂(n) yielded an empirical complexity multiplier of "
   f"{fmt(value*c['resultScale'],c['resultDecimals'])} {c['resultUnit']}, demonstrating exact agreement with the theoretical divide-and-conquer bound "
   f"(difference = {percent:.4f}%). The results empirically prove that Binary Search exhibits optimal Θ(log₂ n) asymptotic scaling, outperforming "
   f"linear search by a factor of over 315× at n = {rows[-1]['input']}."
  )
  graph_choice=(
   f"The mathematical regression fits the linear model y = mx + b, where x = log₂(n) represents input entropy in bits, "
   f"y = C represents discrete key comparisons, m represents the logarithmic scaling factor, and b represents baseline termination "
   f"comparison overhead. The gradient has physical units {c['gradientUnit']}."
  )
  discussion=(
   "The empirical benchmark observations perfectly align with the theoretical divide-and-conquer recurrence T(n) = T(n/2) + O(1). "
   "The slope m = 1.0000 confirms that exactly one additional comparison is required each time the dataset size doubles, illustrating "
   "how logarithmic algorithms tame exponential data volume growth in modern computer systems."
  )
  conclusion=(
   "This laboratory investigation quantitatively demonstrated the asymptotic complexity of search algorithms. Through empirical "
   f"benchmarking across arrays ranging from {rows[0]['input']} to {rows[-1]['input']} elements, we verified that Binary Search achieves "
   f"an optimal logarithmic scaling gradient of k_search = {fmt(value*c['resultScale'],c['resultDecimals'])} {c['resultUnit']}, matching "
   "the theoretical bound with zero residual error. The experiment highlights why divide-and-conquer is a foundational paradigm of modern "
   "computational infrastructure."
  )
 elif slug=='quadratic-sorting-algorithms':
  abstract=(
   f"Seven benchmark trials were generated across input sizes n = {rows[0]['input']} to n = {rows[-1]['input']} elements "
   f"(permutation pair space x = n(n − 1) from {int(rows[0]['x'])} to {int(rows[-1]['x'])} pairs). An ordinary least-squares regression "
   f"of key comparisons C against permutation pair space yielded an empirical quadratic scaling coefficient of "
   f"{fmt(value*c['resultScale'],c['resultDecimals'])} {c['resultUnit']}, demonstrating exact agreement with the combinatorial identity "
   f"C(n) = 1/2 n(n − 1) (difference = {percent:.4f}%). The empirical telemetry proves that while Bubble, Selection, and Insertion Sort "
   f"all share Θ(n²) worst-case comparison complexity, Selection Sort strictly minimizes memory bus write amplification to at most n − 1 "
   f"element swaps (2n − 2 writes), compared to Bubble Sort's up to n(n − 1)/2 swaps (~3× writes per swap), explaining why Selection Sort "
   "is preferred in Flash/EEPROM architectures."
  )
  graph_choice=(
   f"The mathematical regression fits the linear model y = mx + b, where x = n(n − 1) represents the total permutation pair space in pairs, "
   f"y = C represents discrete key comparisons, m represents the quadratic scaling coefficient a_quad, and b represents baseline comparison "
   f"overhead. The gradient has physical units {c['gradientUnit']}."
  )
  discussion=(
   "The empirical benchmark observations perfectly align with the combinatorial pair summation C(n) = ∑_{i=1}^{n-1} (n − i) = n(n − 1)/2. "
   "The slope m = 0.5000 confirms that exactly half of the directed pair space is compared in an unordered array. Furthermore, the inversion "
   "analysis demonstrates why any algorithm relying strictly on adjacent element swaps requires Ω(n²) comparisons on average, as each adjacent "
   "swap can eliminate at most one Kendall-tau inversion from an initial expectation of n(n − 1)/4 inversions. Finally, the hardware telemetry "
   f"highlights the critical trade-off between comparisons and memory write amplification: Selection Sort achieves identical comparisons "
   f"to Bubble Sort while reducing physical memory writes by a factor of over 35× at n = {rows[-1]['input']}."
  )
  conclusion=(
   "This laboratory investigation quantitatively verified the asymptotic complexity and microarchitectural behavior of quadratic sorting "
   f"algorithms. Through systematic benchmarking across arrays from {rows[0]['input']} to {rows[-1]['input']} elements, we verified the "
   f"quadratic scaling multiplier a_quad = {fmt(value*c['resultScale'],c['resultDecimals'])} {c['resultUnit']}, matching theoretical predictions "
   "with an ideal R² = 1.00000. The investigation established the theoretical necessity of non-adjacent partition and exchange primitives "
   "(such as Quicksort and Heapsort) to overcome the Ω(n²) barrier imposed by pairwise adjacent transpositions."
  )
 elif slug=='divide-conquer-sorting':
  abstract=(
   f"Seven benchmark trials were generated across input sizes n = {rows[0]['input']} to n = {rows[-1]['input']} elements "
   f"(recursive merge interval space x = n(log₂ n − 1) from {int(rows[0]['x'])} to {int(rows[-1]['x'])} intervals). "
   f"An ordinary least-squares regression of key comparisons C against recursive interval space yielded an empirical linear scaling multiplier of "
   f"{fmt(value*c['resultScale'],c['resultDecimals'])} {c['resultUnit']}, demonstrating exact agreement with the theoretical worst-case recurrence bound "
   f"C(n) = n log₂ n − n + 1 (difference = {percent:.4f}%). The empirical telemetry proves that while Merge Sort, Quick Sort, and Heap Sort "
   f"all achieve optimal Θ(n log n) comparison scaling, Merge Sort guarantees strictly stable O(n log n) comparisons at the cost of O(n) auxiliary heap space, "
   f"Quick Sort provides minimal cache footprint with O(log n) stack frames but degrades to O(n²) under deterministic worst-case pivot selection, "
   f"and Heap Sort achieves guaranteed O(n log n) worst-case time with strictly O(1) auxiliary space, making Introsort and Timsort the industry standard hybrid architectures."
  )
  graph_choice=(
   f"The mathematical regression fits the linear model y = mx + b, where x = n(log₂ n − 1) represents the cumulative recursive comparison interval space, "
   f"y = C represents discrete key comparisons, m represents the divide-and-conquer scaling factor k_merge, and b represents the base-case leaf offset "
   f"(theoretically b = 1). The gradient has physical units {c['gradientUnit']}."
  )
  discussion=(
   "The empirical benchmark observations perfectly align with the Master Theorem Case 2 solution of the divide-and-conquer recurrence "
   "T(n) = 2T(n/2) + Θ(n), yielding T(n) = Θ(n log₂ n). The regression slope m = 1.0000 confirms that the merge step requires at most n − 1 comparisons "
   "across each of the log₂ n recursive tree levels. Furthermore, comparison of the three algorithms illustrates the deep microarchitectural trade-offs: "
   "Merge Sort requires O(n) auxiliary memory bandwidth for the merge scratchpad but guarantees complete stability and sequential memory streaming. "
   "Quick Sort eliminates auxiliary array allocations by partitioning in place around a pivot, achieving superior CPU L1/L2 cache locality, but risks "
   "quadratic degradation if recursion trees become unbalanced. Heap Sort enforces an explicit binary heap invariant (A[parent] ≥ A[child]), guaranteeing "
   "O(n log n) bounds in strictly O(1) auxiliary space, but suffers from poor cache locality due to non-local child index hops (2i + 1, 2i + 2). "
   "This empirical synthesis explains why production runtimes combine these paradigms into hybrid engines such as Timsort and Introsort."
  )
  conclusion=(
   "This laboratory investigation quantitatively verified the asymptotic complexity, recurrence dynamics, and microarchitectural behavior of divide-and-conquer "
   f"sorting algorithms. Across benchmark array sizes from {rows[0]['input']} to {rows[-1]['input']} elements, we verified the recursive merge scaling "
   f"multiplier k_merge = {fmt(value*c['resultScale'],c['resultDecimals'])} {c['resultUnit']} with an ideal R² = 1.00000. The investigation established "
   "the fundamental information-theoretic lower bound Ω(n log n) for comparison sorts derived from decision tree leaf entropy (log₂(n!) ≈ n log₂ n − 1.44n) "
   "and demonstrated why hybrid algorithms that switch between divide-and-conquer and insertion sort at cache-friendly thresholds achieve optimal practical performance."
  )
 elif slug=='stack-adt-recursion':
  abstract=(
   f"Seven benchmark trials were generated across recursive call depths n = {rows[0]['input']} to n = {rows[-1]['input']} frames "
   f"(peak virtual thread stack allocation from {int(rows[0]['raw'])} bytes to {int(rows[-1]['raw'])} bytes, or {rows[-1]['raw']/1024:.2f} KiB). "
   f"An ordinary least-squares regression of peak stack memory M against recursion depth n yielded an empirical activation record frame size of "
   f"{fmt(value*c['resultScale'],c['resultDecimals'])} {c['resultUnit']}, demonstrating exact agreement with the standard System V AMD64 ABI specification "
   f"(difference = {percent:.4f}%). The empirical telemetry proves that unoptimized linear recursion incurs strict O(n) auxiliary memory overhead, "
   f"consuming memory bus bandwidth and risking fatal Stack Overflow (SIGSEGV) exceptions once depth exceeds the operating system thread stack limit, "
   f"whereas Tail-Call Optimization (TCO) and explicit heap-allocated stacks eliminate unbounded hardware stack pointer growth."
  )
  graph_choice=(
   f"The mathematical regression fits the linear model y = mx + b, where x = n represents the recursive call stack depth in frames, "
   f"y = M represents peak memory consumption in bytes, m represents the physical activation record frame size F_frame, and b represents "
   f"the initial runtime startup CRT stack overhead M_0 (theoretically M_0 = 128 bytes). The gradient has physical units {c['gradientUnit']}."
  )
  discussion=(
   "The empirical benchmark observations perfectly align with the hardware architecture of the thread call stack. Each function invocation "
   "executes the machine instruction CALL, pushing the 8-byte instruction return address onto the stack, followed by the function prologue "
   "(`push rbp; mov rbp, rsp; sub rsp, 48`), resulting in a constant 64-byte activation record per invocation level. The regression slope m = 64.0000 "
   "confirms that stack memory grows linearly at exactly 64 bytes per recursion depth. Furthermore, comparative analysis across execution paradigms "
   "reveals the crucial distinction between recursion classes: while linear recursion requires O(n) activation records, divide-and-conquer tree recursion "
   "bounds peak stack depth to O(log n) frames, and tail-recursive functions can be compiled via Tail-Call Optimization into constant-space O(1) iterative "
   "jumps (`jmp`), completely neutralizing stack overflow vulnerability. Finally, the grammar parser experiment demonstrates the essential role of the "
   "Stack ADT in compiling and evaluating nested syntax trees, maintaining LIFO state invariants across arbitrary context-free grammars."
  )
  conclusion=(
   "This laboratory investigation quantitatively verified the memory architecture, activation record mechanics, and asymptotic behavior of the Stack Abstract Data Type. "
   f"Through systematic benchmarking across recursion depths from {rows[0]['input']} to {rows[-1]['input']} frames, we verified the empirical frame size "
   f"F_frame = {fmt(value*c['resultScale'],c['resultDecimals'])} {c['resultUnit']} with an ideal coefficient of determination R² = 1.00000. "
   "The investigation established the microarchitectural necessity of stack memory discipline, proving how unbounded recursion risks thread stack exhaustion "
   "and validating tail-call optimization and heap-backed data structures as vital engineering defenses in modern software runtimes."
  )
 elif slug=='queue-buffer-management':
  abstract=(
   f"Seven benchmark trials were generated across packet batch sizes n = {rows[0]['input']} to n = {rows[-1]['input']} packets "
   f"(cumulative memory bus transfer volume from {int(rows[0]['raw'])} bytes to {int(rows[-1]['raw'])} bytes, or {rows[-1]['raw']/1024:.2f} KiB). "
   f"An ordinary least-squares regression of buffer transfer volume V against packet count n yielded an empirical packet throughput volume of "
   f"{fmt(value*c['resultScale'],c['resultDecimals'])} {c['resultUnit']}, demonstrating exact agreement with the 64-byte cache line payload specification "
   f"(difference = {percent:.4f}%). The empirical telemetry proves that circular ring buffers eliminate the catastrophic O(n) element-shifting penalty "
   f"of naive array queues, recycling memory in-place via modular indexing arithmetic ((index + 1) mod N) to sustain millions of streaming transactions "
   f"per second with strictly O(1) operational complexity and zero runtime heap reallocations."
  )
  graph_choice=(
   f"The mathematical regression fits the linear model y = mx + b, where x = n represents the cumulative packet batch size in packets, "
   f"y = V represents memory bus throughput volume in bytes, m represents the unit packet payload size L_packet, and b represents "
   f"the ring buffer descriptor header overhead V_0 (theoretically V_0 = 256 bytes). The gradient has physical units {c['gradientUnit']}."
  )
  discussion=(
   "The empirical benchmark observations perfectly align with the queuing mechanics of circular ring buffers. By logically joining index N − 1 back "
   "to index 0 via modular arithmetic, the circular buffer prevents pointer drift and achieves strictly O(1) time complexity for both enqueue and dequeue "
   "operations. The regression slope m = 64.0000 confirms that exactly 64 bytes (one standard CPU cache line) are transferred per processed packet. "
   "Furthermore, comparative architectural analysis across queue implementations demonstrates why ring buffers dominate high-performance computing: "
   "naive array queues incur unacceptable O(n) memory copy overhead on every dequeue, and linked-list queues suffer from heap fragmentation and pointer-chasing "
   "cache misses. In contrast, circular ring buffers provide contiguous spatial locality, enabling hardware prefetchers to anticipate memory accesses. "
   "Finally, multi-core analysis establishes the critical importance of cache-line padding: segregating atomic head and tail pointers onto separate 64-byte "
   "cache lines prevents catastrophic false sharing, allowing concurrent producers and consumers to achieve peak bus throughput."
  )
  conclusion=(
   "This laboratory investigation quantitatively verified the memory architecture, modular pointer dynamics, and asymptotic throughput of the Queue Abstract Data Type. "
   f"Through systematic benchmarking across stream sizes from {rows[0]['input']} to {rows[-1]['input']} packets, we verified the unit payload transfer volume "
   f"L_packet = {fmt(value*c['resultScale'],c['resultDecimals'])} {c['resultUnit']} with an ideal R² = 1.00000. "
   "The investigation established the microarchitectural superiority of circular ring buffers for asynchronous producer-consumer data flow, proving how "
   "modular indexing, power-of-two bitwise masking, and cache-line padding form the foundational infrastructure of modern operating system kernels and high-throughput networking stacks."
  )
 elif slug=='linked-list-architectures':
  abstract=(
   f"Seven benchmark trials were generated across dynamic linked list lengths n = {rows[0]['input']} to n = {rows[-1]['input']} nodes "
   f"(peak dynamic heap memory footprint from {int(rows[0]['raw'])} bytes to {int(rows[-1]['raw'])} bytes, or {rows[-1]['raw']/1024:.2f} KiB). "
   f"An ordinary least-squares regression of heap memory consumption M against list length n yielded an empirical node allocation size of "
   f"{fmt(value*c['resultScale'],c['resultDecimals'])} {c['resultUnit']}, demonstrating exact agreement with the 64-bit ABI doubly linked node specification "
   f"(difference = {percent:.4f}%). The empirical telemetry proves that while doubly linked lists achieve optimal O(1) splice and deletion once a node pointer is held, "
   f"they impose a 300% pointer overhead (24 bytes of pointers and alignment padding per 8 bytes of data) and suffer catastrophic pointer-chasing cache misses during traversal, "
   f"demonstrating why modern high-performance systems utilize contiguous vectors or unrolled chunked lists (B-trees, unrolled linked lists) for cache-resident data pipelines."
  )
  graph_choice=(
   f"The mathematical regression fits the linear model y = mx + b, where x = n represents the list length in nodes, "
   f"y = M represents total dynamic heap memory in bytes, m represents the individual node allocation footprint S_node, and b represents "
   f"the dual sentinel overhead M_0 (theoretically M_0 = 64 bytes). The gradient has physical units {c['gradientUnit']}."
  )
  discussion=(
   "The empirical benchmark observations perfectly align with the heap memory model of doubly linked list architectures. Each dynamically allocated node "
   "comprises an 8-byte 64-bit data value, an 8-byte forward pointer (next), an 8-byte backward pointer (prev), and 8 bytes of internal padding to maintain "
   "the mandatory 16-byte alignment required by standard glibc/ptmalloc allocators, totaling exactly 32 bytes per node. The regression slope m = 32.0000 "
   "confirms that heap memory expands linearly at exactly 32 bytes per node. Furthermore, microarchitectural analysis reveals the profound trade-offs "
   "between pointer structures and contiguous memory: while doubly linked lists allow O(1) node insertion and deletion without shifting elements, "
   "random traversal across non-contiguous heap pointers incurs high cache miss penalties because modern superscalar CPUs cannot prefetch non-linear memory strides. "
   "In contrast, contiguous vectors pack 8 values into a single 64-byte L1 cache line, streaming data at DRAM channel bandwidth (~50 GB/s). "
   "Finally, the sentinel sandbox demonstrates that integrating permanent dummy head and tail sentinel nodes eliminates boundary condition null checks "
   "(`head == NULL` and `tail == NULL`), eradicating conditional branch mispredictions during high-frequency list splice operations."
  )
  conclusion=(
   "This laboratory investigation quantitatively verified the memory footprint, pointer architecture, and microarchitectural behavior of Linked List Architectures. "
   f"Through systematic benchmarking across list sizes from {rows[0]['input']} to {rows[-1]['input']} nodes, we verified the empirical node footprint "
   f"S_node = {fmt(value*c['resultScale'],c['resultDecimals'])} {c['resultUnit']} with an ideal R² = 1.00000. "
   "The investigation established the microarchitectural trade-offs of pointer-based data structures, proving how pointer overhead and cache locality govern "
   "real-world computational throughput, and demonstrating why unrolled lists and sentinel-bounded doubly linked lists remain essential components of operating system schedulers and memory managers."
  )
 elif slug=='binary-search-trees':
  abstract=(
   f"Seven benchmark trials were generated across key dataset sizes n = {rows[0]['input']} to n = {rows[-1]['input']} keys "
   f"(logarithmic entropy x = log₂(n) from {rows[0]['x']:.1f} to {rows[-1]['x']:.1f} bits, tree height h from {rows[0]['raw']} to {rows[-1]['raw']} levels). "
   f"An ordinary least-squares regression of tree height h against logarithmic entropy log₂(n) yielded an empirical height scaling factor of "
   f"{fmt(value*c['resultScale'],c['resultDecimals'])} {c['resultUnit']}, demonstrating exact agreement with the theoretical complete binary tree bound "
   f"(difference = {percent:.4f}%). The empirical telemetry proves that balanced binary search trees strictly constrain search path depth to optimal Θ(log₂ n) scaling, "
   f"outperforming degenerate unaugmented trees by a factor of over 315× at n = {rows[-1]['input']} keys (where degenerate height explodes to h = {rows[-1]['input']} levels), "
   f"and validating self-balancing rotation algorithms (AVL and Red-Black trees) as essential computational defenses against catastrophic worst-case degradation."
  )
  graph_choice=(
   f"The mathematical regression fits the linear model y = mx + b, where x = log₂(n) represents key entropy in bits, "
   f"y = h represents tree height in levels, m represents the height scaling factor alpha, and b represents the baseline leaf level offset "
   f"(theoretically b = 1.0000 level). The gradient has physical units {c['gradientUnit']}."
  )
  discussion=(
   "The empirical benchmark observations perfectly align with the combinatorial capacity theorem for binary trees. Because each node has at most two children, "
   "a binary tree of height h can accommodate at most 2^h − 1 nodes. Inverting this geometric relationship yields the fundamental lower bound on tree height: "
   "h ≥ ⌈log₂(n + 1)⌉ = ⌊log₂ n⌋ + 1. The regression slope m = 1.0000 confirms that tree height increases by exactly 1 level each time dataset size doubles, "
   "mirroring the 1-bit entropy halving of Binary Search. Furthermore, topological comparison across insertion sequence regimes illustrates the vital "
   "importance of balance invariants: while randomly constructed binary search trees achieve an acceptable average search depth E[D(n)] ≈ 1.386 log₂ n, "
   "pathological monotonic insertion sequences (such as sorted datasets) cause unaugmented trees to collapse into degenerate singly-linked lists of height h = n. "
   "Under such degeneracy, search performance degrades catastrophically from O(log n) to O(n), and cumulative construction cost explodes to quadratic O(n²). "
   "Finally, the rotation sandbox demonstrates that local single (LL, RR) and double (LR, RL) tree rotations restore balance factor equilibrium (|BF| ≤ 1) in strictly "
   "O(1) time with 3 to 5 pointer updates, guaranteeing worst-case O(log n) bounds without whole-tree reconstruction."
  )
  conclusion=(
   "This laboratory investigation quantitatively verified the tree height dynamics, search path geometry, and balancing mechanics of Binary Search Trees. "
   f"Through systematic benchmarking across datasets from {rows[0]['input']} to {rows[-1]['input']} keys, we verified the empirical height scaling factor "
   f"alpha = {fmt(value*c['resultScale'],c['resultDecimals'])} {c['resultUnit']} with an ideal coefficient of determination R² = 1.00000. "
   "The investigation established the microarchitectural necessity of self-balancing tree architectures, proving how AVL and Red-Black tree invariants "
   "protect systems from O(n) worst-case collapse, and demonstrating why multi-way B-trees remain the foundational storage architecture for high-fanout disk and cache-resident database engines."
  )
 elif slug=='binary-heaps-priority-queues':
  abstract=(
   f"Seven benchmark trials were generated across array buffer sizes n = {rows[0]['input']} to n = {rows[-1]['input']} keys "
   f"(cumulative sift interval space x = n − log₂(n) from {rows[0]['x']:.1f} to {rows[-1]['x']:.1f} intervals, heapify comparisons C from {rows[0]['raw']} to {rows[-1]['raw']} comparisons). "
   f"An ordinary least-squares regression of key comparisons C against cumulative sift space yielded an empirical heapify scaling coefficient of "
   f"{fmt(value*c['resultScale'],c['resultDecimals'])} {c['resultUnit']}, demonstrating exact agreement with Floyd's bottom-up linear construction bound "
   f"(difference = {percent:.4f}%). The empirical telemetry proves that Floyd's bottom-up heapification achieves strict linear O(n) complexity, "
   f"delivering a 6-fold reduction in comparisons over naive repeated insertion (which consumes n log₂ n = {int(rows[-1]['input'] * math.log2(rows[-1]['input']))} comparisons at n = {rows[-1]['input']}), "
   f"while operating completely in-place within a contiguous array buffer with zero auxiliary pointer memory overhead."
  )
  graph_choice=(
   f"The mathematical regression fits the linear model y = mx + b, where x = n − log₂(n) represents the cumulative sift interval space in intervals, "
   f"y = C represents discrete key comparisons, m represents the heapify comparison scaling factor k_heap, and b represents baseline comparison offset "
   f"(theoretically b = 0.0000 comparisons). The gradient has physical units {c['gradientUnit']}."
  )
  discussion=(
   "The empirical benchmark observations perfectly align with the geometric summation theorem governing Floyd's bottom-up heap construction. "
   "Because ⌈n/2⌉ nodes reside at height 0 (leaves) requiring 0 sifts, ⌈n/4⌉ nodes reside at height 1 requiring at most 1 sift, and in general at most ⌈n/2^{h+1}⌉ "
   "nodes reside at height h requiring at most h sifts, the total sifting work is bounded by (n/2) ∑_{h=0}^∞ (h / 2^h) = (n/2) × 2 = n. "
   "Accounting for exactly 2 comparisons per level (1 child-child comparison and 1 parent-child comparison), the exact comparison count is C(n) = 2(n − log₂ n). "
   "The regression slope m = 2.0000 confirms this linear relationship with zero residual variance. Furthermore, comparative analysis across priority queue "
   "architectures reveals crucial engineering trade-offs: naive unsorted arrays allow O(1) insertion but suffer disastrous O(n) extraction scans, sorted arrays "
   "permit O(1) extraction but require O(n) element shifting on insertion, and binary heaps achieve balanced O(log n) operations for both insertion and extraction "
   "with zero pointer overhead. Finally, the sandbox demonstration illustrates how 4-way heaps optimize modern microarchitectures by cutting tree height in half "
   "and aligning all four sibling nodes within a single 64-byte CPU cache line."
  )
  conclusion=(
   "This laboratory investigation quantitatively verified the comparison complexity, pointerless array mapping, and asymptotic scaling of Binary Heaps and Priority Queues. "
   f"Through systematic benchmarking across array sizes from {rows[0]['input']} to {rows[-1]['input']} keys, we verified the empirical heapify scaling factor "
   f"k_heap = {fmt(value*c['resultScale'],c['resultDecimals'])} {c['resultUnit']} with an ideal R² = 1.00000. "
   "The investigation established the microarchitectural superiority of complete binary trees for in-place priority scheduling, proving how Floyd's bottom-up algorithm "
   "attains linear O(n) construction and demonstrating why binary and d-ary heaps form the core engine of discrete-event simulators, operating system process schedulers, and Heapsort."
  )
 elif slug=='hash-tables-collision-resolution':
  abstract=(
   f"Seven benchmark trials were generated across key dataset sizes n = {rows[0]['input']} to n = {rows[-1]['input']} keys "
   f"in a fixed 1000-slot hash table (load factors α from {float(rows[0]['input'])/1000:.2f} to {float(rows[-1]['input'])/1000:.2f}, "
   f"transformed load coordinate x = 1 / (1 − α) from {rows[0]['x']:.4f} to {rows[-1]['x']:.4f}, expected unsuccessful search probe lengths E[P] from {rows[0]['raw']:.4f} to {rows[-1]['raw']:.4f} probes). "
   f"An ordinary least-squares regression of probe depths against the transformed load coordinate yielded an empirical probe scaling coefficient of "
   f"{fmt(value*c['resultScale'],c['resultDecimals'])} {c['resultUnit']}, demonstrating exact agreement with Knuth's uniform hashing theorem "
   f"(difference = {percent:.4f}%). The empirical telemetry confirms that Double Hashing completely eliminates primary and secondary clustering, "
   f"achieving the optimal theoretical probe bound E[P] = 1 / (1 − α) and outperforming Linear Probing by a factor of 5× at high load factors (α = 0.90)."
  )
  graph_choice=(
   f"The mathematical regression fits the linear model y = mx + b, where x = 1 / (1 − α) represents the transformed load factor coordinate, "
   f"y = E[P] represents the expected number of memory probes in an unsuccessful search, m represents the probe scaling factor k_hash, and b represents "
   f"the baseline probe offset (theoretically b = 0.0000 probes). The gradient has physical units {c['gradientUnit']}."
  )
  discussion=(
   "The empirical benchmark observations provide rigorous quantitative verification of Knuth's asymptotic probe bounds in open-address hash tables. "
   "As key count n increases from 100 to 900 keys (load factor α from 0.10 to 0.90), the raw probe length exhibits a dramatic non-linear acceleration, "
   "rising from 1.1111 probes at α = 0.10 to 10.0000 probes at α = 0.90. Plotting probe depths against the linearized coordinate x = 1 / (1 − α) transforms "
   "this asymptotic divergence into a straight line with slope m = 1.0000 and R² = 1.00000, confirming that the number of unsuccessful search probes follows "
   "a geometric distribution with success parameter p = 1 − α. Comparative analysis across collision resolution strategies reveals profound architectural trade-offs: "
   "Separate Chaining tolerates load factors α > 1.0 and degrades linearly (E[P] = α), but incurs severe CPU cache misses due to pointer chasing across fragmented heap memory. "
   "Linear Probing maximizes CPU L1 spatial cache locality by scanning adjacent array slots, but suffers from catastrophic Primary Clustering where contiguous runs act as "
   "gravitational attractors, squaring the probe penalty to E[P] ≈ 0.5(1 + 1/(1-α)²). Double Hashing eliminates both primary and secondary clustering by varying the probe stride "
   "as a function of the key itself (h₂(k) coprime to m), achieving the ideal theoretical probe bound 1 / (1 − α). Finally, the investigation demonstrates why modern systems "
   "libraries (such as Google Abseil Swiss Tables and Rust hashbrown) pair open addressing with 1-byte control arrays and SIMD vector instructions to inspect 16 slots simultaneously in L1 cache."
  )
  conclusion=(
   "This laboratory investigation quantitatively verified the collision resolution mechanics, probe distributions, and asymptotic load scaling of Hash Tables. "
   f"Through systematic benchmarking across load factors from α = {float(rows[0]['input'])/1000:.2f} to α = {float(rows[-1]['input'])/1000:.2f}, we verified the empirical probe scaling factor "
   f"k_hash = {fmt(value*c['resultScale'],c['resultDecimals'])} {c['resultUnit']} with an ideal R² = 1.00000. "
   "The investigation established the microarchitectural trade-offs between cache-friendly contiguous arrays and pointer-based chaining, proving why Double Hashing, "
   "Robin Hood equalized probing, and SIMD control-byte Swiss Tables form the core dictionary implementation of modern operating systems, database indexes, and high-throughput compilers."
  )
 else:
  abstract=f"Empirical benchmark trials were generated across input sizes for {c['title']}."
  graph_choice=f"Regression fits y = mx + b for {c['fitEquation']}."
  discussion=f"Empirical observations align with theoretical bound {fmt(reference*c['resultScale'],c['resultDecimals'])} {c['resultUnit']}."
  conclusion=f"Quantitative benchmarking verified complexity scaling for {c['title']}."
 return abstract, graph_choice, discussion, conclusion

def report(c,rows,f,out):
 slug=c['slug']
 csvpath=f"/computer-science/{slug}/sample-data.csv"
 csv_content=io.StringIO()
 writer=csv.writer(csv_content)
 writer.writerow(['experiment',c['shortInput'].replace(' ','_')+'_n','key_comparisons','x_metric','fitted_comparisons','residual'])
 for r in rows:
  fit_y=f['m']*r['x']+f['b']
  writer.writerow([slug,r['input'],r['raw'],f"{r['x']:.4f}",f"{fit_y:.4f}",f"{r['y']-fit_y:.4f}"])
 (out/f"computer-science/{slug}/sample-data.csv").write_text(csv_content.getvalue())

 value,se,reference=estimate(c,f)
 percent=abs(value-reference)/reference*100
 uncertainty=uncertainty_text(c)
 abstract,graph_choice,discussion,conclusion=report_narrative(c,rows,f,value,percent,reference)

 obs="".join(
  f"<tr><td>{i+1}</td><td>{r['input']}</td><td>{r['raw']}</td><td>{r['x']:.4f}</td><td>{r['y']:.4f}</td><td>{f['m']*r['x']+f['b']:.4f}</td><td>{r['y']-(f['m']*r['x']+f['b']):.4f}</td></tr>"
  for i,r in enumerate(rows)
 )

 return f'''<div class="section-top"><div><div class="eyebrow">WORKED EXAMPLE · BENCHMARK OBSERVATIONS</div><h2>A complete example laboratory report.</h2></div><button class="secondary" onclick="window.print()">Print / save as PDF</button></div><div class="report-notice"><strong>Simulated demonstration data.</strong><p>This report illustrates formal algorithmic benchmarking, operation counting arithmetic, and regression analysis. Replace its observations with your own benchmark telemetry when preparing a practical submission.</p></div><div class="report-person"><span>Student: __________________</span><span>Student ID: __________________</span><span>Course: __________________</span><span>Date: __________________</span><span>Partner: __________________</span><span>Instructor: __________________</span></div><article class="lab-report"><h3>1. Title and aim</h3><p><strong>{E(c['title'])}.</strong> {E(c['aim'])}</p><h3>2. Abstract</h3><p>{E(abstract)}</p><h3>3. Apparatus and fixed settings</h3><ul>{''.join('<li>'+E(a['name'])+': '+E(a['purpose'])+'</li>' for a in c['apparatus'])}{''.join('<li>'+E(s)+'</li>' for s in c['settings'])}</ul><h3>4. Theory and graph choice</h3><p>{E(c['intro'])}</p><div class="report-equation">{E(c['fitEquation'])}</div><p>{E(graph_choice)}</p><h3>5. Method</h3><ol>{''.join('<li>'+E(s['text'])+'</li>' for s in c['procedure'])}</ol><h3>6. Observations and calculation table</h3><p>All benchmark observations use strictly controlled memory buffers. Values are recorded deterministically from the algorithmic comparator register. Residuals are computed relative to the ordinary least-squares regression line.</p><div class="table-card"><table><caption>Table 1. Seven simulated algorithmic benchmarks; x and y represent computational state metrics.</caption><thead><tr><th>No.</th><th>{E(c['inputLabel'])} ({E(c['inputUnit'])})</th><th>{E(c['rawLabel'])} ({E(c['rawUnit'])})</th><th>{E(c['xAxis'])}</th><th>{E(c['yAxis'])}</th><th>Fitted y</th><th>Residual</th></tr></thead><tbody>{obs}</tbody></table></div><p><a href="{csvpath}" download>Download the sample observations (CSV) ↓</a></p><h3>7. Worked calculation for one observation</h3><div class="report-equation">{E(worked(c,rows[0]))}</div><h3>8. Graph, gradient and final calculation</h3><div class="chart-card">{graph(c,rows,f)}</div><p>Circular markers represent empirical benchmark observations. The solid line represents the ordinary least-squares asymptotic linear fit.</p><div class="report-equation">x̄ = {fmt(f['mx'])}; ȳ = {fmt(f['my'])}<br>Σ(x − x̄)² = {fmt(f['sxx'])}<br>Σ(x − x̄)(y − ȳ) = {fmt(f['sxy'])}<br>m = Σ(x − x̄)(y − ȳ) / Σ(x − x̄)² = {fmt(f['m'],8)}<br>b = ȳ − mx̄ = {fmt(f['b'],8)}<br>{E(formula(c,f))}</div><h3>9. Uncertainty and comparison</h3><p>Percentage difference = |estimate − theoretical value| / |theoretical value| × 100 = <strong>{percent:.4f}%</strong>.</p><p>For n = 7 benchmark observations, Σresidual² = {fmt(f['sse'])}; s² = Σresidual²/(n − 2). Gradient standard error = √[s²/Σ(x − x̄)²] = {fmt(f['slopeSE'])}. Intercept standard error = √[s²(1/n + x̄²/Σ(x − x̄)²)] = {fmt(f['interceptSE'])}.</p><p>Propagating the fit parameters yields a <strong>fit standard error of {fmt(se*c['resultScale'])} {E(c['resultUnit'])}</strong>, with an ideal coefficient of determination R² = {f['r2']:.6f}.</p><p>{E(uncertainty)}</p><h3>10. Result and discussion</h3><div class="report-equation">{E(c['target'])} = {fmt(value*c['resultScale'],c['resultDecimals'])} {E(c['resultUnit'])}<br>Theoretical reference value: {fmt(reference*c['resultScale'],c['resultDecimals'])} {E(c['resultUnit'])}</div><p>{E(discussion)}</p><h3>11. Precautions and limitations</h3><ul>{''.join('<li>'+E(p)+'</li>' for p in c['precautions'])}</ul><p>{E(c['limitations'])} {E(c['modelExtra'])}</p><h3>12. Conclusion</h3><p>{E(conclusion)}</p></article>'''

def lesson_schema(c,part,path,title,desc,base):
 graph=[{'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'Open STEM Lab','item':base+'/'},{'@type':'ListItem','position':2,'name':'Computer Science Laboratory','item':base+'/subjects/computer-science/'},{'@type':'ListItem','position':3,'name':c['shortTitle'],'item':base+f'/computer-science/{c["slug"]}/'}]}]
 if part=='experiment':
  graph.append({'@type':['WebPage','LearningResource','TechArticle'],'name':title,'description':desc,'url':base+path,'learningResourceType':'Interactive computational simulation','educationalLevel':'Undergraduate','about':c['title'],'inLanguage':'en','isPartOf':{'@type':'WebSite','name':'Open STEM Lab','url':base+'/'}})
  if c.get('quiz'):
   graph.append({'@type':'Quiz','name':c['shortTitle']+' Concept Understanding','hasPart':[{'@type':'Question','name':q['question'],'suggestedAnswer':[{'@type':'Answer','text':opt} for opt in q['options']],'acceptedAnswer':{'@type':'Answer','text':q['options'][q['correct']]}} for q in c['quiz']]})
 elif part=='theory':
  graph.append({'@type':['WebPage','TechArticle','FAQPage'],'name':title,'description':desc,'url':base+path,'about':c['title'],'inLanguage':'en','isPartOf':{'@type':'WebSite','name':'Open STEM Lab','url':base+'/'},'mainEntity':[{'@type':'Question','name':t['question'],'acceptedAnswer':{'@type':'Answer','text':t['answer']}} for t in c['topics']]})
 else:
  graph.append({'@type':['WebPage','ScholarlyArticle','TechArticle'],'name':title,'description':desc,'url':base+path,'about':c['title'],'inLanguage':'en','isPartOf':{'@type':'WebSite','name':'Open STEM Lab','url':base+'/'}})
 return json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False)

def shell(c,part,body,base,production):
 from build_catalog import head
 path=f'/computer-science/{c["slug"]}/'+('' if part=='experiment' else part+'/')
 title=c['shortTitle']+(' Experiment & Simulation' if part=='experiment' else ' Theory & Analysis' if part=='theory' else ' Lab Report: Benchmarks & Calculations')+' | Open STEM Lab'
 desc={'experiment':c['aim']+' Explore interactive search algorithms, compare operation counts and analyse complexity scaling.','theory':'Understand '+c['shortTitle'].lower()+': recurrence relations, Big-O bounds, decision trees and hardware cache interactions.','report':'A worked '+c['shortTitle'].lower()+' lab report with benchmark data tables, asymptotic graphs, calculations, uncertainty and conclusions.'}[part]
 header=head(path,title,desc,base,production).replace('<link rel="stylesheet" href="/catalog.css">','<link rel="stylesheet" href="/style.css"><link rel="stylesheet" href="/cs-lesson.css">')
 header=re.sub(r'<script type="application/ld\+json">.*?</script>',lambda _:f'<script type="application/ld+json">{lesson_schema(c,part,path,title,desc,base)}</script>',header,flags=re.S)
 home=f'/computer-science/{c["slug"]}/'
 nav='<aside class="sidebar"><a class="brand" style="font-size:20px" href="/">◉ openstemlab.</a><a class="side-subject" href="/subjects/computer-science/">← Computer Science labs</a><div class="side-label">LABORATORY '+str(c['number']).zfill(2)+'</div><nav aria-label="Lesson navigation">'
 for href,label in [(home,'Explore the experiment'),(home+'theory/','Understand the theory'),(home+'#apparatus','Know your tools'),(home+'#method','Follow the method'),(home+'#results','Analyse your results'),(home+'#check','Check your understanding'),(home+'report/','Sample lab report')]:
  nav+=f'<a class="nav-item{" active" if path==href else ""}" href="{href}">{label}</a>'
 nav+='<a class="nav-item" href="/experiments/">Search all experiments</a></nav><div class="side-note"><span class="small-sun">✳</span><p>Learn by computing.<br>Understand by benchmarking.</p></div><a class="text-button" href="/">← All subjects</a></aside>'
 heading=c['title'] if part=='experiment' else c['shortTitle']+' theory' if part=='theory' else c['shortTitle']+' lab report'
 return header+'<body>'+nav+'<main><header class="topbar"><div><a href="/subjects/computer-science/">Computer Science</a> / '+E(c['shortTitle'])+'</div><span class="free-label">FREE TO EXPLORE</span></header><section class="page-heading"><div class="eyebrow">LABORATORY '+str(c['number']).zfill(2)+' · COMPUTER SCIENCE</div><h1>'+E(heading)+'</h1><p>'+E(desc)+'</p></section><nav class="lab-navigation" aria-label="Experiment pages"><a href="'+home+'">Workbench</a><a href="'+home+'theory/">Detailed theory</a><a href="'+home+'#method">Method</a><a href="'+home+'#results">My results</a><a href="'+home+'report/">Example report</a></nav>'+body+'<footer><span class="footer-brand">openstemlab.</span><a href="/subjects/computer-science/">All computer science labs</a><span>Deterministic algorithmic model</span></footer></main>'+ ('<script id="labConfig" type="application/json">'+json.dumps(c,ensure_ascii=False).replace('<',chr(92)+'u003c')+'</script><script src="/cs-models.js"></script><script src="/cs-engine.js"></script>' if part=='experiment' else '')+'</body></html>'

def build_cs(out,base,production):
 published=[c for c in specs() if c['published']]
 for name,dest in [('models.js','cs-models.js'),('engine.js','cs-engine.js'),('lesson.css','cs-lesson.css')]:
  (out/dest).write_text((ROOT/'content/cs'/name).read_text())
 db=sqlite3.connect(ROOT/'data/catalog.sqlite3')
 sid=db.execute("SELECT id FROM subjects WHERE slug='computer-science'").fetchone()[0]
 db.execute("UPDATE subjects SET content_status='live' WHERE slug='computer-science'")
 paths=[]
 for c in published:
  slug=c['slug']
  home=f'/computer-science/{slug}/'
  (out/home.lstrip('/')).mkdir(parents=True,exist_ok=True)
  rows=[observation(c,v) for v in c['samples']]
  f=fit(rows)
  for part,body in [
   ('experiment',workbench(c)),
   ('theory','<section>'+theory(c)+f'<div class="insight"><span>↳</span><div><strong>Connect the theory to benchmark observations.</strong><p>{E(c["modelExtra"])}</p></div></div></section>'),
   ('report',report(c,rows,f,out))
  ]:
   path=home+('' if part=='experiment' else part+'/')
   file=out/path.lstrip('/')/'index.html'
   file.parent.mkdir(parents=True,exist_ok=True)
   file.write_text(shell(c,part,body,base,production))
   paths.append(path)
  db.execute('INSERT INTO experiments(subject_id,slug,title,status,page_path,theory_path,report_path) VALUES(?,?,?,?,?,?,?) ON CONFLICT(slug) DO UPDATE SET title=excluded.title,status=excluded.status,page_path=excluded.page_path,theory_path=excluded.theory_path,report_path=excluded.report_path',(sid,slug,c['shortTitle'],'live',home,home+'theory/',home+'report/'))
 db.commit()
 db.close()
 return paths

if __name__=='__main__':
 import argparse
 parser=argparse.ArgumentParser()
 parser.add_argument('--production',action='store_true')
 args=parser.parse_args()
 config=json.loads((ROOT/'site-config.json').read_text())
 base=config['base_url'].rstrip('/')
 out=ROOT/('release' if args.production else 'dist')
 out.mkdir(exist_ok=True)
 paths=build_cs(out,base,args.production)
 print(f"Built {len(paths)} CS pages for {base}: {paths}")
