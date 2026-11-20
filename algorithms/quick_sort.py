# =====================================================
# DAA PROJECT
# RANDOMIZED THREE-WAY QUICK SORT
# =====================================================

import random


def _three_way_partition(data, low, high, key, ascending, stats, record=None):
    """Partitions data[low..high] into < pivot, == pivot, and > pivot."""
    pivot_index = random.randint(low, high)
    pivot = data[pivot_index][key]

    if record:
        record("pivot", f"Selected pivot value: {pivot}", pivot_index)

    left = low
    current = low
    right = high

    while current <= right:
        stats["comparisons"] += 1
        value = data[current][key]

        if record:
            record("compare", f"Comparing {value} with pivot {pivot}.", pivot_index, current)

        if ascending:
            smaller = value < pivot
            larger = value > pivot
        else:
            smaller = value > pivot
            larger = value < pivot

        if smaller:
            if left != current:
                data[left], data[current] = data[current], data[left]
                stats["swaps"] += 1
                # Keep pivot_index accurate if the pivot element was swapped
                if pivot_index == left:
                    pivot_index = current
                elif pivot_index == current:
                    pivot_index = left
                if record:
                    record("swap", "Moved element into the smaller partition.", pivot_index, current)
            left += 1
            current += 1

        elif larger:
            if current != right:
                data[current], data[right] = data[right], data[current]
                stats["swaps"] += 1
                if pivot_index == current:
                    pivot_index = right
                elif pivot_index == right:
                    pivot_index = current
                if record:
                    record("swap", "Moved element into the larger partition.", pivot_index, current)
            right -= 1

        else:
            current += 1

    if record:
        record("pivot_placed", "Three-way partition completed.", left)

    return left, right


def _run_quicksort(data, key="risk_score", ascending=True, record=None):
    sorted_data = [item.copy() for item in data]
    stats = {
        "recursive_calls": 0,
        "comparisons": 0,
        "swaps": 0,
        "max_recursion_depth": 0,
    }

    if record:
        record("start", "Quick Sort execution started.", sorted_data)

    def sort(low, high, depth):
        stats["recursive_calls"] += 1
        stats["max_recursion_depth"] = max(stats["max_recursion_depth"], depth)

        while low < high:
            step_cb = (
                (lambda act, desc, p_idx=None, cmp_idx=None: record(act, desc, sorted_data, p_idx, cmp_idx))
                if record
                else None
            )
            left, right = _three_way_partition(
                sorted_data, low, high, key, ascending, stats, step_cb
            )

            # Recurse on smaller partition; iterate on larger partition (guarantees O(log n) stack)
            if (left - low) < (high - right):
                if low < left - 1:
                    sort(low, left - 1, depth + 1)
                low = right + 1
            else:
                if right + 1 < high:
                    sort(right + 1, high, depth + 1)
                high = left - 1

    if len(sorted_data) > 1:
        sort(0, len(sorted_data) - 1, 1)

    if record:
        record("complete", "Quick Sort successfully completed.", sorted_data)

    return sorted_data, stats


def quick_sort(data, key="risk_score", ascending=True):
    return _run_quicksort(data, key=key, ascending=ascending, record=None)


def quick_sort_with_steps(data, key="risk_score", ascending=True):
    steps = []

    def record(action, description, current_array, pivot_index=None, comparing=None):
        steps.append({
            "action": action,
            "description": description,
            "array": [item.copy() for item in current_array],
            "pivot_index": pivot_index,
            "comparing": comparing,
            "stats": None,  # populated right below
        })

    # Track live stats snapshot per recorded step
    sorted_data = [item.copy() for item in data]
    stats = {
        "recursive_calls": 0,
        "comparisons": 0,
        "swaps": 0,
        "max_recursion_depth": 0,
    }

    def record_with_stats(action, description, pivot_index=None, comparing=None):
        steps.append({
            "action": action,
            "description": description,
            "array": [item.copy() for item in sorted_data],
            "pivot_index": pivot_index,
            "comparing": comparing,
            "stats": stats.copy(),
        })

    record_with_stats("start", "Quick Sort execution started.")

    def sort(low, high, depth):
        stats["recursive_calls"] += 1
        stats["max_recursion_depth"] = max(stats["max_recursion_depth"], depth)

        while low < high:
            left, right = _three_way_partition(
                sorted_data, low, high, key, ascending, stats, record_with_stats
            )
            if (left - low) < (high - right):
                if low < left - 1:
                    sort(low, left - 1, depth + 1)
                low = right + 1
            else:
                if right + 1 < high:
                    sort(right + 1, high, depth + 1)
                high = left - 1

    if len(sorted_data) > 1:
        sort(0, len(sorted_data) - 1, 1)

    record_with_stats("complete", "Quick Sort successfully completed.")
    return sorted_data, stats, steps