import os
import tempfile

def run_command(shell, command, is_command):
    os.system(os.system(command) if is_command else os.system(f"{shell} {command}"))

def run_command_with_proxy_export(shell, command, is_command, proxy_url):
    # Create a temp file
    fd, tmp_path = tempfile.mkstemp()
    try:
        with os.fdopen(fd, 'w+') as tmp:
            # Write commands to temp file
            export_command = f"export HTTP_PROXY={proxy_url}\nexport HTTPS_PROXY={proxy_url}\n"
            tmp.write(export_command)
            tmp.write(command if is_command else f"{shell} {command}")
            tmp.flush()

            # Run temp file
            os.system(f"{shell} {tmp_path}")
    finally:
        os.remove(tmp_path)
