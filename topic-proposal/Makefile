all:
	TEXINPUTS="./../sty/:" pdflatex topic-proposal
	TEXINPUTS="./../sty/:" bibtex topic-proposal
	TEXINPUTS="./../sty/:" pdflatex topic-proposal
	TEXINPUTS="./../sty/:" pdflatex topic-proposal
clean:
	rm topic-proposal.aux
	rm topic-proposal.log
	rm topic-proposal.out
	rm topic-proposal.pdf
	rm texput.log
lite:
	TEXINPUTS="./../sty/:" xelatex topic-proposal
