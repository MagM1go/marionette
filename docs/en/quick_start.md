# Quick start, or how to even use this thing

First of all, check the `.env` file. Right now, it is the main place where all variables, secrets, and all that stuff live. Maybe later this will be moved into separate config files, but for now this is the only way.

Let’s go step by step.

Here is an example of the "config": [.env](../../.env.example)

## Environment variables, what is what

### Important!
- `MARIONETTE_TOKEN` is literally the heart of our presenter, aka the Discord bot. Go to the [Discord Developer Portal](https://discord.com/developers/applications), create your own application, grab the token from there, and paste it in.

- `DATABASE_URL`, `DATABASE_POOL_SIZE`, `DATABASE_MAX_OVERFLOW`, `DATA_SOURCE_NAME`, `REDIS_URL` do not really need much tweaking. The example already has ready-to-go values made specifically for this project, and Docker will pick them up from your `.env` file automatically, so everything should work just fine :)

- `MAIN_GUILD_ID` - the bot was built for a local community, so it is designed around one server, not public multi-server use. Because of that, you will need to choose one server where the bot will run.

### Not that important anymore...
All variables below are kind of needed, but also kind of not. Some features depend on them, but overall the bot will still start without them. If you do not need some part of the functionality, you can just remove those variables and cut the related code out of the project.

## Why does `RP_CATEGORIES` look so weird?
Because this project uses the `dature` library, and it can read variables like this as Python lists. That is why the syntax looks like that.

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
