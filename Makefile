SHELL=/bin/bash
devops_state = main
working_dir = `pwd`

install: local_build_and_deploy

reinstall : create_env && install

rebuild: 
	pip uninstall databricks_session -y \
	&& poetry build  \
	&& pip install .

local_build_and_deploy: 
	pip uninstall databricks_session -y \
	&& python setup.py install \
	&& databricks_session

package_build:
	python -m build

package_list:
	unzip -l dist/*.whl  

create_env:
	conda deactivate -n databricks_session \
	&& conda env remove -n databricks_session -y \
	&& conda create -n databricks_session python=3.10 -y \
	&& conda activate databricks_session
