input macros;
input macros2;
input hvdm;
input latexmp;

setupLaTeXMP(packages="amssymb", fontencoding="T2A", language="russian");

verbatimtex
\documentclass{article}
\usepackage[utf8]{inputenc}
%\usepackage[koi8-u]{inputenc}
\usepackage[english,russian]{babel}
\usepackage{amsmath}
\usepackage{graphicx}
%\usepackage{unicode-math}
\begin{document}

etex
filenametemplate "%j.eps";
prologues:=3;

beginfig(1)
path p[];
r := 5cm;

r1 = 0.2360679775 * r;
al = 0.38196601125;

z.x0 = origin;
p0 = circle(z.x0, r);
z.a0 = point 1 of p0;
z.a1 = point 1.8 of p0;
z.a2 = point 2.6 of p0;
z.a3 = point 3.4 of p0;
z.a4 = point 0.2 of p0;

z.b0 = point al of (z.a0--z.a1);
z.b1 = point (1 - al) of (z.a0--z.a1);
z.b2 = point al of (z.a1--z.a2);
z.b3 = point (1 - al) of (z.a1--z.a2);
z.b4 = point al of (z.a2--z.a3);
z.b5 = point (1 - al) of (z.a2--z.a3);
z.b6 = point al of (z.a3--z.a4);
z.b7 = point (1 - al) of (z.a3--z.a4);
z.b8 = point al of (z.a4--z.a0);
z.b9 = point (1 - al) of (z.a4--z.a0);

p1 = circle(z.b0, r1);
p2 = circle(z.b1, r1);

z.c3 = cross(p1, p2);
Dot z.c3;

p3 = circle(z.x0, z.x0-z.c3);

z.c0 = point -1 of p3;
z.c1 = point -0.2 of p3;
z.c2 = point 0.6 of p3;
z.c4 = point -1.8 of p3;

z.d0 = crosspoint(z.c2, z.c4)(z.c1, z.c3);
z.d1 = crosspoint(z.c2, z.c4)(z.c0, z.c3);
z.d2 = crosspoint(z.c1, z.c4)(z.c0, z.c3);
z.d3 = crosspoint(z.c1, z.c4)(z.c0, z.c2);
z.d4 = crosspoint(z.c1, z.c3)(z.c0, z.c2);

z.e0 = z.b0 + z.d0 - z.c3;
z.e1 = z.b1 + z.d1 - z.c3;
z.e2 = z.b3 + z.d2 - z.c4;
z.e3 = z.b5 + z.d3 - z.c0;
z.e4 = z.d4 + z.b8 - z.c2;

%Dot z.e0, z.e1, z.e2, z.e3, z.e4;

z.f0 = (1/al)*z.b0 - (1/al - 1)* z.c3;
z.f1 = (1/al)*z.b1 - (1/al - 1)* z.c3;
z.f2 = (1/al)*z.b2 - (1/al - 1)* z.c4;
z.f3 = (1/al)*z.b3 - (1/al - 1)* z.c4;
z.f4 = (1/al)*z.b4 - (1/al - 1)* z.c0;
z.f5 = (1/al)*z.b5 - (1/al - 1)* z.c0;
z.f6 = (1/al)*z.b6 - (1/al - 1)* z.c1;
z.f7 = (1/al)*z.b7 - (1/al - 1)* z.c1;
z.f8 = (1/al)*z.b8 - (1/al - 1)* z.c2;
z.f9 = (1/al)*z.b9 - (1/al - 1)* z.c2;

%Dot z.f0, z.f1, z.f2, z.f3, z.f4, z.f5, z.f6, z.f7, z.f8, z.f9;

%Dot z.d0, z.d1, z.d2, z.d3, z.d4;
%Dot z.c0, z.c1, z.c2, z.c3, z.c4;


%Dot z.b0, z.b1;
%draw z.a0--z.a1--z.a2--z.a3--z.a4--z.a0;

p4 = z.a0--z.a1--z.f0--z.c3--z.f1--cycle;
p5 = z.a1--z.a2--z.f2--z.c4--z.f3--cycle;
p6 = z.a2--z.a3--z.f4--z.c0--z.f5--cycle;
p7 = z.a3--z.a4--z.f6--z.c1--z.f7--cycle;
p8 = z.a4--z.a0--z.f8--z.c2--z.f9--cycle;
p9 = z.c0--z.c2--z.c4--z.c1--z.c3--cycle;



z.g3 = crosspoint(z.a1, z.f0)(z.a0, z.f1);
z.g2 = crosspoint(z.a0, z.f8)(z.a4, z.f9);
z.g1 = crosspoint(z.a3, z.f7)(z.a4, z.f6);
z.g0 = crosspoint(z.a2, z.f5)(z.a3, z.f4);
z.g4 = crosspoint(z.a2, z.f2)(z.a1, z.f3);
%Dot z.g3, z.g1, z.g2, z.g4, z.g0;

p10 = z.g3--z.f0--z.a0--z.f9--z.g2--z.f8--z.a4--z.f7--z.g1--z.f6--z.a3--z.f5--z.g0--z.f4--z.a2--z.f3--z.g4--z.f2--z.a1--z.f1--cycle;

fill p10 withcolor green+red;
fill p4 withcolor red;
fill p5 withcolor red;
fill p6 withcolor red;
fill p7 withcolor red;
fill p8 withcolor red;
fill p9 withcolor red;


draw p10 penhair;

draw z.d0--z.e0--z.b0 penhair;
draw z.e0--z.b9 penhair;
draw z.d4--z.e4--z.b8 penhair;
draw z.e4--z.b7 penhair;
draw z.d3--z.e3--z.b5 penhair;
draw z.e3--z.b6 penhair;
draw z.d2--z.e2--z.b3 penhair;
draw z.e2--z.b4 penhair;
draw z.d1--z.e1--z.b1 penhair;
draw z.e1--z.b2 penhair;

draw p4 penextrabold;
draw p5 penextrabold;
draw p6 penextrabold;
draw p7 penextrabold;
draw p8 penextrabold;
draw p9 penextrabold;

endfig;

end 