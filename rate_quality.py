import csv
import json
import time
from datetime import datetime
from collections import defaultdict
from google import genai
from tqdm import tqdm

client = genai.Client(api_key="AIzaSyDYgaYarrAj2eoAe2J8WWQNVP2DXJaMcBE")

days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

daily_products = defaultdict(list)

for filename in ['/tmp/producthunt_data/posts_2023.csv', '/tmp/producthunt_data/posts_2024.csv']:
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                created = datetime.strptime(row['createdAt'][:10], '%Y-%m-%d')
                date_key = created.date()
                votes = int(row['votesCount'])
                daily_products[date_key].append({
                    'name': row['name'],
                    'tagline': row['tagline'],
                    'description': row['description'],
                    'votes': votes,
                    'day': days[created.weekday()],
                    'date': str(date_key)
                })
            except:
                continue

top1_by_day = defaultdict(list)
for date_key, products in daily_products.items():
    products.sort(key=lambda x: x['votes'], reverse=True)
    if products:
        top = products[0]
        top1_by_day[top['day']].append(top)

all_ratings = []
total_batches = sum((len(top1_by_day[d]) + 19) // 20 for d in days)
pbar = tqdm(total=total_batches, desc="Rating products", unit="batch")

for day in days:
    products = top1_by_day[day]
    pbar.set_description(f"Rating {day}")

    for batch_start in range(0, len(products), 20):
        batch = products[batch_start:batch_start+20]
        
        prompt = """Rate each product's quality on a scale of 1-10 based on its name, tagline, and description.
Consider: clarity, value proposition, innovation, market appeal, and professional presentation.
Return ONLY a JSON array of integers (the scores), one per product, in the same order.

Products:
"""
        for i, p in enumerate(batch):
            prompt += f"\n{i+1}. Name: {p['name']}\n   Tagline: {p['tagline']}\n   Description: {p['description'][:300]}\n"
        
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
            tqdm.write(f"  Error on {day} batch {batch_start//20+1}: {e}")

        pbar.update(1)
        time.sleep(0.5)

pbar.close()

with open('/tmp/ph_quality_ratings.json', 'w') as f:
    json.dump(all_ratings, f)

print("\n" + "=" * 70)
print("QUALITY OF #1 PRODUCTS BY DAY OF WEEK")
print("=" * 70)
print(f"{'Day':<12} {'N':>5} {'Avg Quality':>12} {'Med Quality':>12} {'Avg Votes':>10}")
print("-" * 55)

for day in days:
    day_ratings = [r for r in all_ratings if r['day'] == day]
    if day_ratings:
        scores = [r['score'] for r in day_ratings]
        votes = [r['votes'] for r in day_ratings]
        avg_s = sum(scores) / len(scores)
        med_s = sorted(scores)[len(scores)//2]
        avg_v = sum(votes) / len(votes)
        print(f"{day:<12} {len(day_ratings):>5} {avg_s:>12.1f} {med_s:>12} {avg_v:>10.0f}")

