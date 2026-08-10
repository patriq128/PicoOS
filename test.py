import subprocess

result = subprocess.run(
    [
        "mpremote",
        "exec",
        "from system.apps import apps_manager; apps_manager.main('list')"
    ],
    capture_output=True,
    text=True
)

apps = [
    app.strip()
    for app in result.stdout.splitlines()[1:]
    if app.strip()
]

print(apps)