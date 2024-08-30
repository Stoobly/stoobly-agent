app_name=app

app_dir_path=/tmp/$app_name
service_name=service
workflow_name=workflow

rm -rf $app_dir_path

cwd=$(pwd)
mkdir -p $app_dir_path
cd $app_dir_path
stoobly-agent init
cd $cwd

# --- App Create
poetry run stoobly-agent scaffold app create --app-dir-path $app_dir_path $app_name

# --- Service Create

# Tests: threat-dashboard
poetry run stoobly-agent scaffold service create --app-dir-path $app_dir_path --hostname http.badssl.com --scheme http --port 80 --workflow record --workflow mock service

# Tests: assets
#poetry run stoobly-agent scaffold service create --app-dir-path $app_dir_path --hostname http.badssl.com --scheme http --port 80 service --proxy-mode reverse:http://assets:8080 --detached

# Tests: tests
#poetry run stoobly-agent scaffold service create --app-dir-path $app_dir_path --hostname http.badssl.com --scheme http --port 80 service --detached

# Tests: enable-intercept
#poetry run stoobly-agent scaffold service create service --app-dir-path $app_dir_path

# --- Workflow Create
#poetry run stoobly-agent scaffold workflow create --app-dir-path $app_dir_path --service-name $service_name $workflow_name

# --- Workflow Run
target_workflow_name=record
poetry run stoobly-agent scaffold workflow run --app-dir-path $app_dir_path --data-dir-path $app_dir_path $target_workflow_name
poetry run stoobly-agent scaffold workflow logs --app-dir-path $app_dir_path $target_workflow_name
