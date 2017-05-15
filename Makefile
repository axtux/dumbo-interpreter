REPORT=rapport/rapport
NAMES=MAAZOUZ_LECOCQ

zip : clean
	mkdir $(NAMES)
	cp -lr src $(NAMES)/src
	cp -l $(REPORT).pdf $(NAMES)/rapport.pdf
	zip -r $(NAMES) $(NAMES)
	rm -r $(NAMES)
clean :
	rm -f $(REPORT).aux $(REPORT).log $(REPORT).synctex.gz $(REPORT).toc
	rm -fr src/__pycache__/
	rm -f src/parsetab.py src/parser.out
	rm -f $(NAMES).zip
