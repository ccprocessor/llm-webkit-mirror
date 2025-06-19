MathJax.Hub.Config({
    tex2jax: {inlineMath: [["$","$"],["\\(","\\)"],["`","`"]]},

    "HTML-CSS": { linebreaks: { automatic: true, width: "65% container" } },
    SVG: { linebreaks: { automatic: true, width: "65% container" } },

    TeX: {
	equationNumbers: {  autoNumber: "AMS"  },

    Macros: {
	goodbreak: '\\mmlToken{mo}[linebreak="goodbreak"]{}',
	badbreak: ['\\mmlToken{mo}[linebreak="badbreak"]{#1}',1],
	nobreak: ['\\mmlToken{mo}[linebreak="nobreak"]{#1}',1],
	invisibletimes: ['\\mmlToken{mo}{\u2062}'],
	cdotbadbreak: '\\badbreak{\u22C5}',
	timesbadbreak: '\\badbreak{\u00D7}',

	diff: ['\\frac{\\mathrm{d} #1}{\\mathrm{d} #2}',2],
	diffn: ['\\frac{\\mathrm{d}^{#3} #1}{\\mathrm{d} #2^{#3}}',3],
	pdiff: ['\\frac{\\partial #1}{\\partial #2}',2],
	pdiffn: ['\\frac{\\partial^{#3} #1}{\\partial #2^{#3}}',3],
	vc: ['\\mathbf{#1}',1],
	R: '\\mathbf{R}',
	tr: '\\mathop{\\rm tr}',
	blue: '\\color{blue}{\\textbf{blue}}',
	red: '\\color{red}{\\textbf{red}}',
	green: '\\color{green}{\\textbf{green}}',
	cyan: '\\color{cyan}{\\textbf{cyan}}',
	magenta: '\\color{magenta}{\\textbf{magenta}}',
	curl: '\\mathop{\\text{curl}}',
	div: '\\mathop{\\text{div}}',
	norm: ['\\|#1\\|',1],

	//arclength symbol
	arcLengthSymbol: 's',
	als: '\\arcLengthSymbol',

	//symbol for differential in vector-valued line integral
	lineIntegralSymbol: '\\vc{s}',
	lis: '\\lineIntegralSymbol',

	//surace area symbol
	surfaceAreaSymbol: 'S',
	sas: '\\surfaceAreaSymbol',

	//symbol for differential in vector-valued surface integral
	surfaceIntegralDifferential: '\\vc{S}',
	sid: '\\surfaceIntegralDifferential',

	///////////////////////////////
	//formats for various integrals
	///////////////////////////////

	//vector line integrals
	lineIntegral: ['\\int_{#1} #2  \\cdot d\\lis', 2],
	lint: ['\\lineIntegral{#1}{#2}',2],

	closedLineIntegral: ['\\oint_{#1} #2 \\cdot d\\lis',2],
	clint: ['\\closedLineIntegral{#1}{#2}',2],

    	//scalar line integrals
	scalarLineIntegral: ['\\int_{#1} #2 \\,d\\als',2],
	slint: ['\\scalarLineIntegral{#1}{#2}',2],

	closedScalarLineIntegral: ['\\oint_{#1} #2 \\,d\\als',2],
	cslint: ['\\closedScalarLineIntegral{#1}{#2}',2],

	//vector surface integrals
	surfaceIntegral: ['\\iint_{#1} #2 \\cdot d\\sid',2],
	sint: ['\\surfaceIntegral{#1}{#2}',2],

	//scalar surface interals
	scalarSurfaceIntegral: ['\\iint_{#1} #2 \\,d\\sas',2],
	ssint: ['\\scalarSurfaceIntegral{#1}{#2}',2],

	//parametrized versions of integrals
	//vector line integrals
	parametrizedLineIntegral: ['\\int_{#1}^{#2} #3(#4(t)) \\cdot #4\'(t) dt',4],
	plint: ['\\parametrizedLineIntegral{#1}{#2}{#3}{#4}',4],

	//scalar line integrals
	parametrizedScalarLineIntegral: ['\\int_{#1}^{#2} #3(#4(t)) \\norm{#4\'(t)} dt',4],
	pslint: ['\\parametrizedScalarLineIntegral{#1}{#2}{#3}{#4}',4],

	//vector surface integrals
	parametrizedSurfaceIntegral: ['\\int_{#1}^{#2}\\int_{#3}^{#4} #5(#6(#7,#8)) \\cdot \\left( \\pdiff{#6}{#7}(#7,#8) \\times \\pdiff{#6}{#8}(#7,#8) \\right) d#7\\,d#8',8],
	psint: ['\\parametrizedSurfaceIntegral{#1}{#2}{#3}{#4}{#5}{#6}{#7}{#8}', 8],

	//vector surface integrals, reverse normal vector
	parametrizedSurfaceIntegralReverseNormal: ['\\int_{#1}^{#2}\\int_{#3}^{#4} #5(#6(#7,#8)) \\cdot \\left( \\pdiff{#6}{#8}(#7,#8) \\times \\pdiff{#6}{#7}(#7,#8) \\right) d#7\\,d#8', 8],
	psintrn: ['\\parametrizedSurfaceIntegralReverseNormal{#1}{#2}{#3}{#4}{#5}{#6}{#7}{#8}', 8],

	//vector surface integrals, reverse normal vector, reverse integration order
	parametrizedSurfaceIntegralReverseNormalReverseOrder: ['\\int_{#1}^{#2}\\int_{#3}^{#4} #5(#6(#7,#8)) \\cdot \\left( \\pdiff{#6}{#8}(#7,#8) \\times \\pdiff{#6}{#7}(#7,#8) \\right) d#8\\,d#7',8],
	psintrnro: ['\\parametrizedSurfaceIntegralReverseNormalReverseOrder{#1}{#2}{#3}{#4}{#5}{#6}{#7}{#8}', 8],

	//vector surface integrals, reverse integration order
	parametrizedSurfaceIntegralReverseOrder: ['\\int_{#1}^{#2}\\int_{#3}^{#4} #5(#6(#7,#8)) \\cdot \\left( \\pdiff{#6}{#7}(#7,#8) \\times \\pdiff{#6}{#8}(#7,#8) \\right) d#8\\,d#7',8],
	psintro: ['\\parametrizedSurfaceIntegralReverseOrder{#1}{#2}{#3}{#4}{#5}{#6}{#7}{#8}', 8],

	//vector surface integrals, over region
	parametrizedSurfaceIntegralOverRegion: ['\\iint_{#1} #2(#3(#4,#5)) \\cdot \\left( \\pdiff{#3}{#4}(#4,#5) \\times \\pdiff{#3}{#5}(#4,#5) \\right) d#4\\,d#5',5],
	psintor: ['\\parametrizedSurfaceIntegralOverRegion{#1}{#2}{#3}{#4}{#5}',5],

	//scalar surface integrals
	parametrizedScalarSurfaceIntegral: ['\\int_{#1}^{#2}\\!\\!\\!\\int_{#3}^{#4} #5(#6(#7,#8)) \\invisibletimes \\left\\| \\pdiff{#6}{#7}(#7,#8) \\times \\pdiff{#6}{#8}(#7,#8) \\right\\| d#7\\,d#8',8],
	pssint: ['\\parametrizedScalarSurfaceIntegral{#1}{#2}{#3}{#4}{#5}{#6}{#7}{#8}', 8],

	//scalar surface integrals, reverse integration order
	parametrizedScalarSurfaceIntegralReverseOrder: ['\\int_{#1}^{#2}\\int_{#3}^{#4} #5(#6(#7,#8)) \\left\\| \\pdiff{#6}{#7}(#7,#8) \\times \\pdiff{#6}{#8}(#7,#8) \\right\\| d#8\\,d#7',8],
	pssintro: ['\\parametrizedScalarSurfaceIntegralReverseOrder{#1}{#2}{#3}{#4}{#5}{#6}{#7}{#8}', 8],

	//scalar surface integrals, over region
	parametrizedScalarSurfaceIntegralOverRegion: ['\\iint_{#1} #2(#3(#4,#5)) \\left\\| \\pdiff{#3}{#4}(#4,#5) \\times \\pdiff{#3}{#5}(#4,#5) \\right\\| d#4\\,d#5',5],
	pssintor: ['\\parametrizedScalarSurfaceIntegralOverRegion{#1}{#2}{#3}{#4}{#5}',5],


	//default letters for objects
	//regions (2D)
	defaultLetterRegion: 'D',
	dlr: '\\defaultLetterRegion',

	//volumes (3D)
	defaultLetterVolume: 'W',
	dlv: '\\defaultLetterVolume',

	//curves
	defaultLetterCurve: 'C',
	dlc: '\\defaultLetterCurve',
	alternateDefaultLetterCurve: 'B',
	adlc: '\\alternateDefaultLetterCurve',
	secondAlternateDefaultLetterCurve: 'E',
	sadlc: '\\secondAlternateDefaultLetterCurve',

	//surfaces
	defaultLetterSurface: 'S',
	dls: '\\defaultLetterSurface',

	//vector fields
	defaultLetterVectorField: '\\vc{F}',
	dlvf: '\\defaultLetterVectorField',
	defaultLetterVectorFieldComponent: 'F',
	dlvfc: '\\defaultLetterVectorFieldComponent',
	alternateDefaultLetterVectorField: '\\vc{G}',
	adlvf: '\\alternateDefaultLetterVectorField',
	alternateDefaultLetterVectorFieldComponent: 'G',
	adlvfc: '\\alternateDefaultLetterVectorFieldComponent',

	//scalar integrals
	defaultLetterScalarIntegrand: 'f',
	dlsi: '\\defaultLetterScalarIntegrand',

	//line parameterization
	defaultLetterLineParameterization: '\\vc{c}',
	dllp: '\\defaultLetterLineParameterization',
	defaultLetterLineParameterizationComponent: 'c',
	dllpc: '\\defaultLetterLineParameterizationComponent',
	alternateDefaultLetterLineParameterization: '\\vc{p}',
	adllp: '\\alternateDefaultLetterLineParameterization',
	alternateDefaultLetterLineParameterizationComponent: 'p',
	adllpc: '\\alternateDefaultLetterLineParameterizationComponent',
	secondAlternateDefaultLetterLineParameterization: '\\vc{q}',
	sadllp: '\\secondAlternateDefaultLetterLineParameterization',
	secondAlternateDefaultLetterLineParameterizationComponent: 'q',
	sadllpc: '\\secondAlternateDefaultLetterLineParameterizationComponent',
	thirdAlternateDefaultLetterLineParameterization: '\\vc{d}',
	tadllp: '\\thirdAlternateDefaultLetterLineParameterization',
	thirdAlternateDefaultLetterLineParameterizationComponent: 'd',
	tadllpc: '\\thirdAlternateDefaultLetterLineParameterizationComponent',

	//surface parameterization
	defaultLetterSurfaceParameterization: '\\vc{\\Phi}',
	dlsp: '\\defaultLetterSurfaceParameterization',
	defaultLetterSurfaceParameterizationComponent: '\\Phi',
	dlspc: '\\defaultLetterSurfaceParameterizationComponent',

	//variables for surface parameters
	surfaceParameterFirstVariable: 'u',
	spfv: '\\surfaceParameterFirstVariable',
	surfaceParameterSecondVariable: 'v',
	spsv: '\\surfaceParameterSecondVariable',

	//change of variable function
	changeVariableFunction: '\\vc{T}',
	cvarf: '\\changeVariableFunction',
	changeVariableFunctionComponent: 'T',
	cvarfc: '\\changeVariableFunctionComponent',

	//default variables for change of variables
	changeVariableFirstVariable: 'u',
	cvarfv: '\\changeVariableFirstVariable',
	changeVariableSecondVariable: 'v',
	cvarsv: '\\changeVariableSecondVariable',
	changeVariableThirdVariable: 'w',
	cvartv: '\\changeVariableThirdVariable',

	//potential function
	defaultLetterPotentialFunction: 'f',
	dlpf: '\\defaultLetterPotentialFunction',

	//default combo shortcuts (combining the above)
	//vector line integral
	defaultLineIntegral: '\\lint{\\dlc}{\\dlvf}',
	dlint: '\\defaultLineIntegral',
	defaultClosedLineIntegral: '\\clint{\\dlc}{\\dlvf}',
	dclint: '\\defaultClosedLineIntegral',
	defaultParametrizedLineIntegral: '\\plint{a}{b}{\\dlvf}{\\dllp}',
	dplint: '\\defaultParametrizedLineIntegral',

	//scalar line integral
	defaultScalarLineIntegral: '\\slint{\\dlc}{\\dlsi}',
	dslint: '\\defaultScalarLineIntegral',
	defaultClosedScalarLineIntegral: '\\cslint{\\dlc}{\\dlsi}',
	dcslint: '\\defaultClosedScalarLineIntegral',
	defaultParametrizedScalarLineIntegral: '\\pslint{a}{b}{\\dlsi}{\\dllp}',
	dpslint: '\\defaultParametrizedScalarLineIntegral',

	//vector surface integral
	defaultSurfaceIntegral: '\\sint{\\dls}{\\dlvf}',
	dsint: '\\defaultSurfaceIntegral',
	defaultParametrizedSurfaceIntegral: '\\psintor{\\dlr}{\\dlvf}{\\dlsp}{\\spfv}{\\spsv}',
	dpsint: '\\defaultParametrizedSurfaceIntegral',

	//scalar surface integral
	defaultScalarSurfaceIntegral: '\\ssint{\\dls}{\\dlsi}',
	dssint: '\\defaultScalarSurfaceIntegral',
	defaultParametrizedScalarSurfaceIntegral: '\\pssintor{\\dlr}{\\dlsi}{\\dlsp}{\\spfv}{\\spsv}',
	dpssint: '\\defaultParametrizedScalarSurfaceIntegral',

	//jacobian matrix
	JacobianMatrix: ['D{#1}',1],
	jacm: ['\\JacobianMatrix{#1}',1],

    }
  }

});

MathJax.Ajax.loadComplete("/static/mathjaxconfig/midefault.js");
