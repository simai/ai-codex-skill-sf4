# When To Stop And Ask

Stop and ask the user when:

- multiple valid site roots or site dirs exist and the target is unclear;
- a required config file is missing (for example `.wizard.config.php` or a
  `*.config.php` expected by the flow);
- the task requests direct system-layer edits that break the update-safe policy;
- the task depends on undocumented project-specific behavior (custom editor
  entrypoints, custom deploy policy).
