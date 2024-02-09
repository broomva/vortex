SHELL=/bin/bash
devops_state = main
working_dir = `pwd`

install: local_build_and_deploy

reinstall : create_env && install

rebuild: 
	pip uninstall vortex -y \
	&& poetry build  \
	&& pip install .

local_build_and_deploy: 
	pip uninstall vortex -y \
	&& python setup.py install \
	&& vortex

package_build:
	python -m build

package_list:
	unzip -l dist/*.whl  

create_env:
	conda deactivate -n vortex \
	&& conda env remove -n vortex -y \
	&& conda create -n vortex python=3.11 -y \
	&& conda activate vortex

docker_build:
	docker build -t vortex:latest .

docker_run:
	docker run -p 3000:3000 --name vortex-flows vortex:latest  

deploy_service:
	dagster-webserver -h 0.0.0.0 -p 3001 && dagster-daemon run  

deploy_api:
	python -m uvicorn vortex.api:app --reload && ngrok http 8000