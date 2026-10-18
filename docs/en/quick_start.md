# Quick start, or how to even use this thing

The project configuration lives in two places: `config/` holds the whole bot layout (server, channel and role IDs, infrastructure settings), while `.env` holds only the secrets that must not be committed.

Let’s go step by step.

Here is an example of the "secrets": [.env](../../.env.example)

## `.env` - secrets, what is what

- `MARIONETTE_TOKEN` is literally the heart of our presenter, aka the Discord bot. Go to the [Discord Developer Portal](https://discord.com/developers/applications), create your own application, grab the token from there, and paste it in.

- `DATABASE_URL`, `REDIS_URL` do not really need much tweaking. The example already has ready-to-go values made specifically for this project, and Docker will pick them up from your `.env` file automatically, so everything should work just fine :)

## `config/` - bot layout

- `config/discord/ids.yaml` - all the Discord IDs: the guild (`guild.main`), RP categories (`category.roleplay`), text channels (`text_channels`, onboarding included), forum channels (`forum_channels.character`) and roles (`roles`). An example with placeholders sits right next to it: [ids.example.yaml](../../config/discord/ids.example.yaml)

- `config/infrastructure.yaml` - database settings (pool size and overflow).

Everything is loaded by the `dature` library: yaml sections are mapped onto nested dataclasses, so the file structure and the structure of `bootstrap/config.py` match one to one.

# Makefile

Alright, we are done with the variables, so let’s move on. How do you run this? You have probably already seen the `make up` command in the `README`, but there are a few more interesting ones too.

## Start and stop

To start:

```bash
make up
```

To stop:

```bash
make down
```

## What else?

There is also `make restart`, which restarts both the app and the monitoring stack.

## Monitoring?

Yep. When you run `make up`, it also starts `Victoria Metrics` with `Grafana`, which you can later configure for better metrics.

You can also run monitoring separately with `make monitoring-up`, and stop it the same way with `make monitoring-down`.

## Logs

To watch container logs, you can use `make logs`. It will automatically attach you to the container logs.

## Cleanup

If `__pycache__` is annoying you, you can delete it with the very complicated command `make clear`.

# What if I do not want Docker?

Well, then things get more annoying. You will have to load `.env` variables into your environment manually, or use `python-dotenv`, which is not exactly the cleanest or nicest practice.

And in that case, forget about `make` - it only works with Docker. The only exception is `make clear`.

You will need: uv and Python 3.14.

Run `uv pip install -e .` - this will install Marionette as a separate package.

Then run `uv sync`, `python -m marionette`, but before that you will also need to start at least Postgres locally, and I am not going to explain that part here.
