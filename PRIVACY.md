# Privacy

Blueprint Signal does not implement telemetry, advertising, user accounts, tracking pixels, or outbound data uploads. Files and pasted text are processed by the running Streamlit application. The AI route is copy and paste only: the app writes a prompt for you to take to an assistant of your choice and never contacts an AI service itself. If someone deploys the app, that operator controls infrastructure logs, retention, authentication, backups, and network access and must document those practices separately.

Do not upload personal or confidential data to a deployment you do not control. Prefer de-identified identifiers and apply appropriate access, retention, and disclosure controls.

Inside Signal Hub, Blueprint Signal runs in Hub mode: uploads stay in the session's memory, the fictional demo is preloaded, and nothing is written to disk.

