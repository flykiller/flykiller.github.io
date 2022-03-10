vardef square(expr c,R) = 
  save r;
  numeric r;
  r=abs(R);
  expandafter (c+(r/2,r/2)--c+(r/2,-r/2)--c+(-r/2,-r/2)--c+(-r/2,r/2)--cycle)
enddef;

vardef square_top(expr c,R) = 
  save r;
  numeric r;
  r=abs(R);
  expandafter (c+(r/2,r/2)--c+(r/2,-r/2)--c+(-r/2,-r/2)--c+(-r/2,r/2))
enddef;

vardef square_bot(expr c,R) = 
  save r;
  numeric r;
  r=abs(R);
  expandafter (c+(-r/2,-r/2)--c+(-r/2,r/2)--c+(r/2,r/2)--c+(r/2,-r/2))
enddef;

vardef square_right(expr c,R) = 
  save r;
  numeric r;
  r=abs(R);
  expandafter (c+(r/2,-r/2)--c+(-r/2,-r/2)--c+(-r/2,r/2)--c+(r/2,r/2))
enddef;

vardef square_left(expr c,R) = 
  save r;
  numeric r;
  r=abs(R);
  expandafter (c+(-r/2,r/2)--c+(r/2,r/2)--c+(r/2,-r/2)--c+(-r/2,-r/2))
enddef;

vardef square_rect(expr c,R,a,b,d,e,f) = 
  save r;
  numeric r;
  r=abs(R);
  for i=a upto b-1:
  	for j = d upto e-1:
  		draw square(c+(i*r,j*r), r) withpen pencircle scaled f;
  	endfor;
  endfor;
enddef;

vardef car(expr s,u) = 
save p,q;
path p,q;
p = circle((0,0),0.2u);
q = circle((u,0),0.2u);
draw p shifted s;
draw q shifted s;
draw ((point 0 of p)--(point 2 of q)) shifted s;
draw ((point 2 of p)--(-0.35u,0)..(-0.5u,0.2u)..(-0.35u,0.45u)--(0,0.45u)) shifted s;
draw ((point 0 of q)--(1.45u,0)..(1.6u,0.2u)..(1.45u,0.45u)--(u,0.45u)) shifted s;
draw ((0,0.45u){right}..(0.2u,0.65u)..(0.3u,0.8u)..(0.45u,0.8u)..(0.8u,0.8u)..(u,0.45u){right}) shifted s;
enddef; 
