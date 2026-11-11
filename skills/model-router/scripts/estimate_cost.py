#!/usr/bin/env python3
"""Estimate the cost of one request (or a whole task) per model.

Reads the dated price snapshot in ../assets/prices.json and applies
long-context price cliffs and cache-read discounts where they are known.

  python estimate_cost.py --input 150000 --output 8000
  python estimate_cost.py --model opus --input 150000 --output 8000 --cached 120000
"""
import argparse
import json
from pathlib import Path

PRICES = Path(__file__).resolve().parent.parent / "assets" / "prices.json"


def cost(m, input_tokens, output_tokens, cached_tokens):
    """Return (usd, notes). cached_tokens is the part of input read from cache."""
    notes = []
    in_price, out_price = m["input"], m["output"]
    cliff = m.get("cliff")
    if cliff and input_tokens > cliff["over_input_tokens"]:
        in_price *= cliff["input_mult"]
        out_price *= cliff["output_mult"]
        notes.append(f"long-context rate (> {cliff['over_input_tokens']:,} input tokens)")
    cache_mult = m.get("cache_read_mult")
    if cached_tokens and cache_mult is None:
        notes.append("cache discount unknown, cached tokens billed at full rate")
        cache_mult = 1
    fresh = input_tokens - cached_tokens
    usd = (fresh * in_price + cached_tokens * in_price * (cache_mult or 1) + output_tokens * out_price) / 1_000_000
    return usd, notes


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--model", help="model key (default: compare all)")
    p.add_argument("--input", type=int, required=True, help="input tokens, including cached ones")
    p.add_argument("--output", type=int, default=0, help="output tokens")
    p.add_argument("--cached", type=int, default=0, help="input tokens read from cache")
    a = p.parse_args()
    if a.cached > a.input:
        p.error("--cached cannot exceed --input")

    data = json.loads(PRICES.read_text(encoding="utf-8"))
    models = data["models"]
    if a.model:
        if a.model not in models:
            p.error(f"unknown model '{a.model}'. Known: {', '.join(models)}")
        models = {a.model: models[a.model]}

    rows = [(k, m, *cost(m, a.input, a.output, a.cached)) for k, m in models.items()]
    rows.sort(key=lambda r: r[2])
    print(f"Prices checked {data['checked']} ({data['unit']}). Verify before relying on them.")
    print(f"input={a.input:,} output={a.output:,} cached={a.cached:,}\n")
    for key, m, usd, notes in rows:
        note = f"  [{'; '.join(notes)}]" if notes else ""
        print(f"{key:<7} {m['name']:<12} {m['tier']:<9} ${usd:>9.4f}{note}")


if __name__ == "__main__":
    main()
