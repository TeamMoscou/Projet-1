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
                //Send initial speed value
                byte[] bytes = Encoding.ASCII.GetBytes("SPE" + getSpeed.Text);
                nwStream.Write(bytes, 0, bytes.Length);

            }
            catch (SocketException ex)
            {
                connectLabel.Text = "Failed to connect";
                Console.WriteLine(ex.Message);
            }
        }


        partial void SetSpeedToCar(UIButton sender)
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

        }

        /*partial void StopSteeringButtonPushed(UIButton sender)
        {
            modeLabel.Text = "NominalMode";
            if (bconnected)
            {
                byte[] bytes = Encoding.ASCII.GetBytes("STE" + "stop");
                nwStream.Write(bytes, 0, bytes.Length);
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
