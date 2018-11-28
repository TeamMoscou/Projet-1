import java.io.IOException;
import java.net.InetAddress;
import java.net.ServerSocket;

public class TestSocket {

    public static void main(String[] args) {

        try {
                String IP = "127.0.0.1";
                int port = 2222;
                int fileAttente = 5;
                ServerSocket sSocket = new ServerSocket(port, fileAttente, InetAddress.getByName(IP));
            } catch (IOException e) {
                System.err.println("Le port " + 2222 + " est déjà utilisé ! ");
            }
        }
}