# Novelix-Agent
Novelix is an expert-level AI agent designed to help students, academics, and professionals generate mature, logical, and novel research ideas. It moves beyond simple brainstorming by employing a rigorous, multi-phase process of inquiry, evidence-based web research, and creative synthesis.

## Project Goal

The primary goal of Novelix is to bridge the gap between a user's initial curiosity and a well-formed, testable research question. It achieves this by systematically understanding the user's domain, performing targeted searches to identify knowledge gaps and emerging trends, and then synthesizing this information into innovative research proposals that are grounded in established academic frameworks.

## Features

- **Multiple Research Frameworks**: Select from a dropdown of established research idea generation frameworks (e.g., PICOT, SPICE, CHIP) to structure the output. An "Auto-Select" option allows the agent to choose the most appropriate framework for your domain.
- **Interactive Deep Inquiry**: The agent initiates a two-phase dialogue to deeply understand your goals, context, and existing knowledge before starting its research.
- **AI-Powered Synthesis**: Novelix uses your answers as a starting point to perform live web searches with the Tavily API, actively seeking out knowledge gaps, novel methodologies, and state-of-the-art findings.
- **Transparent Reasoning**: An expandable "Thinking..." log in the UI shows the agent's real-time internal monologue, including its search queries, self-critique, and synthesis process.
- **Structured, Novel Output**: The final output consists of 5-6 concise, research questions that are creatively synthesized from your input and the agent's research—not just a rephrasing of what you already said.

## Tech Stack

- **AI Framework**: LangChain
- **Language Model**: OpenAI GPT-4 Series
- **Search**: Tavily Search API
- **UI**: Streamlit
- **Dependency Management**: Poetry

## Installation and Setup

Follow these steps to run Novelix locally.

### 1. Prerequisites

- Python 3.9+ 
- [Poetry](https://python-poetry.org/docs/#installation) installed for dependency management.

### 2. Clone the Repository

```bash
git clone https://github.com/mehrdadameri/Novelix-Agent.git
cd Novelix-Agent
```

### 3. Install Dependencies

Use Poetry to install the required Python packages from the `pyproject.toml` file.

```bash
poetry install --no-root
```

### 4. Set Up Environment Variables

You will need API keys for OpenAI and Tavily Search.

Add your API keys to the `.env.example` file:

```bash
OPENAI_API_KEY=YOUR_API_KEY
TAVILY_API_KEY=YOUR_API_KEY
```

Don't forget to rename the `.env.example` to `.env`.

## Running the Application

Once the setup is complete, you can run the Streamlit application from the `Novelix-Agent` root directory.

```bash
run streamlit run app.py
```
The application will open in your web browser automatically.
