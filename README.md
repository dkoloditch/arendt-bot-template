# arendt-bot-template

This is a basic [LangChain](https://www.langchain.com) app that ingests provided
nonviolent literature and news articles, then outputs the context of the news in
terms of authoritarianism along with nonviolent tactics.

The impetus is to provide simple, quick, digestible context and helpful guidance
around complicated and fast-moving news events for pro-democracy movements.

## Setup

Create a `.env` file in root of project directory and add the following. You'll
need an [Anthropic API key](https://console.anthropic.com/settings/keys) to
generate responses.

```yaml
ANTHROPIC_API_KEY=your_api_key_here
```

Install [pyenv](https://github.com/pyenv/pyenv?tab=readme-ov-file#installation)
and `python` (Mac).

```bash
brew install pyenv
pyenv install 3.13
pyenv local 3.13
```

Install `poetry`, make sure to add the path to your shell config, then reload
your shell.

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Activate `poetry`.

```bash
eval $(poetry env activate)
```

Run the app.

```bash
python src/main.py
```

Exit the poetry shell.

```bash
deactivate
```