"""SmartCity Logistics dashboard """
import csv
import os
import sys

from divide_conquer.merge_sort import merge_sort_counted, empirical_check
from divide_conquer.closest_pair import closest_pair, benchmark
from greedy.activity_selection import activity_selection
from greedy.fractional_knapsack import fractional_knapsack
from greedy.huffman import build_tree, build_codes, encode, decode, compression_stats
from dynamic_programming.knapsack_01 import (knapsack_2d, knapsack_1d, knapsack_bruteforce,
                                             benchmark as knapsack_benchmark, memory_comparison)
from dynamic_programming.shortest_path_dp import shortest_path

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
VAN_CAPACITY = 50          # kg, used by the van (greedy) and truck (DP) demos


# ---------------------------------------------------------------- data loading
def read_csv(name):
    """Reading a csv file"""
    with open(os.path.join(DATA, name), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def read_text(name):
    """Reading a text file"""
    with open(os.path.join(DATA, name), encoding="utf-8") as f:
        return f.read()


# ------------------------------------------------------------------- features
def sort_packages():
    """merge sort the packages by deadline."""
    pk = [{"id": r["id"], "deadline": int(r["deadline_hour"])} for r in read_csv("sample_packages.csv")]
    out, comps = merge_sort_counted(pk, key=lambda p: p["deadline"])
    print(f"Sorted {len(pk)} packages by deadline using {comps} comparisons:")
    for p in out[:10]:
        print(f"  {p['id']}  deadline hour {p['deadline']}")
    print("  ...")
    print("\nEmpirical O(n log n) check (n, comparisons, n*log2 n, ratio):")
    for row in empirical_check():
        print("  ", row)


def hubs():
    """closest pair of hubs, compared with brute force"""
    pts = [(float(r["x"]), float(r["y"])) for r in read_csv("sample_hubs.csv")]
    d, (a, b) = closest_pair(pts)
    print(f"Closest hubs: {a} and {b}, distance {d:.3f}")
    print("\nBenchmark (n, brute_s, divide&conquer_s, same_answer):")
    for row in benchmark():
        print("  ", row)


def schedule():
    """most deliveries one driver can serve based on earliest finish time"""
    w = [(int(r["start"]), int(r["end"])) for r in read_csv("sample_windows.csv")]
    chosen = activity_selection(w)
    print(f"{len(chosen)} of {len(w)} deliveries scheduled: {chosen}")


def van_fractional():
    """fill a van with divisible cargo"""
    items = [(r["item"], float(r["weight"]), float(r["value"])) for r in read_csv("sample_cargo.csv")]
    total, taken = fractional_knapsack(items, VAN_CAPACITY)
    print(f"Capacity {VAN_CAPACITY} -> value {total:.2f}")
    for name, frac in taken:
        print(f"  {name}: {frac:.0%}")


def compress():
    """Huffman compress the manifest and check it is lossless"""
    text = read_text("sample_manifest.txt")
    root = build_tree(text)
    codes = build_codes(root)
    bits = encode(text, codes)
    if decode(bits, root) != text:
        raise RuntimeError("Huffman round trip failed: decoded text differs from the manifest")
    s = compression_stats(text, bits)
    print(f"Lossless round trip OK. {s['original_bits']} -> {s['compressed_bits']} bits, "
          f"ratio {s['ratio']:.2f}x ({s['savings_pct']:.1f}% saved)")


def truck_knapsack():
    """0/1 knapsack with a runtime and memory comparison"""
    rows = read_csv("sample_cargo.csv")
    items = [(int(r["weight"]), int(r["value"])) for r in rows]
    best, chosen, _ = knapsack_2d(items, VAN_CAPACITY)
    print(f"Capacity {VAN_CAPACITY} -> best value {best} (1D check: {knapsack_1d(items, VAN_CAPACITY)})")
    print("  Load:", [rows[i]["item"] for i in chosen])
    print("  Brute force on all", len(items), "items agrees:",
          knapsack_bruteforce(items, VAN_CAPACITY) == best)
    print("\nRuntime (n, brute_s, 2D_s, 1D_s, same_answer):")
    for row in knapsack_benchmark():
        print("  ", row)
    peak_2d, peak_1d = memory_comparison()
    print(f"\nPeak memory, 100 items x capacity 1000: 2D {peak_2d // 1024} KB vs 1D {peak_1d // 1024} KB")


def routes(src=None, dst=None):
    """cheapest route using Bellman Ford """
    edges = [(r["from"], r["to"], float(r["weight"])) for r in read_csv("sample_roads.csv")]
    places = sorted({n for u, v, _ in edges for n in (u, v)})
    if src is None:
        src = input("  From [Depot]: ").strip() or "Depot"
    if dst is None:
        dst = input("  To [Warehouse]: ").strip() or "Warehouse"
    if src not in places or dst not in places:
        print("  Unknown place. Known places:", ", ".join(places))
        return
    cost, path = shortest_path(edges, src, dst)
    print(f"  Cost {cost}: {' -> '.join(path) if path else 'unreachable'}")


MENU = [("Sort Packages by Delivery Deadline", sort_packages),
        ("Find the Two Closest Delivery Hubs", hubs),
        ("Schedule Non Overlapping Deliveries", schedule),
        ("Optimise Van Loading", van_fractional),
        ("Compress Delivery Manifest", compress),
        ("Optimise Truck Loading", truck_knapsack),
        ("Find the Cheapest Delivery Route", routes)]


# ------------------------------------------------------------------------ CLI
def print_menu():
    print("\n=== SmartCity Logistics ===")
    for i, (label, _) in enumerate(MENU, 1):
        print(f" {i}. {label}")
    print(" 0. Exit")


def run_all():
    """Run every feature in order with default inputs """
    for i, (label, func) in enumerate(MENU, 1):
        print(f"\n=== {i}. {label} ===")
        func(*(("Depot", "Warehouse") if func is routes else ()))


def run_cli(args):
    cmd = args[0].lower()
    if cmd.isdigit() and 1 <= int(cmd) <= len(MENU):
        func = MENU[int(cmd) - 1][1]
        extra = args[1:]
        if func is routes:
            if len(extra) not in (0, 2):
                print("Option 7 takes either no arguments or two: <from> <to>", file=sys.stderr)
                return 2
        elif extra:
            print(f"Option {cmd} takes no extra arguments", file=sys.stderr)
            return 2
        func(*extra)
        return 0
    print(f"Unknown option '{args[0]}'. Choose 1-{len(MENU)}.", file=sys.stderr)
    return 2


def interactive():
    """Menu loop Ends on 0 or Ctrl+C."""
    while True:
        print_menu()
        try:
            choice = input("Select: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            return
        if choice == "0":
            return
        if choice.isdigit() and 1 <= int(choice) <= len(MENU):
            print()
            try:
                MENU[int(choice) - 1][1]()
            except (EOFError, KeyboardInterrupt):
                print("\nCancelled.")
        else:
            print("Invalid choice.")


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    try:
        if args:
            return run_cli(args)
        interactive()
        return 0
    except FileNotFoundError as e:
        print(f"Missing data file: {e.filename}. Run from the project folder and keep the data/ folder.",
              file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())