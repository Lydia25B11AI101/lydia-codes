# Program Title: Association Rule Mining (Apriori Concept)
# Author: Lydia S. Makiwa
# Date: 2026-05-05
# Description: Demonstrates frequent itemset mining and association rules
#              from transaction data — a core technique in retail analytics.

from itertools import combinations
from collections import defaultdict

def get_support(transactions, itemset):
    count = sum(1 for t in transactions if itemset.issubset(t))
    return count / len(transactions)

def apriori(transactions, min_support=0.5, min_confidence=0.6):
    # Build unique items
    items = set(item for t in transactions for item in t)
    freq_itemsets = []
    rules = []

    # Frequent 1-itemsets
    candidates = [frozenset([i]) for i in items]
    frequent = [c for c in candidates if get_support(transactions, c) >= min_support]
    freq_itemsets.extend(frequent)

    k = 2
    while frequent:
        # Generate k-itemsets from frequent (k-1)-itemsets
        new_candidates = set()
        for a, b in combinations(frequent, 2):
            union = a | b
            if len(union) == k:
                new_candidates.add(union)
        frequent = [c for c in new_candidates if get_support(transactions, c) >= min_support]
        freq_itemsets.extend(frequent)
        k += 1

    # Generate association rules
    for itemset in freq_itemsets:
        if len(itemset) < 2:
            continue
        for i in range(1, len(itemset)):
            for antecedent in combinations(itemset, i):
                antecedent = frozenset(antecedent)
                consequent = itemset - antecedent
                supp_both = get_support(transactions, itemset)
                supp_ant  = get_support(transactions, antecedent)
                confidence = supp_both / supp_ant if supp_ant else 0
                lift = confidence / get_support(transactions, consequent) if get_support(transactions, consequent) else 0
                if confidence >= min_confidence:
                    rules.append((antecedent, consequent, round(confidence, 2), round(lift, 2)))

    return freq_itemsets, rules

# ─── Demo ───
transactions = [
    {"bread", "milk"},
    {"bread", "diaper", "beer", "eggs"},
    {"milk", "diaper", "beer", "cola"},
    {"bread", "milk", "diaper", "beer"},
    {"bread", "milk", "diaper", "cola"},
]

freq_sets, rules = apriori(transactions, min_support=0.6, min_confidence=0.7)

print("Frequent Itemsets (support >= 60%):")
for fs in sorted(freq_sets, key=len):
    print(f"  {set(fs)}  support={get_support(transactions, fs):.2f}")

print("\nAssociation Rules (confidence >= 70%):")
for ant, con, conf, lift in rules:
    print(f"  {set(ant)} → {set(con)}  conf={conf}  lift={lift}")
