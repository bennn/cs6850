all:
	TEXINPUTS="./../sty/:" pdflatex reaction-paper
	TEXINPUTS="./../sty/:" bibtex reaction-paper
	TEXINPUTS="./../sty/:" bpdflatex reaction-paper
	TEXINPUTS="./../sty/:" bpdflatex reaction-paper
clean:
	rm reaction-paper.aux
	rm reaction-paper.log
	rm reaction-paper.out
	rm reaction-paper.pdf
	rm texput.log
lite:
	TEXINPUTS="./../sty/:" xelatex reaction-paper
