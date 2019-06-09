import java.lang.*;
import java.io.*;
import java.awt.*;
import javax.swing.*;
import java.awt.event.*;
import java.net.*;

public class Display_copyDrJava {
  
  public static void main (String [] agrs) throws Exception {
    String fromClient;
    String toClient;
    
    ServerSocket server = new ServerSocket(8080);
    System.out.println("wait for connection on port 8080");
    
    boolean run = true;
    while(run) {
      Socket client = server.accept();
      System.out.println("got connection on port 8080");
      BufferedReader in = new BufferedReader(new InputStreamReader(client.getInputStream()));
      PrintWriter out = new PrintWriter(client.getOutputStream(),true);
      
      fromClient = in.readLine();
      System.out.println("received: " + fromClient);
      
      if(fromClient.equals("Hello")) {
        toClient = "olleH";
        System.out.println("send olleH");
        out.println(toClient);
        fromClient = in.readLine();
        System.out.println("received: " + fromClient);
        
        if(fromClient.equals("Bye")) {
          toClient = "eyB";
          System.out.println("send eyB");
          out.println(toClient);
          client.close();
          run = false;
          System.out.println("socket closed");
        }
      }
    }
    System.exit(0);
    
    
    Frame frame = new Frame();
    
    Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize();
    
    double screenHeight = screenSize.getHeight();
    int h = (int) screenHeight;
    double screenWidth = screenSize.getWidth();
    int w = (int) screenWidth;
    int b = w/3;
    
    int divide = b/2;
    System.out.println("divide = "+divide);
    int half = (int) (Math.ceil(divide/100))*100;
    
    frame.setSize(w, h);
    System.out.println("("+w+", "+h+")");
    
    JPanel redPanel = new JPanel();
    redPanel.setSize(b, h);
    redPanel.setLocation(0, 0);
    frame.add(redPanel);
    redPanel.setBackground(Color.RED);
    redPanel.setLayout(null);
    
    JPanel cameraPanel = new JPanel();
    cameraPanel.setSize(b, h);
    cameraPanel.setLocation(b, 0);
    frame.add(cameraPanel);
    cameraPanel.setBackground(Color.WHITE);
    cameraPanel.setLayout(null);
    
    JPanel bluePanel = new JPanel();
    int c = b*2;
    bluePanel.setSize(b, h);
    bluePanel.setLocation(c, 0);
    System.out.println("c = "+c);
    frame.add(bluePanel);
    bluePanel.setBackground(Color.BLUE);
    bluePanel.setLayout(null);
    
    int d=(int) (Math.floor(0/100))+100;
    System.out.println("d = "+d);
    int e=(int) (Math.ceil(c/100))*100;
    int he = d/2;
    int f = d+he;
    System.out.println("int g  = ( ("+c+") + ("+divide+") ) - "+f);
    int g= (c+divide)-f;
    System.out.println("f = "+f);
    
    JLabel redheadlabel = new JLabel("Red Team");
    redheadlabel.setFont(new Font("Verdana", Font.PLAIN, 45));
    //redheadlabel.setBackground(Color.BLACK);
    redheadlabel.setForeground(Color.WHITE);
    redheadlabel.setBounds(f,0,300,300);
    redPanel.add(redheadlabel);
    
    JLabel cameraheadlabel = new JLabel("Player Record");
    cameraheadlabel.setFont(new Font("Verdana", Font.PLAIN, 45));
    cameraheadlabel.setForeground(Color.BLACK);
    cameraheadlabel.setBounds(f,0, 600, 300);
    cameraPanel.add(cameraheadlabel);
    
    JLabel blueheadlabel = new JLabel("Blue Team");
    blueheadlabel.setFont(new Font("Verdana", Font.PLAIN, 45));
    blueheadlabel.setForeground(Color.WHITE);
    blueheadlabel.setBounds(g, 0,1300,225);
    bluePanel.add(blueheadlabel);
    
    frame.setVisible(true);
    
    
  }
  
}

