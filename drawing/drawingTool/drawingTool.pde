import java.io.*; 
import java.net.*;

public class ColourContainer {
  public int h = 0;
  public int s = 0;
  public int v = 0;
  
  public ColourContainer (int h, int s, int v){
    this.h = h;
    this.v = v;
    this.s = s;
  }
}

/*
color[] pallette = {
  color(0, 0, 0), 
  color(255, 0, 0), 
  color(0, 255, 0), 
  color(0, 0, 255), 
  color(255, 255, 0), 
  color(255, 255, 255), 
  color(255, 0, 255), 
  color(0, 255, 255)
};*/
int[] pal;

ColourContainer[] palette;



int w = 14;
int h = 12;
int[][] pixels;
int curColour = 0;

PFont f;


DatagramSocket socket ;
InetAddress IPAddress;
;

void setup() {
  palette = new ColourContainer[8];
  pal = new int[8];
  for (int i = 0; i < 8; i++){
    pal[i] = 27 * i;
    palette[i] = new ColourContainer(27*i, 255,255);
  }
  palette[0].v = 0;
  palette[7].s = 0;
  
  
  size(800, 500);
  f = loadFont("Aharoni-Bold-48.vlw");
  try {
    socket = new DatagramSocket();
    IPAddress = InetAddress.getByName("127.0.0.1");
  } 
  catch (Exception e) {
    e.printStackTrace();
  }
  pixels = new int[w][h];
  for (int x = 0; x < w; x++) {
    for (int y = 0; y < h; y++) {

      pixels [x][y] = 0;
    }
  }
}

void clear(){
  for (int x = 0; x < w; x++) {
    for (int y = 0; y < h; y++) {

      pixels [x][y] = 0;
    }
  }
}

void send() {
  byte[] sendData = new byte[w*h];

  for (int x = 0; x < w; x++) {
    for (int y = 0; y < h; y++) {

      sendData[x + y * w] = (byte)pixels[x][y];
    }
  }
  try {
    DatagramPacket sendPacket = new DatagramPacket(sendData, sendData.length, IPAddress, 9001);
    socket.send(sendPacket);
    println("sent + " + sendData.length);
  } 
  catch (Exception e) {
    e.printStackTrace();
  }
}

void mouseDragged(){
  drawOnCanvas();
}

void drawOnCanvas(){
   int colour = 0;
  println(mouseButton);
  if(mouseButton == 37){
    colour = curColour;
  } else {
    colour = 0;
  }
  int mx = mouseX - 100;
  int my = mouseY - 100;

  for (int x = 0; x < w; x++) {
    for (int y = 0; y < h; y++) {
      if (mx > x*30 && mx < x*30 + 30) {
        if (my > y*30 && my < y*30 + 30) {
          println("clicked");
          pixels[x][y] = colour;
        }
      }
    }
  }
}

void mouseClicked() {
  
  if( mouseY < 70){
    if(mouseX < 150){
      send();
      return;
    } else if (mouseX > 170 && mouseX < 330){
      clear();
      return;
    }
  }
 drawOnCanvas();
}


void draw() {
  stroke(255);
  colorMode(HSB,255,255,255);
  for (int x = 0; x < w; x++) {
    for (int y = 0; y < h; y++) {
      int sat = 255;
      if(pixels[x][y] == 0){
        sat = 0;
      }
      ColourContainer c = palette[pixels[x][y]];
      fill(c.h, c.s, c.v);
      rect(100 +  x * 30, 100 + y * 30, 30, 30);
    }
  }
 
  
  ColourContainer c = palette[curColour];
  fill(c.h, c.s, c.v);
    
  
  rect(10,200,40,40);
  colorMode(RGB,255,255,255);
  fill(0);
  rect(0, 0, 150, 70);
  rect(180, 0, 150, 70);
  
  fill(255);
  textFont(f, 12);
  text("send", 10,40);
  text("clear", 210, 40);
  
  
  text("load = l", 360, 30);
  text("save = s", 360, 50);
  text("0-7 = change pen colour", 360, 70);
  
}

void keyPressed(){
  if(key == 'l'){
    selectInput("load", "fileSelected");
  } else if (key == 's'){
    selectInput("save", "saveSelected");
  } else if(key >= '0' && key <= '7'){
    curColour = key - 48;
    println("col " + curColour);
  }
}

void saveSelected(File f){
  String path = f.getAbsolutePath();
  String out = "";
  for (int x = 0; x < w; x++) {
    for (int y = 0; y < h; y++) {
      out += pixels[x][y];
    }
  }
  saveStrings(path, new String[]{out});

}


void fileSelected(File f){
  
  println(f.getAbsolutePath());
  String[] data = loadStrings(f.getAbsolutePath());
  
  println(data);
  String d = data[0];
  int ct = 0;
  for (int x = 0; x < w; x++) {
    for (int y = 0; y < h; y++) {
      pixels[x][y] = Integer.parseInt(""+d.charAt(ct));   
      ct ++;
    }
  }
  
  
}

