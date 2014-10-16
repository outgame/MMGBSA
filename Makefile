all: mmgbsa

scp: scp.py
	/opt/schrodinger/suites2014-2/run scp.py

mmgbsa: mmgbsa.py
	/opt/schrodinger/suites2014-2/run mmgbsa.py

clean:
	rm *.inp *.maegz *.log *~