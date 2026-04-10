# What Day Should You Launch on Product Hunt to Reach #1?

A data-driven analysis of **76,525 Product Hunt launches** (2023-2024) with **656 LLM-rated #1 products**, investigating the optimal day of the week to maximize your chances of reaching #1 Product of the Day.

## TL;DR

- **If your only goal is #1 Product of the Day** --> launch on **Saturday**. You face 2x fewer competitors, need 2x fewer votes, and the quality bar is lower.
- **If you also want Product of the Week** --> launch on **Tuesday**. Weekend launches almost never (2.2%) win POTW.
- **Product quality barely predicts upvotes** (r = 0.17). Distribution and community mobilization matter far more than how polished your product is.

---

## Methodology

### Data Sources

1. **Launch data**: [ProductHunt 2023-2024 Kaggle dataset](https://www.kaggle.com/datasets/haxzie/producthunt-2023-launches) -- 76,525 launches with timestamps, vote counts, comment counts, descriptions, and featured status.
2. **Traffic data**: Aggregated votes and comments by day of week from Product Hunt's public analytics (see chart below).
3. **Quality ratings**: All 656 #1-ranked daily products were rated 1-10 by Google's Gemini 3 Flash model based on their name, tagline, and description -- evaluating clarity, value proposition, innovation, market appeal, and presentation.

### Metrics Computed

- **Avg Launches / Featured**: Mean number of total and featured (curated) products per day of week.
- **Median #1 / #2 / #5 votes**: Median upvotes received by the 1st, 2nd, and 5th ranked product each day.
- **Gap**: Median vote difference between #1 and #2 (your margin of safety).
- **P25 / P75 of #1**: Votes needed on an "easy" (25th percentile) vs "hard" (75th percentile) day.
- **LLM Quality**: Average and median quality score (1-10) of #1 products.
- **POTW Win Rate**: How often each day's #1 goes on to win Product of the Week.

---

## 1. Competition Levels by Day

How many products are you competing against?

| Day | Avg Launches | Avg Featured | Featured % |
|:---|---:|---:|---:|
| **Monday** | 121 | 31 | 25.1% |
| **Tuesday** | 151 | 43 | 28.4% |
| **Wednesday** | 140 | 41 | 29.5% |
| **Thursday** | 136 | 41 | 29.9% |
| **Friday** | 118 | 34 | 28.6% |
| **Saturday** | 79 | 20 | 25.8% |
| **Sunday** | 72 | 18 | 25.1% |

**Insight**: Weekends have roughly **half** the competition of peak weekdays. Tuesday is the most crowded day with 151 avg launches and 43 featured products.

---

## 2. Votes Needed for Each Rank

What does it actually take to reach #1, #2, or top 5?

| Day | Median #1 | Median #2 | Median #5 | Gap #1-#2 |
|:---|---:|---:|---:|---:|
| **Monday** | 1,106 | 694 | 329 | 348 |
| **Tuesday** | 1,169 | 808 | 415 | 299 |
| **Wednesday** | 1,069 | 728 | 380 | 271 |
| **Thursday** | 1,026 | 738 | 374 | 228 |
| **Friday** | 760 | 526 | 262 | 212 |
| **Saturday** | 511 | 362 | 185 | 141 |
| **Sunday** | 625 | 412 | 194 | 169 |

**Insight**: Saturday requires only **511 votes** to reach #1 -- less than half of Tuesday's 1,169. The gap between #1 and #2 is also smaller on weekends, meaning less margin needed.

---

## 3. Predictability: How Stable Is the Target?

Can you plan for a specific vote target, or is it a coin flip?

| Day | P25 (Easy) | Median | P75 (Hard) | Range |
|:---|---:|---:|---:|:---|
| **Monday** | 818 | 1,106 | 1,397 | 527 - 4,256 |
| **Tuesday** | 923 | 1,169 | 1,482 | 494 - 3,039 |
| **Wednesday** | 826 | 1,069 | 1,402 | 516 - 5,244 |
| **Thursday** | 811 | 1,026 | 1,325 | 485 - 2,807 |
| **Friday** | 633 | 760 | 1,003 | 342 - 7,466 |
| **Saturday** | 431 | 511 | 644 | 256 - 4,192 |
| **Sunday** | 488 | 625 | 797 | 224 - 3,486 |

**Insight**: Saturday is the most predictable -- the IQR (P75 - P25) is only 213 votes, vs 559 on Tuesday. You can plan with more confidence on weekends.

---

## 4. Quality of #1 Products (LLM-Rated)

Are weekend winners lower quality than weekday winners?

| Day | N Rated | Avg Quality | Median Quality |
|:---|---:|---:|---:|
| **Monday** | 94 | 7.7 | 8 |
| **Tuesday** | 94 | 8.0 | 8 |
| **Wednesday** | 94 | 7.8 | 8 |
| **Thursday** | 94 | 7.7 | 8 |
| **Friday** | 93 | 7.4 | 8 |
| **Saturday** | 93 | 7.0 | 7 |
| **Sunday** | 94 | 7.3 | 7 |

**Insight**: Weekend #1 products score about **1 point lower** on quality (7.0-7.3 vs 7.7-8.0). The quality bar is genuinely lower on weekends.

---

## 5. Does Quality Predict Upvotes?

| Quality Score | Count | Avg Votes | Median Votes |
|---:|---:|---:|---:|
| 4 | 8 | 578 | 511 |
| 5 | 28 | 869 | 582 |
| 6 | 84 | 816 | 692 |
| 7 | 166 | 959 | 816 |
| 8 | 208 | 1,043 | 941 |
| 9 | 137 | 1,096 | 958 |
| 10 | 23 | 1,310 | 1,169 |

**Pearson correlation: r = 0.174** (weak positive)

**Insight**: Quality explains only ~3% of the variance in votes. A 10/10 product averages just 1.6x the votes of a 6/10 product. **Distribution, community, and timing matter far more than product quality for reaching #1.** This is perhaps the most important finding of the study.

---

## 6. Same Quality, Different Day: The Controlled Experiment

What happens when we hold quality constant and only vary the day?

### Products rated 7/10 that reached #1:

| Day | N | Avg Votes | Median Votes |
|:---|---:|---:|---:|
| **Monday** | 23 | 1,290 | 1,275 |
| **Tuesday** | 19 | 1,287 | 1,113 |
| **Wednesday** | 30 | 1,071 | 928 |
| **Thursday** | 24 | 1,066 | 1,029 |
| **Friday** | 24 | 880 | 708 |
| **Saturday** | 23 | 526 | 505 |
| **Sunday** | 23 | 614 | 588 |

### Products rated 8/10 that reached #1:

| Day | N | Avg Votes | Median Votes |
|:---|---:|---:|---:|
| **Monday** | 30 | 1,126 | 1,062 |
| **Tuesday** | 35 | 1,243 | 1,155 |
| **Wednesday** | 35 | 1,278 | 1,079 |
| **Thursday** | 32 | 1,156 | 1,105 |
| **Friday** | 25 | 888 | 836 |
| **Saturday** | 23 | 703 | 599 |
| **Sunday** | 28 | 697 | 679 |

**Insight**: A 7/10 product gets **1,275 votes on Monday but only 505 on Saturday** -- a 2.5x difference for the same quality level. The day doesn't make your product look worse; it just means fewer people see it. A weekend win is a "cheaper" win but an equally valid badge.

---

## 7. Product of the Week: Weekend Launches Almost Never Win

Out of 93 complete weeks analyzed:

| Day | POTW Wins | Win Rate |
|:---|---:|---:|
| **Monday** | 23 | 24.7% |
| **Tuesday** | 28 | 30.1% |
| **Wednesday** | 19 | 20.4% |
| **Thursday** | 16 | 17.2% |
| **Friday** | 5 | 5.4% |
| **Saturday** | 1 | 1.1% |
| **Sunday** | 1 | 1.1% |

- **Weekend POTW wins: 2/93 (2.2%)**
- **Weekday POTW wins: 91/93 (97.8%)**

**Insight**: If Product of the Week matters to your launch strategy, weekends are essentially disqualified. Tuesday alone captures 30% of all POTW wins.

---

## 8. Master Comparison Table

| Day | Launches | Featured | Med #1 | Med #2 | Gap | P25 #1 | P75 #1 | Quality | POTW % |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Monday** | 121 | 31 | 1,106 | 694 | 348 | 818 | 1,397 | 7.7 | 24.7% |
| **Tuesday** | 151 | 43 | 1,169 | 808 | 299 | 923 | 1,482 | 8.0 | 30.1% |
| **Wednesday** | 140 | 41 | 1,069 | 728 | 271 | 826 | 1,402 | 7.8 | 20.4% |
| **Thursday** | 136 | 41 | 1,026 | 738 | 228 | 811 | 1,325 | 7.7 | 17.2% |
| **Friday** | 118 | 34 | 760 | 526 | 212 | 633 | 1,003 | 7.4 | 5.4% |
| **Saturday** | 79 | 20 | 511 | 362 | 141 | 431 | 644 | 7.0 | 1.1% |
| **Sunday** | 72 | 18 | 625 | 412 | 169 | 488 | 797 | 7.3 | 1.1% |

---

## 9. Strategic Recommendations

### Launch on Saturday if:
- Your **primary goal is #1 Product of the Day** badge
- You can mobilize **~500 votes** from your own network
- You don't care about Product of the Week
- You want the most predictable outcome (narrowest vote range)

### Launch on Tuesday if:
- You want a shot at **Product of the Week** (30% win rate)
- You can mobilize **~1,100+ votes**
- You want maximum organic traffic and newsletter exposure
- Your product is genuinely exceptional (8+/10 quality)

### Launch on Friday if:
- You want a **middle ground**: only ~760 votes needed
- You still get weekday newsletter exposure
- Lower competition than Tue-Thu but more traffic than weekends

### Additional Considerations
- Product Hunt **does not send their "Top Products" email newsletter on weekends** (Friday/Saturday), reducing the amplification of a weekend #1
- The **first half of the month** tends to have more launches and stiffer competition
- **Distribution > Quality**: With r = 0.17, your ability to rally votes matters ~6x more than product polish

---

## Methodology Notes

- **Dataset**: 76,525 launches from the [ProductHunt 2023-2024 Kaggle dataset](https://www.kaggle.com/datasets/haxzie/producthunt-2023-launches) by Musthaq Ahamad (MIT License)
- **Quality ratings**: 656 #1-ranked products rated by Google Gemini 3 Flash on a 1-10 scale for clarity, value proposition, innovation, market appeal, and presentation
- **Traffic data**: Aggregated vote and comment counts by day of week from Product Hunt public analytics
- **POTW analysis**: Based on 93 complete weeks (Mon-Sun) where the daily #1 with the highest votes was considered the weekly winner
- **Limitations**: 
  - The dataset covers 2023-2024; patterns may shift as Product Hunt evolves
  - LLM quality ratings are subjective proxies -- they evaluate the text presentation, not the actual product
  - Vote counts in the dataset are final counts, not real-time; some products may have gained votes after their launch day
  - The analysis doesn't account for seasonal effects, holidays, or major tech events

---

*Analysis conducted April 2026. Data from ProductHunt 2023-2024.*
