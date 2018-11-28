
import java.io.BufferedInputStream;
import java.io.IOException;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;


public class ClientConnexion implements Runnable{

    private Socket connexion = null;
    private PrintWriter writer = null;
    private BufferedInputStream reader = null;
    private PolarLineChartExample demo = null;

    private static int count = 0;
    private String name = "Client-";

    public ClientConnexion(String host, int port, PolarLineChartExample demo){
        name += ++count;
        this.demo = demo;
        try {
            System.out.println("Tentative de connexion au serveur "+host+" sur le port "+port);
            connexion = new Socket(host, port);
            System.out.println("Connexion établie.");
        } catch (UnknownHostException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }


    public void run(){
        try {
            Thread.currentThread().sleep(1000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        while (true){

            try {
                writer = new PrintWriter(connexion.getOutputStream(), true);
                reader = new BufferedInputStream(connexion.getInputStream());
                //On envoie la commande au serveur

            /*String commande = "Salut";
            writer.write(commande);
            //TOUJOURS UTILISER flush() POUR ENVOYER RÉELLEMENT DES INFOS AU SERVEUR
            writer.flush();*/

                // System.out.println("Commande " + commande + " envoyée au serveur");

                //On attend la réponse
                String response = read();

                System.out.println("\t * " + name + " : Réponse reçue " + response);
                String[] splited1 = response.split("&");
                //System.out.println(splited1[0] +" 1 "+splited1[1]);
                System.out.println("donnée ajouté");
                for (int i = 1; i<splited1.length;i++){
                    String[] splited = splited1[i].split(" ");
                    int tailleSplit = splited.length;
                    double newTheta = Double.valueOf(splited[tailleSplit-5]);

                    Data d = new Data(newTheta,Double.valueOf(splited[tailleSplit-3]),Integer.valueOf(splited[tailleSplit-1]));
                    demo.addOneData(d);
                    System.out.println("donnée ajouté");
                }


            } catch (IOException e1) {
                e1.printStackTrace();
            }

            try {
                Thread.currentThread().sleep(1000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            writer.write("CLOSE");
            writer.flush();
            //writer.close();
        }



    }


    //Méthode pour lire les réponses du serveur
    private String read() throws IOException{
        String response = "";
        int stream;
        byte[] b = new byte[4096];
        stream = reader.read(b);
        response = new String(b, 0, stream);
        return response;
    }
}