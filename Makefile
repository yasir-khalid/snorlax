define support-libs
	@pip install black
	@pip install isort
endef

health:
	@make --version
	@python --version

freeze:
	@pip install pipreqs
	@pipreqs . --force
	@conda env export > environment.yml

setup: health
	@pip install -r requirements.txt
	@$(support-libs)

run: setup
	@python main.py

format:
	@isort *.py
	@black *.py

vault-push:
	@npx dotenv-vault push

vault-pull:
	@npx dotenv-vault pull

vault-open: 
	@npx dotenv-vault open -y
	# alternatively you can visit `ui.dotenv.org`

vault-setup:
	@npx dotenv-vault new -y

vault-login:
	@npx dotenv-vault login -y

upload-package:
	@python -m twine upload dist/* --skip-existing -p $(PYPI_PASSWORD) -u $(PYPI_USERNAME)