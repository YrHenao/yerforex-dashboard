# YerForex Trading Dashboard

<img width="1402" height="1996" alt="image" src="https://github.com/user-attachments/assets/459e5168-8c7d-4b2e-aac3-e3cd3b94b945" />


> Quantitative D1 market analytics, historical pattern research,
> macroeconomic context, and AI-assisted deployment.

## 📑 Contents

-   [Pattern Interpretation](#-pattern-interpretation)
-   [20-Session OHLC Table](#-20-session-ohlc-table)
-   [Historical Reaction Zones](#-historical-reaction-zones)
-   [Macroeconomic News & Catalysts](#-macroeconomic-news--catalysts)
-   [Sunday--Friday Statistical
    Scenario](#-sundayfriday-statistical-scenario)
-   [Facts vs. Projections](#-facts-vs-projections)
-   [System Architecture](#️-system-architecture)
-   [Security Architecture](#️-security-architecture)
-   [Technology Stack](#️-technology-stack)
-   [Performance Optimization](#-performance-optimization)
-   [Running YerForex Locally](#-running-yerforex-locally)
-   [Future Roadmap](#️-future-roadmap)
-   [Disclaimer](#️-disclaimer)

The objective is not to say:

> "Wednesday will always rise."

Instead, YerForex reports:

> "Wednesday showed bullish behavior in 3 of the 4 analyzed weeks."

This distinction is fundamental to the project.

------------------------------------------------------------------------

# 🔁 Pattern Interpretation

The dashboard converts raw statistics into simple explanations.

It searches for behavior such as:

-   Repeated bullish Mondays
-   Repeated bearish Tuesdays
-   Wednesday recovery after Tuesday weakness
-   Continuation between consecutive sessions
-   Reversal behavior
-   Strong and weak weekdays
-   Average daily directional movement

The goal is to make quantitative information understandable without
requiring the user to manually calculate every statistic.

------------------------------------------------------------------------

# 📋 20-Session OHLC Table

YerForex includes the complete historical dataset used in the analysis.

For every D1 session the dashboard displays:

  Field       Description
  ----------- -----------------------
  Date        Trading session
  Day         Day of the week
  Open        Opening price
  High        Highest price
  Low         Lowest price
  Close       Closing price
  Direction   Bullish / Bearish
  Change      Open → Close movement
  Range       High → Low movement

This allows every visual conclusion to be compared with the underlying
market data.

------------------------------------------------------------------------

# 🎯 Historical Reaction Zones

The dashboard identifies areas where price has previously reacted.

These zones can include:

-   Nearby support
-   Secondary support
-   Extreme 20-day support
-   Nearby resistance
-   Major resistance

Each level contains additional information such as:

-   Zone
-   Type
-   Reaction to monitor
-   Invalidation condition
-   Quantitative justification

Example:

    Zone: 4,365 – 4,381

    Type:
    Nearby support

    Observation:
    Potential reaction zone if price recovers and closes above the area.

    Invalidation:
    Sustained D1 close below the zone.

These zones are derived from historical price behavior and are not

presented as guaranteed reversal points.

------------------------------------------------------------------------

# 📰 Macroeconomic News & Catalysts

Price behavior alone does not explain every market movement.

For that reason, YerForex also includes a macroeconomic context section.

Relevant events may include:

-   CPI
-   PPI
-   Federal Reserve decisions
-   FOMC meetings
-   Interest-rate decisions
-   Other high-impact US economic releases

The news table includes:

  Field                    Description
  ------------------------ ---------------------------------
  Date / Time              Scheduled event time
  Event                    Economic catalyst
  Strength                 Estimated volatility importance
  Status                   Published / Scheduled
  XAU/USD interpretation   Potential market relevance
  Source                   Information source

------------------------------------------------------------------------

# 🔥 News Strength Classification

Macroeconomic events are classified by their potential to generate

volatility.

Examples:

    MODERATE
    STRONG
    VERY STRONG

The strength classification represents **potential volatility**.

It does **not** automatically predict market direction.

For example:

    VERY STRONG

means the event may produce significant volatility.

It does not mean Gold must rise or fall.

------------------------------------------------------------------------

# 🔮 Sunday--Friday Statistical Scenario

YerForex includes a projection module for the following trading week.

The projection chart contains:

### 🔵 Projected Open

Estimated starting level for each daily session.

### 🔴 Projected Close

Statistical closing scenario derived from historical weekday behavior.

### 📊 Projected Daily Range

Each session contains an estimated price interval.

The interval is displayed as a **shaded statistical range**.

Example:

    Projected High
          │
          │   Statistical Range
          │
    Projected Open
          │
    Projected Close
          │
          │
    Projected Low

This makes the expected volatility area easier to understand visually.

------------------------------------------------------------------------

# 📐 Projection Methodology

The projection module uses historical weekday statistics from the

four-week sample.

The model evaluates information such as:

    Median Monday Open → Close movement
    Median Tuesday Open → Close movement
    Median Wednesday Open → Close movement
    Median Thursday Open → Close movement
    Median Friday Open → Close movement

A conservative fraction of the historical movement is used to build

the central scenario.

The daily statistical range also considers the historical D1 range for

the corresponding weekday.

Conceptually:

    Historical weekday behavior
              ↓
    Median Open → Close movement
              ↓
    Conservative adjustment
              ↓
    Projected Close

and:

    Historical D1 ranges
            ↓
    Median weekday range
            ↓
    Statistical adjustment
            ↓
    Projected daily range

This methodology intentionally avoids assuming that historical movement

will repeat exactly.

------------------------------------------------------------------------

# 🧠 Facts vs. Projections

YerForex explicitly separates historical information from forecasts.

## HECHOS / FACTS

These values come directly from historical observations.

Examples:

    Historical Open
    Historical High
    Historical Low
    Historical Close
    20-day maximum
    20-day minimum
    Average D1 range
    Weekday frequencies

## PROYECCIÓN / PROJECTION

These values represent statistical scenarios.

Examples:

    Projected Open
    Projected Close
    Projected daily range
    Potential support reaction
    Potential resistance reaction

This distinction prevents statistical estimates from being confused

with actual market data.

------------------------------------------------------------------------

# 🏗️ System Architecture

YerForex is more than a Streamlit dashboard.

The project includes an automated architecture connecting AI-assisted

analysis with a production deployment workflow.

                  ┌─────────────────────┐
                  │   YerForex GPT      │
                  │  AI Analysis Layer  │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │     GPT Action      │
                  │      REST API       │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ Cloudflare Worker   │
                  │ Secure Middleware   │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │     GitHub API      │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ GitHub Repository   │
                  │ yerforex-dashboard  │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ Streamlit Community │
                  │       Cloud         │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ Interactive Market  │
                  │     Dashboard       │
                  └─────────────────────┘

------------------------------------------------------------------------

# 🤖 Automated Deployment Workflow

The deployment pipeline works as follows.

### Step 1 --- Market Analysis

Historical market information is collected and validated.

### Step 2 --- Quantitative Processing

The system analyzes:

    OHLC
    weekday behavior
    daily ranges
    support/resistance
    repeated patterns

### Step 3 --- Dashboard Generation

The Streamlit application is generated or updated.

### Step 4 --- GPT Action

The AI-assisted workflow communicates with the infrastructure through

a REST action.

### Step 5 --- Cloudflare Worker

A Cloudflare Worker acts as secure middleware.

Its responsibilities include:

    Authentication
    Request validation
    File authorization
    GitHub API communication

### Step 6 --- GitHub Update

Authorized dashboard files are updated through the GitHub API.

### Step 7 --- Streamlit Deployment

Streamlit Community Cloud detects the GitHub change.

### Step 8 --- Production Dashboard

The updated quantitative dashboard becomes available online.

The result is an automated pipeline:

    Market Data
         ↓
    Quantitative Analysis
         ↓
    AI-Assisted Generation
         ↓
    Secure API
         ↓
    GitHub
         ↓
    Automatic Deployment
         ↓
    Interactive Dashboard

------------------------------------------------------------------------

# 🔐 Security Architecture

Security was an important part of the project.

Sensitive credentials are **not stored directly inside the application**
source code\*\*.

Examples of protected credentials include:

    GitHub authentication token
    API authentication key

The architecture uses environment-level secrets instead.

Conceptually:

    GPT Action
         │
         │ Authenticated Request
         ▼
    Cloudflare Worker
         │
         ├── Authentication validation
         ├── File validation
         └── GitHub communication

The middleware restricts which repository files can be modified.

This reduces the attack surface of the automated deployment workflow.

------------------------------------------------------------------------

# ⚙️ Technology Stack

## Data & Analytics

-   Python
-   Pandas

## Visualization

-   Plotly

## Application

-   Streamlit

## Version Control

-   Git
-   GitHub

## Automation

-   GitHub API
-   REST APIs
-   GPT Actions

## Infrastructure

-   Cloudflare Workers
-   Streamlit Community Cloud

## AI-Assisted Development

-   ChatGPT
-   Custom GPT workflow

------------------------------------------------------------------------

# ⚡ Performance Optimization

The application is designed to run efficiently on Streamlit Community
Cloud.

Several optimizations were implemented.

### Data caching

    @st.cache_data

is used for calculations that do not need to run repeatedly.

### Reusable calculations

Historical statistics are calculated once and reused across the

dashboard.

### Lightweight visualizations

Plotly charts are generated without unnecessary repeated processing.

### No polling loops

The application avoids continuous background requests.

### No automatic refresh loops

The dashboard does not continuously rerun itself.

### Minimal dependencies

The project intentionally keeps its Python dependency list small.

Current core dependencies include:

    Streamlit
    Pandas
    Plotly

This improves deployment speed and reduces resource usage.

------------------------------------------------------------------------

# 📁 Repository Structure

The project intentionally keeps the production repository simple.

    yerforex-dashboard/
    │
    ├── streamlit_app.py
    │
    ├── requirements.txt
    │
    └── README.md

### `streamlit_app.py`

Main Streamlit application containing:

-   Data processing
-   Quantitative calculations
-   Weekly charts
-   Pattern analysis
-   Reaction levels
-   News table
-   Projection model
-   Dashboard interface

### `requirements.txt`

Defines the Python dependencies required by Streamlit Community Cloud.

### `README.md`

Technical documentation and project presentation.

------------------------------------------------------------------------

# 💻 Running YerForex Locally

Clone the repository:

    git clone https://github.com/YrHenao/yerforex-dashboard.git

Enter the project directory:

    cd yerforex-dashboard

Create a virtual environment:

    python -m venv .venv

Activate the environment.

### Windows

    .venv\Scripts\activate

### macOS / Linux

    source .venv/bin/activate

Install dependencies:

    pip install -r requirements.txt

Run Streamlit:

    streamlit run streamlit_app.py

The application will then be available through the local Streamlit

development server.

------------------------------------------------------------------------

# 🧪 Current Analysis Model

The current dashboard focuses on:

    Instrument: XAU/USD
    Timeframe: D1
    Historical sample: 4 complete trading weeks
    Sessions analyzed: 20

The architecture can later be extended to other instruments such as:

    EUR/USD
    GBP/USD
    USD/JPY
    AUD/USD
    USD/CAD
    XAG/USD

without changing the fundamental analytical workflow.

------------------------------------------------------------------------

# 🔄 Version Control & Recovery

Every production update is stored in GitHub.

This provides:

-   Version history
-   Change tracking
-   Rollback capability
-   Deployment traceability
-   Backup of stable dashboard versions

A previously working version can therefore be restored using Git rather

than rebuilding the entire application.

------------------------------------------------------------------------

# 🧩 Design Philosophy

YerForex was built around several principles.

### 1. Data before prediction

Historical data must be validated before generating a scenario.

### 2. Explain the statistics

The dashboard should not only calculate a result.

It should explain what the result means.

### 3. Separate facts from estimates

Historical observations and future projections must never be presented

as the same type of information.

### 4. Keep the interface understandable

Complex quantitative calculations should be translated into simple

visual explanations.

### 5. Automate repetitive deployment work

Once the analysis is generated, the deployment pipeline should require

minimal manual intervention.

------------------------------------------------------------------------

# 🧠 What I Learned Building YerForex

This project combines several areas of software development and
quantitative analysis.

During development I worked with:

-   Python data processing
-   Financial OHLC analysis
-   Statistical pattern detection
-   Interactive visualization
-   Streamlit application development
-   REST API architecture
-   API authentication
-   Cloudflare Workers
-   GitHub API integration
-   Automated deployment
-   Environment secrets
-   Cloud application optimization
-   AI-assisted software workflows

One of the most important lessons from the project was that building an

AI-assisted system is not only about generating analysis.

A production workflow also requires:

    Data validation
    Security
    Error handling
    Infrastructure
    Version control
    Resource optimization
    Clear user experience

------------------------------------------------------------------------

# 🚧 Challenges Solved

Some of the engineering challenges addressed during development

included:

### Cloud deployment compatibility

Python and package versions had to remain compatible with Streamlit

Community Cloud.

### Resource consumption

The application was optimized to avoid unnecessary reruns and excessive

CPU consumption.

### Secure GitHub automation

The AI workflow does not directly expose GitHub credentials.

A Cloudflare Worker provides a controlled middleware layer.

### Statistical interpretation

Historical patterns are expressed as frequencies and scenarios instead

of guaranteed market predictions.

### Visualization

Complex market information was converted into charts designed to be

understandable at a glance.

------------------------------------------------------------------------

# 🗺️ Future Roadmap

Possible future improvements include:

-   Multi-asset selection
-   EUR/USD analysis
-   GBP/USD analysis
-   USD/JPY analysis
-   XAG/USD analysis
-   Longer historical samples
-   Rolling pattern analysis
-   Volatility models
-   ATR integration
-   Economic-calendar automation
-   Automatic data ingestion
-   Backtesting
-   Pattern confidence scores
-   Multi-timeframe analysis
-   D1 / H4 comparison
-   Historical projection evaluation
-   Forecast-vs-actual tracking
-   Performance statistics
-   Automated report archives

------------------------------------------------------------------------

# 📊 Future Quantitative Research

One future direction for YerForex is to evaluate whether detected

weekday patterns remain stable across larger datasets.

For example:

    4 weeks
    12 weeks
    26 weeks
    52 weeks

The system could then compare:

    Short-term pattern
    vs.
    Medium-term pattern
    vs.
    Long-term pattern

This would help determine whether a detected pattern is persistent or

simply temporary.

------------------------------------------------------------------------

# 🎯 Project Objective

YerForex demonstrates how several technologies can be combined into a

single workflow:

    Quantitative Analysis
            +
    Financial Data
            +
    Artificial Intelligence
            +
    API Automation
            +
    Cloud Infrastructure
            +
    Interactive Visualization

The result is not just a market chart.

It is an end-to-end system that moves from historical market analysis

to an automatically deployed interactive application.

------------------------------------------------------------------------

# ⚠️ Disclaimer

YerForex is an **educational and quantitative research project**.

The information displayed by the application, including statistical

projections, historical patterns, support/resistance zones and

macroeconomic interpretations, is provided for educational and research

purposes.

Historical behavior does not guarantee future market behavior.

Nothing in this project should be interpreted as financial or

investment advice.

------------------------------------------------------------------------

# 👨‍💻 Author

**YerForex**

Quantitative market analytics, Python development, AI-assisted

automation and cloud deployment project.

------------------------------------------------------------------------

## ⭐ About This Repository

If you are reviewing this project from LinkedIn or my software/data

portfolio, this repository demonstrates practical experience with:

**Python · Pandas · Plotly · Streamlit · REST APIs · GitHub API ·**
Cloudflare Workers · Git · Cloud Deployment · Quantitative Analysis ·**
AI-Assisted Automation**

------------------------------------------------------------------------

### Built with Python + Streamlit + Plotly + Cloudflare + GitHub

**From market data → quantitative analysis → automated deployment.**
