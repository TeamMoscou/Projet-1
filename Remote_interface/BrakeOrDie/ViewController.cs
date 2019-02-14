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
        //if bmodeNominal true the car is in nominal mode
        bool bmodeNominal; 

        protected ViewController(IntPtr handle) : base(handle)
        {
            // Note: this .ctor should not contain any initialization logic.
        }

        /*******************************************connect socket***********************************************************/
        //Connect to socket with the IP address given in the feald. 
        partial void StartButtonPushed(UIButton sender)
        {

            try
            {
                //Connect the socket to the server
                clientSocket.Connect(getIPAddress.Text, 6666);
                bconnected = true;
                bmodeNominal = true;
                connectLabel.Text = "Connected";
                nwStream = clientSocket.GetStream();
                Receive();
            }
            catch (SocketException ex)
            {
                connectLabel.Text = "Failed to connect";
                Console.WriteLine(ex.Message);
            }
        }

        /*******************************************change mode label***********************************************************/
        //Functon to change the mode label on the interface
        private void ChangeModeLabel(){
            if (bmodeNominal == true){
                modeLabel.Text = "Nominal Mode";
            } else {
                modeLabel.Text = "Autonomous mode";
            }
        }

        /*******************************************receive from backend***********************************************************/
        //Receive via socket information about potential obstacles 
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
                            ObstacleInfront();
                            break;
                        case "OIB":
                            ObstacleInBack(); 
                            break;
                        case "OBB":
                            ObstacleDetected();
                            break;
                        case "NOD":
                            NoObstacleDetected();
                            break;
                        default:
                            cmpt = (cmpt + 1) % 100;
                            break;
                    }

                }

            }
        }

        //If an obstecle is detected in the back, change to colors on the arrows 
        private void ObstacleInBack(){
            modeLabel.Text = "Obstacle in back";
            downButton.TintColor = UIColor.Gray;
            backwardLeft.TintColor = UIColor.Gray;
            backwardRight.TintColor = UIColor.Gray;
            upButton.TintColor = new UIColor(red: 0.04f, green: 0.38f, blue: 1.00f, alpha: 1.0f);
            forwardLeft.TintColor = new UIColor(red: 0.35f, green: 0.78f, blue: 1.00f, alpha: 1.0f);
            forwardRight.TintColor = new UIColor(red: 0.35f, green: 0.78f, blue: 1.00f, alpha: 1.0f);
        }

        //If an obstecle is detected in the front, change to colors on the arrows 
        private void ObstacleInfront(){
            modeLabel.Text = "Obstacle in front";
            upButton.TintColor = UIColor.Gray;
            forwardLeft.TintColor = UIColor.Gray;
            forwardRight.TintColor = UIColor.Gray;
            downButton.TintColor = new UIColor(red: 0.04f, green: 0.38f, blue: 1.00f, alpha: 1.0f);
            backwardLeft.TintColor = new UIColor(red: 0.35f, green: 0.78f, blue: 1.00f, alpha: 1.0f);
            backwardRight.TintColor = new UIColor(red: 0.35f, green: 0.78f, blue: 1.00f, alpha: 1.0f);
        }

        //If an obstecle is detected in the front and back, change to colors on the arrows 
        private void ObstacleDetected()
        {
            modeLabel.Text = "Obstacle both";
            downButton.TintColor = UIColor.Gray;
            backwardLeft.TintColor = UIColor.Gray;
            backwardRight.TintColor = UIColor.Gray;
            upButton.TintColor = UIColor.Gray;
            forwardLeft.TintColor = UIColor.Gray;
            forwardRight.TintColor = UIColor.Gray;
        }

        //If no is detected in the back, change back the colors and change the mode label back to the original mode.  
        private void NoObstacleDetected(){
            ChangeModeLabel(); //Change the mode label to the previous modelabel 

            upButton.TintColor = new UIColor(red: 0.04f, green: 0.38f, blue: 1.00f, alpha: 1.0f);
            forwardLeft.TintColor = new UIColor(red: 0.35f, green: 0.78f, blue: 1.00f, alpha: 1.0f);
            forwardRight.TintColor = new UIColor(red: 0.35f, green: 0.78f, blue: 1.00f, alpha: 1.0f);
            downButton.TintColor = new UIColor(red: 0.04f, green: 0.38f, blue: 1.00f, alpha: 1.0f);
            backwardLeft.TintColor = new UIColor(red: 0.35f, green: 0.78f, blue: 1.00f, alpha: 1.0f);
            backwardRight.TintColor = new UIColor(red: 0.35f, green: 0.78f, blue: 1.00f, alpha: 1.0f);
        } 


        /*******************************************Send to backend***********************************************************/

        partial void StopWheelButtonPushed(UIButton sender)
        {
            bmodeNominal = true;
            //send command via socket to the backend that is communicating with the car 
            if (bconnected)
            {
                byte[] bytes = Encoding.ASCII.GetBytes("MOV" + "stop");
                nwStream.Write(bytes, 0, bytes.Length);
            }

        }

        partial void RightButtonPushed(UIButton sender)
        {
            bmodeNominal = true;
            //send command via socket to the backend that is communicating with the car 
            if (bconnected)
            {
                byte[] bytes = Encoding.ASCII.GetBytes("STE" + "right");
                nwStream.Write(bytes, 0, bytes.Length);
            }
        }

        partial void LeftButtonPushed(UIButton sender)
        {
            bmodeNominal = true;
            //send command via socket to the backend that is communicating with the car 
            if (bconnected)
            {
                byte[] bytes = Encoding.ASCII.GetBytes("STE" + "left");
                nwStream.Write(bytes, 0, bytes.Length);
            }
        }

        partial void AutonomousButtonClicked(UIButton sender)
        {
            bmodeNominal = false;
            ChangeModeLabel();
            //send command via socket to the backend that is communicating with the car 
            if (bconnected)
            {
                byte[] bytes = Encoding.ASCII.GetBytes("AUT");
                nwStream.Write(bytes, 0, bytes.Length);
            }
        }


        partial void UpButtonPushed(UIButton sender)
        {
            bmodeNominal = true;
            //send command via socket to the backend that is communicating with the car 
            if (bconnected)
            {
                byte[] bytes = Encoding.ASCII.GetBytes("MOV" + "forward");
                nwStream.Write(bytes, 0, bytes.Length);
            }
        }

        partial void DownButtonPushed(UIButton sender)
        {
            bmodeNominal = true;
            //send command via socket to the backend that is communicating with the car 
            if (bconnected)
            {
                byte[] bytes = Encoding.ASCII.GetBytes("MOV" + "backward");
                nwStream.Write(bytes, 0, bytes.Length);
            }
        }

        partial void BackwardRight(UIButton sender)
        {
            bmodeNominal = true;
            //send command via socket to the backend that is communicating with the car 
            if (bconnected)
            {
                byte[] bytes = Encoding.ASCII.GetBytes("MOV" + "backwardright");
                nwStream.Write(bytes, 0, bytes.Length);
            }
        }

        partial void BackwardLeft(UIButton sender)
        {
            bmodeNominal = true;
            //send command via socket to the backend that is communicating with the car 
            if (bconnected)
            {
                byte[] bytes = Encoding.ASCII.GetBytes("MOV" + "backwardleft");
                nwStream.Write(bytes, 0, bytes.Length);
            }
        }

        partial void ForwardLeft(UIButton sender)
        {
            bmodeNominal = true;
            //send command via socket to the backend that is communicating with the car 
            if (bconnected)
            {
                byte[] bytes = Encoding.ASCII.GetBytes("MOV" + "forwardleft");
                nwStream.Write(bytes, 0, bytes.Length);
            }
        }

        partial void ForwardRight(UIButton sender)
        {
            bmodeNominal = true;
            //send command via socket to the backend that is communicating with the car 
            if (bconnected)
            {
                byte[] bytes = Encoding.ASCII.GetBytes("MOV" + "forwardright");
                nwStream.Write(bytes, 0, bytes.Length);
            }
        }

        /************************************************************************************************************************/
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
