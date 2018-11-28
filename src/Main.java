import org.jfree.ui.RefineryUtilities;

public class Main {

    public static void main(String[] args) {



        final PolarLineChartExample demo = new PolarLineChartExample("Dynamic Line And TimeSeries Chart");
        demo.pack();
        RefineryUtilities.centerFrameOnScreen(demo);
        demo.setVisible(true);


        //String host = "10.105.0.52";
        String host = "192.168.43.47";
        //String host = "localhost";
        int port = 2345;

        /*TimeServer ts = new TimeServer(host, port);
        ts.open();*/


        //new ClientConnexion(host, port);
        Thread t = new Thread(new ClientConnexion(host, port, demo));
        t.start();


    }
}