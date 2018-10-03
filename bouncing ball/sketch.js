
var bg,ball,vector,low,high,flag,supposed,mouse,count=0,frames,swi;

function inside(given){
	if ((given.x<high.x && given.x>low.x) && (given.y<high.y && given.y>low.y)){
		return 1;
	}
	else if((given.x<low.x && given.y<low.y)||(given.x<low.x && given.y>high.y)||(given.x>high.x && given.y<low.y)||(given.x>high.x && given.y>high.y)){
			vector.x*=-1;
			vector.y*=-1;
	}
	else if((given.x<low.x)||(given.x>high.x)){
			vector.x*=-1;
	}
	else if((given.y<low.y)||(given.y>high.y)){
		vector.y*=-1;
	}
	return 0;
}
function setup() {
	createCanvas(windowWidth, windowHeight);

	frames = 0;
	flag=1;
	swi=1;
	//background colors

	bg = {
		r:100,
		g:100,
		b:255,
		a:20
	};

	//ball specifications

	ball = {
		r:10,
		g:10,
		b:200,
		x:0,
		y:0,
		diameter:0,
		radius:30
	};
	ball.x = random(ball.radius,windowWidth-ball.radius);
	ball.y = random(ball.radius,windowHeight-ball.radius);
	ball.diameter = 2*ball.radius;
	//direction of the ball

	vector = {
		x:random(-1,1)*20,
		y:random(-1,1)*20
	};

	//defining boundaries of x and y

	low = {
		x:ball.radius,
		y:ball.radius
	};

	high = {
		x:windowWidth - ball.radius,
		y:windowHeight - ball.radius
	};

	supposed = {
		x:ball.x,
		y:ball.y
	};

	mouse = {
		x:mouseX,
		y:mouseY
	}
	
}

function draw() {
	
	//setting background
	background(bg.r,bg.g,bg.b,bg.a);

	//setting stroke to false and changing color of the pen
	noStroke();
	fill(ball.r,ball.g,ball.b);

	//drawing the ball
	ellipse(ball.x,ball.y,ball.diameter,ball.diameter); 
	
	//updating ball coordinates
	supposed.x=ball.x + vector.x;
	supposed.y=ball.y + vector.y;

	if(inside(supposed)==1){
		count=0;
		ball.x = supposed.x;
		ball.y = supposed.y;
	}
	else{
		count+=1;
	}
	if (count>1){
		console.log("Ball out of bounds");
		setup();
	}
	frames+=1;
	if(frames%200==0){
		frames=1;
		ball.r+=swi*Math.floor(random(0,50));
		ball.g+=swi*Math.floor(random(0,50));
		ball.b+=swi*Math.floor(random(0,50));
		bg.r = Math.floor(ball.g * 0.5);
		bg.g = Math.floor(ball.b * 0.5);
		bg.b = Math.floor(ball.r * 0.5);

		if(ball.r>120 && ball.g>120 && ball.b>120){
			swi = -1;
		}
		if(ball.r<50 && ball.g<50 && ball.b<50){
			swi=1;
		}
	}
}

function mousePressed(){
	setup();
	if(inside(mouse)==1){
		ball.x = mouseX;
		ball.y = mouseY;
	}
}