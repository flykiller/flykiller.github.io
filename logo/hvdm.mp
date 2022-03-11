%	Macros for inclusion in Metapost
% 	author: Hans van der Meer
message "Loading file hvdm.mp";
% 2008-10-16: added pencircle around label drawing with textext - luatex failed
% 2010-03-29: removed transparent color from tihis code => error in LuaTeX
% 2011-11-03: changes in color handling, needs ConTeXt beta 2011-1102 or later
% 2013-08-27: convenience macros for color handling added
% 2013-08-27: arrow drawing simplified and more flexibel
% 2013-09-05: enabled modifier on Label
%	=========================== General macros ===========================

% General scratchstring, use it only temporarily.
newinternal scratchstring_; string scratchstring_;

% Access to width (x) and height (y) of current pen
vardef penX = (xpart rt origin - xpart lft origin) enddef;
vardef penY = (ypart top origin - ypart bot origin) enddef;

% Get and reset pen; note that not nestable.
newinternal savepen_;
def getpen(expr p) =
	savepen_ := savepen;
	pickup p;
enddef;
def storepen = savepen_ := savepen; enddef;
def restorepen = pickup savepen_; enddef;

% Calculate point bisecting in triangle corner b-a-c.
def bisect(expr a, b, c) =
	whatever[b,c] = a + whatever * dir(0.5(angle(b-a)+angle(c-a)))
enddef;

%	====================== Reprogrammed plain macros ======================

% redefine intersectionpoint in order to get rid of errmessage
secondarydef p intersectionpoint q =
	begingroup
	save x_, y_;
	(x_,y_) = p intersectiontimes q;
	if x_ < 0:
		% errmessage("The paths don't intersect");
		origin
	else:
		.5[point x_ of p, point y_ of q]
	fi
	endgroup
enddef;

% Drawing with additional operation after the _op_ from drawoptions.
% At the end of the draw call the addtional operation is erased.
% Especially needed to fool textext, which uses draw somewhere.
% Without this trick we cannot switch the textcolor only during
% the typesetting of a label.

def drawoptions(text t) =
  def _op_ = t __op__ enddef
enddef;

def extradrawoptions(text t) =
	def __op__ = t enddef;
enddef;

%	============================ Dots ============================

% Stark dot with sized circle pen, can be followed by withcolor.
def bulldot(expr pos, dotsize) =
	fill fullcircle scaled dotsize shifted pos
enddef;

% Stark dot with sized chosen pen, can be followed by withcolor.
def bulldotpen(expr pos, dotsize, dotpen) =
	draw pos withpen dotpen scaled dotsize
enddef;

%	=========================== Colors ===========================

% Until back again in ConTeXt distribution:
%def namedcolor (expr n) =
%    1
%    withprescript "sp_type=named"
%    withprescript "sp_name=" & n
%enddef ;

% Color application macros for string color values
%def withcolorname text name = withcolor namedcolor(str name) enddef;

% Macros to facilitate uniform color usage.
%	outlinecolor is used for frames of boxes etc.
%	textcolor is used for drawing texts, e.g. with textext
%	insidecolor is used for filling up blocks etc.
%	backgroundcolor is used for unfill and undraw

% administration for blocks.
def colorsuffix = "_c" enddef;
newinternal colorcounter;
newinternal savecolorcounter;
string colornames[];
color outlinecolors[], textcolors[], insidecolors[], backgroundcolors[];
color outlinecolor, textcolor, insidecolor, backgroundcolor;

% Convert between name of block and index into array
% for the mechanism see metafont book definition of mode_def
def colorcount_ suffix $ =
	$ := incr colorcounter;
	colornames[$] := str$;
enddef;

% Install colors in the given location.
def storeColors_ expr loc =
	 outlinecolors[loc] := outlinecolor;
	 textcolors[loc] := textcolor;
	 insidecolors[loc] := insidecolor;
	 backgroundcolors[loc] := backgroundcolor;
enddef;

% Retrieve colors from the given location.
def retrieveColors_ expr loc =
	outlinecolor := outlinecolors[loc];
	textcolor := textcolors[loc];
	insidecolor := insidecolors[loc];
	backgroundcolor := backgroundcolors[loc];
enddef;

% Color values used for general drawing.
% - outlineColor    => outlinecolor = color of outline
% - insideColor     => insidecolor = color of interior
% - textColor       => textcolor = color of text
% - backgroundColor => backgroundcolor = color of background
% - name            => name of the standard block parameter macro as a string

% Use two different values to set the four colors.
% In the order (outline, text) (inside, background).
def setupColors (expr fore, back) =
	outlinecolor := fore;
	textcolor := fore;
	insidecolor := back;
	backgroundcolor := back;
	drawoptions(withcolor fore);
enddef;

% Convenience setting of individual colors.
def setOutlineColor expr thecolor = outlinecolor := thecolor; enddef;
def setFrameColor expr thecolor = outlinecolor := thecolor; enddef;
def setTextColor expr thecolor = textcolor := thecolor;enddef;
def setInsideColor expr thecolor = insidecolor := thecolor; enddef;
def setFillColor expr thecolor = insidecolor := thecolor; enddef;
def setBackgroundColor expr thecolor = backgroundcolor := thecolor; enddef;

% Define current colors by name, name must be string.
def defineColors expr name =
	colorcount_ scantokens(name & colorsuffix);
	storeColors_ colorcounter;
enddef;

% Retrieve colors by name, name must be string.
def setColors expr name =
	retrieveColors_ scantokens(name & colorsuffix);
enddef;

% Save and restore colors -- note that not nestable
def saveColors =
	storeColors_ savecolorcounter;
enddef;
def restoreColors =
	retrieveColors_ savecolorcounter;
enddef;

%	=========================== Arrows ===========================

%	Original arrow source:
%	David Salomon
%	Arrows for Technical Drawings
%	TUGboat, Volume 13 (1992), No.2, p. 146-149

% Construct path of arrowhead, placing the tip at the origin.
vardef arrowPath (expr arrowLength, insetRatio, tipAngle, wingCurve, tailCurve) =
	begingroup
	save zz, insetdir; pair zz[], insetdir;
	save swdir, ewdir, stdir, etdir;
	numeric swdir, ewdir, stdir, etdir;

	% calculate anchor points
	rt zz1 = origin;
	zz2 = (-arrowLength, arrowLength * sind 0.5 tipAngle / cosd 0.5 tipAngle);
	zz3 = (-insetRatio * arrowLength, 0);
	zz4 = (xpart zz2, -ypart zz2);

	% calculate outgoing and incoming wing and tail directions.
	swdir := angle(zz2 - zz1) + wingCurve;
	ewdir := angle(zz1 - zz4) - wingCurve;
	stdir := angle(zz3 - zz2) + tailCurve;
	etdir := angle(zz4 - zz3) - tailCurve;
	insetdir := if tailCurve = 0: (0,0); else: down; fi

	% return path of the arrow contour
	zz1{dir swdir} .. zz2 &
		zz2{dir stdir} .. {insetdir}zz3 &
		zz3{insetdir} .. {dir etdir}zz4 &
		zz4 .. {dir ewdir}cycle
	endgroup
enddef;

% administration for arrows.
newinternal arrowcounter;		% by default initally zero
path arrowcontours[];
boolean arrowisopen[];
numeric arrowlengths[];
string arrownames[];
def arrowsuffix = "_a" enddef;

% Convert between name of arrow and index into array
% for the mechanism see metafont book definition of mode_def
def arrowcount_ suffix $ =
	$ := incr arrowcounter;
	arrownames[$] := str$;
enddef;

% Define an arrowhead.
% Parameters:
% - arrowLength  = length from base to tip (0 takes ahlength)
% - insetRatio   = relative position of inset 1..0
% - tipAngle     = opening angle at tip (0 takes ahangle)
% - wingCurve    = curvature of flanks (+ inwards, - outwards)
% - tailCurve    = curvature of flanks (+ inwards, - outwards)
% - outline      = outlining true/false
% If outline drawn it has outlinecolor and the interior insidecolor.
% If outline not drawn the whole arrow has outlinecolor.
% - name         = name of the arrowhead macro, must be "string"
vardef defineArrow (expr arrowLength, insetRatio, tipAngle, wingCurve,
		tailCurve, outline) expr name =
	begingroup
	% determine parameters for arrowhead
	save len, ang; numeric len, ang;
	len := if arrowLength = 0: ahlength else: arrowLength fi;
	ang := if tipAngle = 0: ahangle else: tipAngle fi;

	% increment counter and define name for indexed access to arrowhead
	% note the necessary scantokens usage here.
	arrowcount_ scantokens(name & arrowsuffix);

	% Keep these data.
	arrowlengths[arrowcounter] := insetRatio * len;
	arrowcontours[arrowcounter] := arrowPath(len, insetRatio, ang, wingCurve, tailCurve);
	arrowisopen[arrowcounter] := outline;
	endgroup
enddef;

% Definition of default arrowhead
% The default arrows and lines are all drawn solid and in the current
% outlinecolor which may be overridden by the modifier.
def defineDefaultArrow (expr length, ratio, angle, wing, tail) =
	defineArrow(length, ratio, angle, wing, tail, false) "_DEFAULT_";
enddef;

% Drawing arrows and doublesided arrows with modifier on line and arrowhead
% NB remember 'draw', 'fill' etc. by itself followed by drawoptions content.
%	arrow = name of the arrow, given as "string".
def drawArrow (expr arrow) expr p =
	addto currentpicture also arrowlinedrawer(p, false, arrow)
enddef;
def drawdblArrow (expr arrow) expr p =
	addto currentpicture also arrowlinedrawer(p, true, arrow)
enddef;

% actual arrowline drawer into picture, modifier works on outlines only
%	line    = path variable containing the line
%	double  = true/false for double/single sided arrowline
%	index   = pointer into the arrows arrays.
%	modif   = modifier applied to the line only.
vardef arrowlinedrawer (expr line, double, name) text modif =
	begingroup
	save index; numeric index;
	index := scantokens(name & arrowsuffix);
	save linepath; path linepath;
	save bpt, bbpt, ept, eept; pair bpt, bbpt, ept, eept;
	save brot, erot; numeric brot, erot;
	save leng; numeric leng;
	leng := arrowlengths[index];

	% Manipulate path of connecting lines.
	linepath := line;

	% Save original begin- and endpoints.
	bpt := point 0 of linepath;
	ept := point length linepath of linepath;

	% Clip endpoint of line against inset of arrowhead, calculate rotation.
	linepath := cutarrowline(linepath,leng);
	eept := point length linepath of linepath;
	erot := if ept = eept: 0; else: angle(ept - eept); fi

	% The same for beginpoint when doublesided arrows.
	if double:
		linepath := reverse cutarrowline(reverse linepath,leng);
		bbpt := point 0 of linepath;
		brot := if bpt = bbpt: 180; else: angle(bpt - bbpt); fi
	fi

	% Initialize the picture of the arrowhead plus lines.
	save arrow, arrowpic;
	picture arrow, arrowpic;
	arrowpic = nullpicture;

	% Arrows either filled or outline.
	addto arrowpic doublepath linepath withpen currentpen
		withcolor outlinecolor modif;
	arrow := nullpicture;
	if arrowisopen[index]:
	 	% Outline arrows has outlinecolor contour and insidecolor fill.
		addto arrow contour arrowcontours[index] withcolor insidecolor;
		addto arrow doublepath arrowcontours[index]
			withpen currentpen withcolor outlinecolor;
	else:
		% Filled arrows are drawn with current outline color.
		addto arrow contour arrowcontours[index] withcolor outlinecolor modif;
	fi;

	% draw arrowhead(s) at endpoint(s) in proper orientation.
	addto arrowpic also arrow rotated erot shifted ept;
	if double:
		addto arrowpic also arrow rotated brot shifted bpt;
	fi;

	% return the completed picture
	arrowpic
	endgroup
enddef;

% Cutoff arrowline at the endpoint at the inset of arrowhead
vardef cutarrowline (expr p, l) =
	p cutafter makepath pencircle
		scaled (2l) shifted (point length p of p)
enddef;

%	=========================== Blocks ===========================

% Retrieve width and height of picture c.q. currentpicture
def picturewidth (expr pic) =
	xpart ulcorner pic - xpart lrcorner pic
enddef;
def pictureheight (expr pic) =
	ypart ulcorner pic - ypart lrcorner pic
enddef;
def picturesize (expr pic) =
	(picturewidth(pic), pictureheight(pic))
enddef;
def currentwidth =
	picturewidth(currentpicture)
enddef;
def currentheight =
	pictureheight(currentpicture)
enddef;
def currentsize =
	picturesize(currentpicture)
enddef;

% Reserve canvas.
def blockframe (expr w, h) =
	setbounds currentpicture to (fullsquare xyscaled (w,h) shifted (w/2,h/2))
enddef;

% Reserve canvas with extended outlying dimensions.
def extendedblockframe (expr w, h, offx, offy) =
	blockframe(w + 2 * offx, h + 2 * offx) shifted (-offx,-offy)
enddef;

% Colored canvas.
def colorframe (expr w, h, clr) =
	fill (0,0)--(w,0)--(w,h)--(0,h)--cycle withcolor clr;
enddef;
def ColorFrame (expr w, h) =
	colorframe(w,h,backgroundcolor);
enddef;

% Colored canvas with extended outlying dimensions.
def extendedcolorframe (expr w, h, offx, offy, clr) =
	fill (-offx,-offy)
		--(w+offx,-offy)
		--(w+offx,h+offy)
		--(-offx,h+offy)
		--cycle withcolor clr;
enddef;
def ExtendedColorFrame (expr w, h, offx, offy) =
	extendedcolorframe (w, h, offx, offy, backgroundcolor);
enddef;

% Colored canvas without an outline as canvas for drawing plus border.
def bordercolorframe (expr w, h, bx, by, clr, bgclr) =
	begingroup save background;
	color background; background := white;
	unfill (-bx,-by)
			--(w+bx,-by)
			--(w+bx,h+by)
			--(-bx,h+by)
			--cycle withcolor clr;
	fill (0,0)--(w,0)--(w,h)--(0,h)--cycle withcolor bgclr
	endgroup
enddef;
def BorderColorFrame (expr w, h, bx, by) =
	bordercolorframe (w, h, bx, by, outlinecolor, backgroundcolor)
enddef;

% Colored canvas without an outline as canvas for drawing plus border
% and extended outlying dimensions.
def extendedbordercolorframe (expr w, h, offx, offy, bx, by, clr, bgclr) =
	begingroup save background;
	color background; background := white;
	unfill (-bx-offx,-by-offy)
			--(w+bx+offx,-by-offy)
			--(w+bx+offx,h+by+offy)
			--(-bx-offx,h+by+offy)
			--cycle withcolor clr;
	fill (-offx,-offy)
		--(w+offx,-offy)
		--(w+offx,h+offy)
		--(-offx,h+offy)
		--cycle withcolor bgclr;
	endgroup
enddef;
def ExtendedBorderColorFrame (expr w, h, offx, offy, bx, by) =
	extendedbordercolorframe (w, h, offx, offy, bx, by, outlinecolor, backgroundcolor)
enddef;

% Builtin possibilities for Block.form are:
%	round (superellipse 0.5 <= <factor>  <= 1.0, default 0.85)
%	oval (ellips)
%	rectangle (rectangle)
%	hexagon
%	diamond (rectangle rotated 45)
%	slant (slanted rectangle <slant> default 0.2)
%	roundrect (rounded left and rightside <roundness> default 0.08)
vardef Block@#(expr position, width, height, labeltext) text modifier =
	VarBlock@#(0, 0, position, width, height, labeltext, true) modifier
enddef;

% Open block, i.e. without an outline.
vardef OBlock@#(expr position, width, height, labeltext) text modifier =
	VarBlock@#(0, 0, position, width, height, labeltext, false) modifier
enddef;

% Block variation.
vardef VarBlock@#(expr param, rotation, position, width, height,
		labeltext, outline) text modifier =
	Form(rotation, position, width, height, labeltext, outline,
		varcblock@#(param, width, height)) modifier;
enddef;

% Return path of various preprogrammed forms with block.variant
%	round (superellipse), oval (ellips), rectangle (rectangle), hexagon
vardef block@#(expr width, height) =
	varblock@#(0, width, height)
enddef;
vardef varblock@#(expr param, width, height) =
	% note: cannot simply define blockl.oval as "shifted (width/2,height/2)",
	% because width and height are not recognized as the formal parameters.
	% this is the reason for using local variables w and h.
	begingroup
	save w_, h_, p_; numeric w_, h_, p_; w_:= width; h_ := height; p_ := param;
	scantokens blockf@# xscaled w_ yscaled h_ scantokens blockl@#
	endgroup
enddef;

% Return path of various preprogrammed centered forms with cblock.variant
%	round (superellipse), oval (ellips), rectangle (rectangle), hexagon
vardef cblock@#(expr width, height) =
	varcblock@#(0, width, height)
enddef;
vardef varcblock@#(expr param, width, height) =
	varblock@#(param, width, height) shifted (-width/2,-height/2)
enddef;

% Form placed at given position.
%	rotation      = applied to form before placement
%	position      = origin where to place the form
%	width, height = dimensions of the form
%	labeltext     = text positioned at center with textext macro
%	outline       = true/false for do/don't draw the outline frame
%	form          = its outline path
%	modifier      = applied to outline, e.g. dashing (pencircle only!), color.
def Form(expr rotation, position, width, height,
		labeltext, outline, form) text modifier =
	begingroup
	% get the outline of the frame
	save formpath; path formpath;
	formpath = form rotated rotation shifted position;

	% ensure that we have the text in a picture
	save labelpic; picture labelpic;
	labelpic =	Lab(labeltext);

	% calculate label offset and vector from center to outline intersection
	save sect; pair sect;
	sect = (position -- (position +
		% must make path long enough to spot crossing
		(width ++ height) * (llcorner labelpic + urcorner labelpic)))
			intersectionpoint formpath;

	% fill inside, draw the label at designated place and draw the outline
	fill formpath withcolor insidecolor;
	
	% surround label text placement with textcolor addition.
	% however, an explicit color in the label text (e.g. "\red ..") will hold.
	extradrawoptions(withcolor textcolor);
	draw labelpic shifted if sect = origin: position; else: sect; fi
	extradrawoptions();
	if outline:
		draw formpath modifier; % drawn with drawoptions then modifier.
	fi
	endgroup
enddef;

% Define path for special block forms.
vardef unittriangle =
	(0,0) -- (1,0) -- (1/2,1) -- cycle
enddef;
vardef unithexagon =
	(1,1/2) -- (3/4,1) -- (1/4,1) -- (0,1/2) -- (1/4,0) -- (3/4,0) -- cycle
enddef;
vardef unitroundrect =
	(p_,0)--(1-p_,0)..(1,1/2)..(1-p_,1)--(p_,1)..(0,1/2)..cycle
enddef;

% Define strings for path constructions.
string blockf, blockf.rectangle, blockf.oval, blockf.round, blockf.hexagon,
	blockf.triangle, blockf.diamond, blockf.slant, blockf.roundrect;
string blockl, blockl.rectangle, blockl.oval, blockl.round, blockl.hexagon,
	blockl.triangle, blockl.diamond, blockl.slant, blockl.roundrect;
% prefix string
	blockf           := "unitsquare";
	blockf.rectangle := "unitsquare";
	blockf.oval      := "fullcircle shifted (0.5,0.5)";
	blockf.round     := "unitsquare";
	blockf.triangle  := "unittriangle";
	blockf.hexagon   := "unithexagon";
	blockf.diamond   := "unitsquare rotated 45 scaled (1/sqrt 2) shifted (0.5,0)";
	blockf.slant     := "if p_ = 0: p_ := 0.2 fi; unitsquare slanted p_ shifted (-p_/2,0)";
	blockf.roundrect := "if p_ = 0: p_ := 0.2 fi; p_ := min(1,max(0,p_*h_/w_))/2; unitroundrect";
% postfix string
	blockl           := "";
	blockl.rectangle := "";
	blockl.oval      := "";
	blockl.round     := "superellipsed if p_ = 0: 0.85 else: min(1.0,max(0.5,p_)) fi";
	blockl.triangle  := "";
	blockl.hexagon   := "";
	blockl.diamond   := "";
	blockl.slant     := "";
	blockl.roundrect := "";

%	=========================== Labels ===========================

% Produce labels, shifted to their intended places, delivered as picture.
% Text at specific point possibly rotated, shifted, scaled, colored.
% In contrast to plain.mf we do not solely use fixed (3bp) labeloffset,
% but add half the width and/or height of the current pen.
% labeltext = Lab.xx(string) [scaled,shifted] or picture
% pos       = point where to place text

% Flag and color for showing the boundingbox of the label.
boolean draw_labelbox; draw_labelbox := false;
def showLabel (expr switch) = draw_labelbox := switch; enddef;

% Label(string/textext(string), center position)
vardef Label@#(expr labeltext, pos) text modifier =
	% surround label text placement with textcolor addition.
	% however, an explicit color in the label text (e.g. "\red ..") will hold.
	extradrawoptions(withcolor textcolor);
	draw Lab@#(labeltext) shifted pos modifier;
	extradrawoptions();
enddef;

% Label with text
vardef Lab@#(expr labeltext) =
	begingroup
	save labelpicture; picture labelpicture;
	save labelpictureshift; pair labelpictureshift; labelpictureshift := origin;

	if picture labeltext:
		labelpicture := labeltext;
	else:
		labelpicture := nullpicture;
		% other pens then pencircle draw nonsense
		getpen(pencircle);
		% prevented wobbling of text boxes with uneven depth.
		% but proves bad idea because math formulas and other text
		% may extend below the baseline and then is be clipped.
		% therefore, do this operation beforehand on labeltext.
		% pic := textext("\setbox0=\hbox{"&labeltext&"}\dp0=0pt\box0");
		labelpicture := textext(labeltext);
		restorepen;
	fi
	
	% Make label and dimensions directly accessible.
	labelWidth :=  xpart urcorner labelpicture - xpart llcorner labelpicture;
	labelHeight := ypart urcorner labelpicture - ypart llcorner labelpicture;

	% calculate labelshift from suffix
	labelpictureshift := ((penX/2 + labeloffset) * xpart laboff@#,
		(penY/2 + labeloffset) * ypart laboff@#)
		- (labxf@# * lrcorner labelpicture + labyf@# * ulcorner labelpicture
		+ (1 - labxf@# - labyf@#) * llcorner labelpicture);

	% for debugging surround label with frame.
	if draw_labelbox :
		addto labelpicture doublepath boundingbox labelpicture
			withpen pensquare scaled 1pt;
	fi;

	% deliver picture at proper place according to variation.
	labelpicture shifted labelpictureshift
	endgroup
enddef;

%	=========================== Initializations ===========================

% Preprogrammed default colors and their standard color representation
outlinecolor := black;
textcolor := black;
insidecolor := white;
backgroundcolor := white;
defineColors "BLACK_WHITE";
savecolorcounter := colorcounter;
background := white;
extradrawoptions();

% Preprogrammed default arrows
clearpen;
ahlength := 3mm;
ahangle := 40;
defineDefaultArrow(ahlength, 0.4, ahangle, 0, 0);

% Picture, width and height of boundingbox last label made are here available.
numeric labelWidth, labelHeight; labelWidth := 0; labelHeight := 0;
% Offset for labels
numeric labeloffset; labeloffset := 4pt;

% alternative names for arrows
def arrowline    = drawArrow("_DEFAULT_") enddef;
def dblarrowline = drawdblArrow("_DEFAULT_") enddef;

% redefine drawarrow and drawdblarrow to use hvdm.mp defaults
def hvdmarrows =
	def drawarrow =  arrowline enddef;
	def drawdblarrow =  dblarrowline enddef;
enddef;
def plainarrows =
	def drawarrow expr p = _apth:=p; _finarr enddef;
	def drawdblarrow expr p = _apth:=p; _findarr enddef;
enddef;
hvdmarrows;

% Note that beginfig clears the drawoptions variable _opt_.

endinput
