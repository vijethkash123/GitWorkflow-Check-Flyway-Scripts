### GitWorkflow-Check-Flyway-Scripts
- We dealt with a problem, during subsequent merges of PRs working with Flyway Scripts.
- Flyway requires users to bump up the DB scripts, when we use it to do incremental updates on DB tables.
- If a user merges a PR with a script V2 to main, and another Dev tries to raise a PR with V2 script, the Github Workflow runner, gets into action, failing the build and stopping the user from merging the PR, hence later avoiding facing failures after the merge in the codepipeline.

### Tech used:
- Github APIs
- Git Workflows and Git Actions

### Markup language:
- YAML
