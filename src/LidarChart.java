import javax.swing.*;

import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartPanel;
import org.jfree.chart.JFreeChart;
import org.jfree.data.time.Millisecond;
import org.jfree.data.xy.XYSeries;
import org.jfree.data.xy.XYSeriesCollection;
import org.jfree.ui.ApplicationFrame;
import org.jfree.ui.RefineryUtilities;

import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.*;
import java.util.ArrayList;

public class PolarLineChartExample extends ApplicationFrame implements ActionListener {

    private static final long serialVersionUID = 1L;
    private static int compteur = 0;
    private static XYSeries series;

    /** The most recent value added. */
    private double lastTheta = 0;
    private double lastDistance = 0;

    /** Timer to refresh graph after every 1/2 second */
    private Timer timer = new Timer(500, this);



    public PolarLineChartExample() {
        //Name of the frame
        super("LIDAR representation");

        //Creation of the collection of series
        XYSeriesCollection dataSet = new XYSeriesCollection();

        //Creation of the dataset about distance
        series = new XYSeries("Distance");
        dataSet.addSeries(series);

        // Based on the dataset we are creating PolarChart
        JFreeChart polarChart = ChartFactory.createPolarChart("LIDAR", dataSet, true, true, false);

        //Created JPanel to show graph on screen
        final JPanel content = new JPanel(new BorderLayout());
        //Created Chartpanel for chart area
        final ChartPanel chartPanel = new ChartPanel(polarChart);
        //Added chartpanel to main panel
        content.add(chartPanel);
        //Sets the size of whole window (JPanel)
        chartPanel.setPreferredSize(new java.awt.Dimension(800, 500));
        //Puts the whole content on a Frame
        setContentPane(content);

        //timer.start();


    }

    public XYSeries getXYSeries(){
        return this.series;
    }

    private static ArrayList<Data> parsingData(){
        ArrayList<Data> data = new ArrayList<>();
        double oldTheta = 0;
        double newTheta = 0;
        try {
            File f = new File ("./test2.txt");
            FileReader fr = new FileReader(f);
            BufferedReader br = new BufferedReader (fr);
            try
            {
                String line = br.readLine();
                for(int i = 0; i < compteur && line != null; i++){
                    line = br.readLine();
                }
                while (line != null)
                {
                    String[] splited = line.split(" ");
                    int tailleSplit = splited.length;
                    newTheta = Double.valueOf(splited[tailleSplit-5]);
                    if(newTheta < oldTheta){
                        break;
                    }
                    else{
                        oldTheta = newTheta;
                    }
                    Data d = new Data(newTheta,Double.valueOf(splited[tailleSplit-3]),Integer.valueOf(splited[tailleSplit-1]));
                    data.add(d);
                    line = br.readLine();
                }

                br.close();
                fr.close();
            }
            catch (IOException exception)
            {
                System.out.println ("Erreur lors de la lecture : " + exception.getMessage());
            }
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }
        compteur += data.size();

        System.out.println("Nb data  "+data.size());
        System.out.println("Compteur "+compteur);
        System.out.println("OldTheta "+oldTheta+" New theta "+ newTheta);
        return data;

    }

    private void addData(ArrayList <Data> data) {

        int j =  this.series.getItemCount();
        //System.out.println(/*"Item count = " + j+" et dans */"data "+data.size());
        if( this.series.getItemCount() > 0)
            this.series.clear();
        int i = 0;
        while(data.get(i).getTheta() < 359){
            if(data.get(i).getDistance() != 0)
                this.series.add(data.get(i).getTheta(), data.get(i).getDistance());
            i++;
        }
    }

    public void addOneData(Data data) {

        this.series.add(data.getTheta(), data.getDistance());

    }

    /**
     * Generates an random entry for a particular call made by time for every 1/4th of a second.
     *
     * @param e  the action event.
     */
    public void actionPerformed(final ActionEvent e) {
        //ArrayList <Data> data = parsingData();
        //addData(data);

        /*final double factor = 0.9 + 0.2*Math.random();
        this.lastTheta = this.lastTheta * factor;
        this.lastDistance = this.lastDistance +1;*/

        final Millisecond now = new Millisecond();
       // this.series.add(lastTheta, this.lastDistance);

        System.out.println("Milliseconds = " + now.toString());
    }


   /* public static void main(String[] args) {
        PolarLineChartExample chart = new PolarLineChartExample("Polar Chart Example");
        chart.pack();
        chart.setVisible(true);
    }*/
    /**
     * Starting point for the dynamic graph application.
     *
     * @param args  ignored.
     */
    public static void main(final String[] args) {

        final PolarLineChartExample demo = new PolarLineChartExample();
        demo.pack();
        RefineryUtilities.centerFrameOnScreen(demo);
        demo.setVisible(true);

    }
}