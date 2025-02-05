echo "Jai Shree Ram"
user_name=$(whoami)
path_to_env="/home/${user_name}/.cache/pypoetry/virtualenvs/chainmind-os-*"
if [ -d $path_to_env ]; then
  echo "Found the existing environment!!"
else
  echo "Creating a working environment ..."
  poetry install --no-root

fi
echo -e "\n\nActivating the working environment..."

export PYTHONPATH="${PYTHONPATH}:$(pwd)"
poetry shell