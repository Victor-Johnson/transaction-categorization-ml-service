# UK Transaction Categorization ML Service (WIP)

A production-style machine learning service that categorizes noisy, bank-like UK transaction descriptions into spending categories (e.g., groceries, utilities, dining).

This project is intentionally designed around **ML-as-a-service** principles (inspired by fintech MLOps practices): reproducible training, versioned artifacts, batch inference, and clear API contracts.

---

## What it does

**Input (bank-style text)**  
`"contactless tesco milk 182933"`  

**Output (predicted category + confidence)**  
`{"category":"groceries","confidence":0.93}`

---

## Categories (v1)

- groceries
- dining
- utilities
- transportation
- subscriptions
- housing
- other

---

## Data approach

Because real banking datasets are sensitive, this repo uses **synthetic but realistic UK transaction text**:

- Structured retail-like records provide label authority (`Category`, `Item`, `Amount`, `Date`)
- A generator converts them into bank-style descriptions using:
  - UK merchants/providers (Tesco, TfL, British Gas, Netflix, etc.)
  - payment rails/tokens (POS, CARD, CONTACTLESS, DIRECT DEBIT, BACS, FPS)
  - noise injection (random references, separators, casing, truncation)

### Why the baseline accuracy is high
The initial TF-IDF + Logistic Regression model reaches near-perfect accuracy on synthetic data because the generator produces strong lexical signals.
To validate correctness, we run:
- **Label-shuffle test** → accuracy drops near random chance (no leakage)
- **Merchant masking** → small degradation, indicating the model learns structure beyond merchant names

---

## Quickstart

### 1) Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
