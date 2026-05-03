[![CI](https://github.com/MagM1go/marionette/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/MagM1go/marionette/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.14-blue)
![Coverage](https://img.shields.io/badge/coverage-88%25-brightgreen)
![License](https://img.shields.io/github/license/MagM1go/marionette)

!!! If some parts of this text sound a bit unnatural, it is because I used AI to translate it. My English is not very good yet. !!!

[🇷🇺 Original (Russian) version](README.md)

# HIKARI // Marionette

Let me say this right away: this is basically an application hidden inside a **Discord** bot.

So this README explains what it is, what inspired it, and why there is clean architecture here at all, and whether that counts as overengineering.

This is not a tutorial project, and it does not claim to be perfect. If you find any **serious** issues (that are not mentioned below), [please do](https://github.com/MagM1go/marionette/pulls)

---

# For those hoping to find something important here!

If you know me and just decided to look through my repositories, please read on. You might even already be familiar with the project.

If you want to extract practical information from this, this README will not be entirely relevant to you, though there will still be useful bits here, do not worry. There is some technical info, a bit on how to launch this beast, a bit of everything, really. Maybe I will add some lightweight project documentation later, but this is a local project with very specific subject matter, so I honestly have no idea who would need it besides me. So this is not a README in the usual sense. Please keep that in mind.

TL;DR: this is a local and niche project, so the README is more introductory than technically exhaustive.

---

# A bit of boring stuff

You can find some more detailed info about running the project and a few other things [here](docs/en/quick_start.md)

---

# So what is it for?

It exists to implement mechanics from my fictional world. Doing all of that manually in Discord would have been tedious and boring, so the bot automated it. It also removes the annoying need to manually moderate certain kinds of specific content that would be awful to clean up by hand.

---

# Is it overengineered, and what is the architecture like?

Yes, for a local and niche bot, something simpler probably would have been enough. That choice was intentional.

Now imagine this: you board a plane, then suddenly remember you are the pilot. What do you do?
Open `src/marionette/` and see this:

* `application/usecases/` - the things the bot juggles in commands or in any feature where the user needs to be involved
* `application/protocols/` - repository protocols. Just descriptions. Nothing more.
* `domain/policies` - some business rules that define how certain scenarios should be handled properly
* `domain/services/rating_service.py` - the heart of the rating system, and honestly of the whole world this application was made for
* `infrastructure/repositories/` - the fishing rods that pull all the required data out of the database. Implemented on top of `protocols/`
* `presentation/discord/` - probably the reason you came here in the first place
* `presentation/discord/presenters` - a neat and pleasant abstraction layer for messages, embeds, and the rest of the Discord circus
* `tests/*` - probably self-explanatory

---

# Alright, so what can it do as a Discord bot?

I am not going to drag you into the game's setting here. A Discord server will show up later, and you will be able to click around and try things yourself. But the basics are:

* Entering and leaving locations
* Posting news
* Paparazzi
* Rating system
* Auto-moderation of unwanted non-RP content in RP chats
* Onboarding for new users

---

# Inspiration

The bot was made for a local and very specific community, namely a roleplay project inspired by the Japanese entertainment industry, with a layer of anime and manga aesthetics from **Oshi no Ko**

A bit childish and naive as an idea, maybe, but I liked it. If you are not into that kind of thing, feel free to skip this part of the README.

---

## Rating

The rating system was partially inspired by a mechanic from MLBB (Mobile Legends: Bang Bang), specifically the seasonal rank reset.

The idea of making rating gain harder as your rating gets higher is my own.

## Paparazzi

Inspired by the OnK episode where Kana gets tracked down by paparazzi.

## News

Well, news is news... It helps create a sense of a living world, at least in my opinion.

## Onboarding

This one I made simply because I wanted to, and it seems like it might actually lower the barrier to getting into RP.

---

# For nerds

This runs on Python 3.14. Everything else is in `pyproject.toml`.

Clean architecture, yes, partly overengineering, but this was mostly a learning project, and it helped me understand how to write architecture more properly and what direction to think in overall. I would recommend reading about coupling and cohesion if we are talking architecture.

Still, I agree with Bob Martin on one thing: **good** architecture should be easy to test.

## A bit more info:

This ships with PostgreSQL, Redis, and everyone's favorite or least favorite SQLAlchemy. Migrations run through alembic, and the driver is psycopg.

Package manager: `uv`.

Containerization via **Docker**.

Why this stack? Because I felt like it. PostgreSQL is cool, Redis has a vibe, SQLAlchemy works for a project like this, alembic is convenient, and the driver was there purely because I got curious what kind of pokemon it was. Before writing Marionette, I did not know about it. As it turns out, asyncpg is more efficient and better than psycopg in pretty much every way, so draw your own conclusions.

## The architecture itself

```bash
├── src                         # src-layout
│   └── marionette
│       ├── application/        # Application layer, use cases live here and everything the app is supposed to do happens here
│       ├── bootstrap/          # Entry point + DI
│       ├── domain/             # Business logic, business rules, and entities
│       ├── infrastructure/     # Interaction with the outside world
│       ├── presentation/       # How the app is shown to the outside world
```

## So where is the ignition key?

First:

```python
python3 -m pip install uv
```

Before launching, edit `.env`

Manual setup:

```bash
uv pip install -e .
uv lock
uv run python -m marionette
# but metrics will not come up that way, so do with that what you will
```

Containerized:

```bash
make up
# and you can restart it with
make restart
# Available flags: DETACH (defaults to 1), BUILD (defaults to 0)
```

> [!WARNING]
> Please take your own environment into account. These commands are tailored to my setup. Your Docker version and Docker Compose version may differ.

## So what are the compromises?

There is an article on Habr about misconceptions around clean architecture, [here it is](https://habr.com/ru/companies/mobileup/articles/335382/)

And what can I point out in my own case... I do not have interactors. Honestly, I did not fully understand the article. At first it says that according to Bob Martin, `Interactors` are just another name for Use Cases, and then further down it says there are interactors for the use case *layer*. So I decided not to overthink it and just left the use cases as they are. In my project, they act like regular orchestrators with a small amount of business logic mixed in. I did not separate everything with absolute strictness.

In the domain layer, I diverge from Bob Martin pretty heavily: in `entities/`, I keep SQLAlchemy models, which goes against the book's canon. But I made that compromise consciously. Well... let's say it was gently explained to me that with relationships, doing it this way is better, simpler, and faster. Overall, I agree. It really is more convenient. Though yes, moving away from SQLAlchemy later would be harder. Fair enough. But not *that* much harder. This was also decided with the expected size of the codebase in mind, and I already know what its upper limit is.

So yeah, hopefully there will not be too many unnecessary complaints. I am not going to go deep into what exactly is more convenient and why. No one is going to read this section anyway.

> [!NOTE]
> **Environment everything was created and tested in:**
>
> Python 3.14.2 (main, Jan 10 2026, 19:46:42) [GCC 15.2.1 20260103] on linux
>
> Docker: Docker version 29.1.4, build 0e6fee6c52
>
> Docker Compose version 5.0.1
>
> uv 0.9.26
