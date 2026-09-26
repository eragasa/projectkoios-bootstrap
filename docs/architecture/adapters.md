# Adapter and integration boundaries

Project Koios bootstrap uses the adapter taxonomy incubated in
[`projectkoios-frankenstein` at `88ee1733`](https://github.com/eragasa/projectkoios-frankenstein/blob/88ee17332a5fdf0fddceedf8e08cbd55968cf8d7/docs/architecture/adapters/index.md).
The corresponding
[architecture](https://github.com/eragasa/projectkoios-frankenstein/blob/88ee17332a5fdf0fddceedf8e08cbd55968cf8d7/docs/architecture/adapters/architecture/index.md),
[specification](https://github.com/eragasa/projectkoios-frankenstein/blob/88ee17332a5fdf0fddceedf8e08cbd55968cf8d7/docs/architecture/adapters/specifications/index.md),
and
[tests](https://github.com/eragasa/projectkoios-frankenstein/tree/88ee17332a5fdf0fddceedf8e08cbd55968cf8d7/tests/projectkoios/frankensteins/adapters/base)
are the extraction source.

An **adapter** is a nominal boundary role. It deliberately has no generic
`adapt()` or `execute()` method.

- A **binding** adapts imported or deliberately vendored code. It owns
  dependency API translation and dependency identity, but grants no authority
  to invoke an external application or service.
- An **integration** adapts an external application or service. It owns
  executable or service selection, typed requests and results, bounded external
  effects and failures, artifacts, and external-version evidence.
- An integration may contain a binding through composition. It does not inherit
  from the binding or collapse both authorities into one hybrid role.

The bootstrap-local nominal classes live in
`projectkoios.bootstrap.adapters.base`. Provider behavior belongs beneath
`projectkoios.bootstrap.integrations.<provider>`. Shared package levels do not
re-export every implementation class; a provider leaf may expose an intentional
facade.

This extraction does not claim that bootstrap owns the eventual Project Koios
product-wide adapter taxonomy. The local classes bound coordination-harness
integrations while the source taxonomy remains incubated. Product adapters and
architecture still route to their owning repositories.
