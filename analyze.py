"""
Full analysis script for the Product Hunt launch day study.
Produces all metrics, tables, and strategic summaries from the raw data.

Requirements:
    pip install tqdm google-genai

Usage:
    python analyze.py                    # Run full analysis (uses pre-computed quality ratings)
    python analyze.py --rate-quality     # Re-run LLM quality ratings (requires GEMINI_API_KEY env var)
"""

import csv
import json
import os
import sys
from datetime import datetime
from collections import defaultdict

DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
DATA_DIR = os.path.dirname(os.path.abspath(__file__))


def med(lst):
    return sorted(lst)[len(lst) // 2] if lst else 0

def p25(lst):
    return sorted(lst)[len(lst) // 4] if lst else 0

def p75(lst):
    return sorted(lst)[3 * len(lst) // 4] if lst else 0


def load_data():
    daily_products = defaultdict(list)
    launches_by_day = defaultdict(int)
    featured_by_day = defaultdict(int)
    dates_by_day = defaultdict(set)

    for filename in ['posts_2023.csv', 'posts_2024.csv']:
        filepath = os.path.join(DATA_DIR, filename)
        with open(filepath, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    created = datetime.strptime(row['createdAt'][:10], '%Y-%m-%d')
                    day_name = DAYS[created.weekday()]
                    date_key = created.date()
                    votes = int(row['votesCount'])
                    launches_by_day[day_name] += 1
                    dates_by_day[day_name].add(date_key)
                    daily_products[date_key].append({
                        'name': row['name'],
                        'tagline': row['tagline'],
                        'description': row['description'],
                        'votes': votes,
                        'day': day_name,
                        'date': str(date_key)
                    })
                    if row.get('featuredAt') and row['featuredAt'].strip():
                        featured_by_day[day_name] += 1
                except Exception:
                    continue

    return daily_products, launches_by_day, featured_by_day, dates_by_day


def compute_rankings(daily_products):
    daily_max = defaultdict(list)
    daily_2nd = defaultdict(list)
    daily_5th = defaultdict(list)
    daily_gap = defaultdict(list)

    for date_key, products in daily_products.items():
        s = sorted([p['votes'] for p in products], reverse=True)
        day_name = products[0]['day']
        if len(s) >= 1:
            daily_max[day_name].append(s[0])
        if len(s) >= 2:
            daily_2nd[day_name].append(s[1])
            daily_gap[day_name].append(s[0] - s[1])
        if len(s) >= 5:
            daily_5th[day_name].append(s[4])

    return daily_max, daily_2nd, daily_5th, daily_gap


def compute_potw(daily_products):
    daily_winners = {}
    for date_key, products in daily_products.items():
        products_sorted = sorted(products, key=lambda x: x['votes'], reverse=True)
        daily_winners[date_key] = products_sorted[0]

    weekly_winners = defaultdict(list)
    for date_key, winner in daily_winners.items():
        iso_year, iso_week, _ = date_key.isocalendar()
        weekly_winners[(iso_year, iso_week)].append(winner)

    potw_day_counts = defaultdict(int)
    potw_total = 0
    for week_key, winners in weekly_winners.items():
        if len(winners) < 5:
            continue
        best = max(winners, key=lambda x: x['votes'])
        potw_day_counts[best['day']] += 1
        potw_total += 1

    return potw_day_counts, potw_total


def rate_quality(daily_products):
    """Rate #1 products using Gemini. Requires GEMINI_API_KEY env var."""
    import time
    from tqdm import tqdm
    from google import genai

    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        print("ERROR: Set GEMINI_API_KEY environment variable")
        sys.exit(1)

    client = genai.Client(api_key=api_key)

    top1_by_day = defaultdict(list)
    for date_key, products in daily_products.items():
        products_sorted = sorted(products, key=lambda x: x['votes'], reverse=True)
        if products_sorted:
            top = products_sorted[0]
            top1_by_day[top['day']].append(top)

    all_ratings = []
    total_batches = sum((len(top1_by_day[d]) + 19) // 20 for d in DAYS)
    pbar = tqdm(total=total_batches, desc="Rating products", unit="batch")

    for day in DAYS:
        products = top1_by_day[day]
        pbar.set_description(f"Rating {day}")

        for batch_start in range(0, len(products), 20):
            batch = products[batch_start:batch_start + 20]

            prompt = """Rate each product's quality on a scale of 1-10 based on its name, tagline, and description.
Consider: clarity, value proposition, innovation, market appeal, and professional presentation.
Return ONLY a JSON array of integers (the scores), one per product, in the same order.

Products:
"""
            for i, p in enumerate(batch):
                prompt += f"\n{i + 1}. Name: {p['name']}\n   Tagline: {p['tagline']}\n   Description: {p['description'][:300]}\n"

            try:
                response = client.models.generate_content(
                    model="gemini-3-flash-preview",
                    contents=prompt
                )
                text = response.text.strip()
                if "```" in text:
                    text = text.split("```")[1].replace("json", "").strip()
                scores = json.loads(text)

                for i, p in enumerate(batch):
                    if i < len(scores):
                        all_ratings.append({
                            'day': p['day'],
                            'name': p['name'],
                            'votes': p['votes'],
                            'score': scores[i]
                        })
            except Exception as e:
                tqdm.write(f"  Error on {day} batch {batch_start // 20 + 1}: {e}")

            pbar.update(1)
            time.sleep(0.5)

    pbar.close()

    output_path = os.path.join(DATA_DIR, 'quality_ratings.json')
    with open(output_path, 'w') as f:
        json.dump(all_ratings, f)

    return all_ratings


def load_quality_ratings():
    path = os.path.join(DATA_DIR, 'quality_ratings.json')
    with open(path) as f:
        return json.load(f)


def print_analysis(launches_by_day, featured_by_day, dates_by_day,
                   daily_max, daily_2nd, daily_5th, daily_gap,
                   potw_day_counts, potw_total, all_ratings):

    quality_by_day = defaultdict(list)
    for r in all_ratings:
        quality_by_day[r['day']].append(r['score'])

    total = sum(launches_by_day.values())

    print("=" * 100)
    print(f"PRODUCTHUNT LAUNCH DAY ANALYSIS -- {total:,} launches, {len(all_ratings)} LLM-rated #1 products (2023-2024)")
    print("=" * 100)

    # Competition
    print("\n-- COMPETITION --")
    print(f"{'Day':<12} {'Avg Launches':>13} {'Avg Featured':>13} {'Featured %':>11}")
    print("-" * 52)
    for day in DAYS:
        n = len(dates_by_day[day])
        print(f"{day:<12} {launches_by_day[day] / n:>13.0f} {featured_by_day[day] / n:>13.0f} {featured_by_day[day] / launches_by_day[day] * 100:>10.1f}%")

    # Votes needed
    print("\n-- VOTES NEEDED FOR EACH RANK (median) --")
    print(f"{'Day':<12} {'#1':>8} {'#2':>8} {'#5':>8} {'Gap #1-#2':>10}")
    print("-" * 50)
    for day in DAYS:
        print(f"{day:<12} {med(daily_max[day]):>8} {med(daily_2nd[day]):>8} {med(daily_5th[day]):>8} {med(daily_gap[day]):>10}")

    # Predictability
    print("\n-- PREDICTABILITY OF #1 --")
    print(f"{'Day':<12} {'P25':>8} {'Median':>8} {'P75':>8} {'Range':>14}")
    print("-" * 54)
    for day in DAYS:
        vals = daily_max[day]
        print(f"{day:<12} {p25(vals):>8} {med(vals):>8} {p75(vals):>8} {min(vals):>6}-{max(vals):>6}")

    # Quality
    print("\n-- QUALITY OF #1 PRODUCTS (LLM-rated) --")
    print(f"{'Day':<12} {'N':>5} {'Avg':>8} {'Median':>8}")
    print("-" * 36)
    for day in DAYS:
        qs = quality_by_day[day]
        if qs:
            print(f"{day:<12} {len(qs):>5} {sum(qs) / len(qs):>8.1f} {med(qs):>8}")

    # Quality vs votes correlation
    scores = [r['score'] for r in all_ratings]
    votes = [r['votes'] for r in all_ratings]
    n = len(scores)
    mean_s = sum(scores) / n
    mean_v = sum(votes) / n
    cov = sum((s - mean_s) * (v - mean_v) for s, v in zip(scores, votes)) / n
    std_s = (sum((s - mean_s) ** 2 for s in scores) / n) ** 0.5
    std_v = (sum((v - mean_v) ** 2 for v in votes) / n) ** 0.5
    pearson = cov / (std_s * std_v)
    print(f"\n-- QUALITY vs VOTES CORRELATION --")
    print(f"Pearson r = {pearson:.3f} (weak -- quality explains ~{pearson**2*100:.0f}% of vote variance)")

    # POTW
    print(f"\n-- PRODUCT OF THE WEEK ({potw_total} weeks) --")
    print(f"{'Day':<12} {'Wins':>6} {'Rate':>8}")
    print("-" * 28)
    for day in DAYS:
        c = potw_day_counts[day]
        print(f"{day:<12} {c:>6} {c / potw_total * 100:>7.1f}%")
    weekend = potw_day_counts['Saturday'] + potw_day_counts['Sunday']
    print(f"\nWeekend wins: {weekend}/{potw_total} ({weekend / potw_total * 100:.1f}%)")

    # Quality-adjusted
    print("\n-- SAME QUALITY, DIFFERENT DAY (controlled comparison) --")
    for target_score in [7, 8]:
        print(f"\nProducts rated {target_score}/10 that reached #1:")
        for day in DAYS:
            day_items = [r for r in all_ratings if r['day'] == day and r['score'] == target_score]
            if day_items:
                v = [r['votes'] for r in day_items]
                print(f"  {day:<12} n={len(day_items):>3}  avg_votes={sum(v) / len(v):>7.0f}  med_votes={sorted(v)[len(v) // 2]:>6}")


if __name__ == '__main__':
    print("Loading data...")
    daily_products, launches_by_day, featured_by_day, dates_by_day = load_data()
    daily_max, daily_2nd, daily_5th, daily_gap = compute_rankings(daily_products)
    potw_day_counts, potw_total = compute_potw(daily_products)

    if '--rate-quality' in sys.argv:
        print("Rating #1 products with Gemini...")
        all_ratings = rate_quality(daily_products)
    else:
        print("Loading pre-computed quality ratings...")
        all_ratings = load_quality_ratings()

    print_analysis(launches_by_day, featured_by_day, dates_by_day,
                   daily_max, daily_2nd, daily_5th, daily_gap,
                   potw_day_counts, potw_total, all_ratings)
