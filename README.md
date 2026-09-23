# Project Koios Bootstrap

A minimal coordination entry point for work spanning Project Koios
repositories. It may incubate bounded Project Koios-specific Pi coordination
candidates, but it owns no product code, architecture, live workflow state, or
persistent orchestration system.

## Start

Follow the upstream [Herdr quick start](https://herdr.dev/docs/quick-start/),
then start Pi from a Herdr-managed pane:

```bash
cd path/to/projectkoios-bootstrap
herdr
```

Inside the managed pane:

```bash
pi
```

Pi must inherit `HERDR_ENV=1`. If it does not, stop and start a new Pi session
inside Herdr; pane context cannot be added afterward.

## Operating model

1. Read the [repository map](maps/repositories.md).
2. Use `pi-intercom` to discover or contact repository sessions.
3. Use one visible Herdr-hosted Pi session per active repository.
4. Keep implementation, validation, and Git history in the owning repository.
5. Record cross-repository architecture in the `projectkoios` mothership.

See [AGENTS.md](AGENTS.md) for coordination rules and the
[harness-incubation policy](docs/harness-incubation.md) for candidate
boundaries. Git, GitHub, and owner repositories remain the durable record.
