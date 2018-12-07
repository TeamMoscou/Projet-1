using System;

using UIKit;

using System.Net.Sockets;
using System.Text;

namespace BrakeOrDie
{
    public partial class ViewController : UIViewController
    {
        TcpClient clientSocket = new TcpClient();
        NetworkStream nwStream;
        bool bconnected = false;

        protected ViewController(IntPtr handle) : base(handle)
        {
            // Note: this .ctor should not contain any initialization logic.
        }

        partial void StartButtonPushed(UIButton sender)
        {

            try
            {
                //Connect the socket to the server
                clientSocket.Connect(getIPAddress.Text, 6666);
                bconnected = true;
                connectLabel.Text = "Connected";
                nwStream = clientSocket.GetStream();
                Receive();
                //Send initial speed value
                //byte[] bytes = Encoding.ASCII.GetBytes("SPE" + getSpeed.Text);
                //nwStream.Write(bytes, 0, bytes.Length);

            }
            catch (SocketException ex)
            {
                connectLabel.Text = "Failed to connect";
                Console.WriteLine(ex.Message);
            }
        }


       /* partial void SetSpeedToCar(UIButton sender)
        {
            int speed = Int32.Parse(getSpeed.Text);
            if (bconnected)
            {
                if (speed < 0){
                    byte[] bytes = Encoding.ASCII.GetBytes("SPE" + "0");
                    nwStream.Write(bytes, 0, bytes.Length);
                } else if (speed > 20){
                    byte[] bytes = Encoding.ASCII.GetBytes("SPE" + "20");
                    nwStream.Write(bytes, 0, bytes.Length);
                } else {
                    byte[] bytes = Encoding.ASCII.GetBytes("SPE" + getSpeed.Text);
                    nwStream.Write(bytes, 0, bytes.Length);
                }
            }

        }*/

        partial void StopWheelButtonPushed(UIButton sender)
        {
            modeLabel.Text = "NominalMode";
            if (bconnected){
                byte[] bytes = Encoding.ASCII.GetBytes("MOV" + "stop");
                nwStream.Write(bytes, 0, bytes.Length);
            }

        }

        partial void RightButtonPushed(UIButton sender)
        {
            modeLabel.Text = "NominalMode";
            if (bconnected)
             {
                 byte[] bytes = Encoding.ASCII.GetBytes("STE" + "right");
                 nwStream.Write(bytes, 0, bytes.Length);
             }
        }

        partial void LeftButtonPushed(UIButton sender)
        {
            modeLabel.Text = "NominalMode";
            if (bconnected)
            {
                byte[] bytes = Encoding.ASCII.GetBytes("STE" + "left");
                nwStream.Write(bytes, 0, bytes.Length);
            }
        }

        partial void UpButtonPushed(UIButton sender)
        {
            modeLabel.Text = "NominalMode";
            if (bconnected)
            {
                byte[] bytes = Encoding.ASCII.GetBytes("MOV" + "forward");
                nwStream.Write(bytes, 0, bytes.Length);
            }
        }

        partial void DownButtonPushed(UIButton sender)
        {
            modeLabel.Text = "NominalMode";
            if (bconnected){
                byte[] bytes = Encoding.ASCII.GetBytes("MOV" + "backward");
                nwStream.Write(bytes, 0, bytes.Length);
            }
        }

        partial void AutonomousButtonClicked(UIButton sender)
        {
            modeLabel.Text = "Autonomous mode";
            if (bconnected)
            {
                byte[] bytes = Encoding.ASCII.GetBytes("AUT");
                nwStream.Write(bytes, 0, bytes.Length);
            }
        }


        async void Receive()
        {
            int cmpt = 0;
            while (clientSocket.Connected)
            {
                byte[] myReadBuffer = new byte[2048];
                await nwStream.ReadAsync(myReadBuffer, 0, myReadBuffer.Length);
                String st = Encoding.UTF8.GetString(myReadBuffer);
                String[] msgs = st.Split(';');

                foreach (String msg in msgs)
                {
                    Console.WriteLine(msg);
                    String[] elt = msg.Split(':');
                    switch (elt[0])
                    {
                        case "OIF":
                            modeLabel.Text = "Obstacle in front";
                            break;
                        case "OIB":
                            modeLabel.Text = "Obstacle in back";
                            break;
                        default:
                            cmpt = (cmpt + 1) % 100;
                            break;
                    }

                }

            }
        }

        partial void BackwardRight(UIButton sender)
        {
            modeLabel.Text = "NominalMode";
            if (bconnected)
            {
                byte[] bytes = Encoding.ASCII.GetBytes("MOV" + "backwardright");
                nwStream.Write(bytes, 0, bytes.Length);
            }
        }

        partial void BackwardLeft(UIButton sender)
        {
            modeLabel.Text = "NominalMode";
            if (bconnected)
            {
                byte[] bytes = Encoding.ASCII.GetBytes("MOV" + "backwardleft");
                nwStream.Write(bytes, 0, bytes.Length);
            }
        }

        partial void ForwardLeft(UIButton sender)
        {
            modeLabel.Text = "NominalMode";
            if (bconnected)
            {
                byte[] bytes = Encoding.ASCII.GetBytes("MOV" + "forwardleft");
                nwStream.Write(bytes, 0, bytes.Length);
            }
        }

        partial void ForwardRight(UIButton sender)
        {
            modeLabel.Text = "NominalMode";
            if (bconnected)
            {
                byte[] bytes = Encoding.ASCII.GetBytes("MOV" + "forwardright");
                nwStream.Write(bytes, 0, bytes.Length);
            }
        }


        public override void ViewDidLoad()
        {
            base.ViewDidLoad();
            // Perform any additional setup after loading the view, typically from a nib.
        }

       

        public override void DidReceiveMemoryWarning()
        {
            base.DidReceiveMemoryWarning();
            // Release any cached data, images, etc that aren't in use.
        }
    }
}
