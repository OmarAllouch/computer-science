REPO = SBoudrias/Inquirer.js

1:
	@python 01/main.py

3:
	@python 03/main.py
	@echo
	@python 03/geo-info.py

4:
	@python 04/main.py $(REPO)

all:
	@echo "Running 01/main.py"
	@python 01/main.py
	@echo
	@echo "Running 03/main.py"
	@python 03/main.py
	@echo
	@python 03/geo-info.py
	@echo
	@echo "Running 04/main.py"
	@python 04/main.py $(REPO)
