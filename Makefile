define support-libs
	@pip install black
	@pip install isort
endef

health:
	@make --version
	@python --version

freeze:
	@pip install pipreqs
	@pipreqs src/whykay --savepath "requirements.txt" --force

setup: health
	@pip install -r requirements.txt
	@$(support-libs)

run: setup
	@python main.py

format:
	@isort src/whykay *.py
	@black src/whykay *.py

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

build-package:
	@python setup.py sdist

upload-package:
	@echo "Pushing to PyPi will only be possible if you have the right PYPI_TOKEN passed as an environment variable"
	@pwd
	@python -m twine upload dist/* --skip-existing -p $PYPI_PASSWORD -u $PYPI_USERNAME