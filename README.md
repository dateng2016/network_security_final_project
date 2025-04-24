# 🍪 Cookie Classification & GDPR Compliance Checker

This project classifies cookies collected from popular websites using both a predefined database and LLM (Large Language Model) assisted classification, then evaluates GDPR compliance based on the cookie types. It supports scraping in both **desktop** and **mobile** modes using Selenium and Chrome.

---

## 📁 Project Structure

```
.
├── check.py                            # Evaluates GDPR compliance from classification output
├── complianceResult.json               # Output: compliance results per domain
├── draw.ipynb                          # Notebook for visualizing results
├── llm_classification.py               # Classifies cookies using a large language model (LLM)
├── mobile_cookies.json                 # Cookies scraped in mobile mode
├── mobile_output.json                  # LLM-classified cookies from mobile mode
├── open-cookie-database.csv            # Public cookie classification database
├── output.json                         # Raw cookie classification result (LLM or mixed)
├── programmatical_classification.py    # Scrapes and classifies cookies via known database
├── push.sh                             # Script to sync or push files (if applicable)
├── README.md                           # Project overview and usage guide
├── top-10000-domains                   # List of top websites to scrape
├── venv/                               # Python virtual environment
├── website_cookies.json                # Cookies scraped in desktop mode
├── website_output.json                 # LLM-classified cookies from desktop mode
```

---

## 🚀 Features

-   Scrapes cookies from top websites using Selenium (mobile & desktop modes).
-   Classifies cookies using a public dataset.
-   Detects conflicts in dataset and removes ambiguous cookie names.
-   Uses multithreading for faster scraping.
-   Classifies cookies via LLM (in `llm_classification.py`).
-   Assesses GDPR compliance: allows only **Functional** or **Security** cookies.
-   Outputs detailed JSON reports for further analysis.

---

## ⚙️ Installation

**Set up a virtual environment (optional but recommended)**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

**Install dependencies**

    ```bash
    pip install -r requirements.txt
    ```

    > **Note:** You need **Chrome** and the appropriate **ChromeDriver** installed.

---

## 🧑‍💻 Usage

### 1. Programmatic Cookie Collection

Scrape cookies and classify based on known database:

```bash
python programmatical_classification.py
# For mobile mode:
python programmatical_classification.py --mobile
```

### 2. LLM Classification (if applicable)

Use `llm_classification.py` to apply LLM-based classification to scraped cookie data.

```bash
python llm_classification.py
```

### 3. GDPR Compliance Check

Check if websites are compliant (i.e., use only Functional or Security cookies):

```bash
python check.py
```

Results saved to:

```
complianceResult.json
```

---

## 📊 Outputs

-   `website_cookies.json` / `mobile_cookies.json`: Raw cookies from scraping
-   `website_output.json` / `mobile_output.json`: Cookies with classifications
-   `complianceResult.json`: Boolean GDPR compliance per domain

---

## 📌 Notes

-   Be respectful of target websites and ensure usage aligns with their terms of service.
-   The classification relies on cookie names — it's not bulletproof.
-   GDPR compliance logic is simplified; consult legal experts for production use.

---

## 📃 License

MIT License
