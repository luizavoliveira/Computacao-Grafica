
float a = 0;

void setup() {
  size(800,600);
}

void draw() {
    background(255);
    translate(mouseX, mouseY);
    printMatrix();
    rotate(a);   
    printMatrix();
    circle(30,30,10);
    a += 0.1;
}
