"""SmartCity Logistics dashboard: python main.py  (or: python main.py <number>)"""
import csv
import os
import sys

from divide_conquer.merge_sort import merge_sort, merge_sort_counted, empirical_check
from divide_conquer.closest_pair import closest_pair, benchmark
from greedy.activity_selection import activity_selection
from greedy.fractional_knapsack import fractional_knapsack
from greedy.huffman import build_tree, build_codes, encode, decode, compression_stats
from dynamic_programming.knapsack_01 import knapsack_2d, knapsack_1d, knapsack_bruteforce
from dynamic_programming.shortest_path_dp import shortest_path

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


def read_csv(name):
    with open(os.path.join(DATA, name), newline="") as f:
        return list(csv.DictReader(f))


def sort_packages():
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
    pts = [(float(r["x"]), float(r["y"])) for r in read_csv("sample_hubs.csv")]
    d, (a, b) = closest_pair(pts)
    print(f"Closest hubs: {a} and {b}, distance {d:.3f}")
    print("\nBenchmark (n, brute_s, divide&conquer_s, same_answer):")
    for row in benchmark():
        print("  ", row)


def schedule():
    w = [(int(r["start"]), int(r["end"])) for r in read_csv("sample_windows.csv")]
    chosen = activity_selection(w)
    print(f"{len(chosen)} of {len(w)} deliveries scheduled: {chosen}")


def van_fractional():
    items = [(r["item"], float(r["weight"]), float(r["value"])) for r in read_csv("sample_cargo.csv")]
    total, taken = fractional_knapsack(items, 50)
    print(f"Capacity 50 -> value {total:.2f}")
    for name, frac in taken:
        print(f"  {name}: {frac:.0%}")


def compress():
    text = open(os.path.join(DATA, "sample_manifest.txt")).read()
    root = build_tree(text)
    codes = build_codes(root)
    bits = encode(text, codes)
    assert decode(bits, root) == text, "round trip failed"
    s = compression_stats(text, bits)
    print(f"Lossless round trip OK. {s['original_bits']} -> {s['compressed_bits']} bits, "
          f"ratio {s['ratio']:.2f}x ({s['savings_pct']:.1f}% saved)")


def truck_knapsack():
    rows = read_csv("sample_cargo.csv")
    items = [(int(r["weight"]), int(r["value"])) for r in rows]
    best, chosen, _ = knapsack_2d(items, 50)
    print(f"Capacity 50 -> best value {best} (1D check: {knapsack_1d(items, 50)})")
    print("  Load:", [rows[i]["item"] for i in chosen])
    small = items[:15]
    print("  Brute-force on 15 items agrees:", knapsack_bruteforce(small, 50) == best)


def routes():
    edges = [(r["from"], r["to"], float(r["weight"])) for r in read_csv("sample_roads.csv")]
    src = input("  From [Depot]: ").strip() or "Depot"
    dst = input("  To [Warehouse]: ").strip() or "Warehouse"
    cost, path = shortest_path(edges, src, dst)
    print(f"  Cost {cost}: {' -> '.join(path) if path else 'unreachable'}")


MENU = [("Sort packages by deadline (Merge Sort)", sort_packages),
        ("Closest hub pair + benchmark (Closest Pair)", hubs),
        ("Schedule deliveries (Activity Selection)", schedule),
        ("Load van, divisible cargo (Fractional Knapsack)", van_fractional),
        ("Compress manifest (Huffman)", compress),
        ("Load truck, indivisible cargo (0/1 Knapsack DP)", truck_knapsack),
        ("Cheapest route (Bellman-Ford DP)", routes)]


def main():
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        MENU[int(sys.argv[1]) - 1][1]()
        return
    while True:
        print("\n=== SmartCity Logistics ===")
        for i, (label, _) in enumerate(MENU, 1):
            print(f" {i}. {label}")
        print(" 0. Exit")
        choice = input("Select: ").strip()
        if choice == "0":
            break
        if choice.isdigit() and 1 <= int(choice) <= len(MENU):
            print()
            MENU[int(choice) - 1][1]()
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
