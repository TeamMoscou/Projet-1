# coding: utf-8
import threading

class Can_send(threading.Thread):
    def __init__(self, bus):
        threading.Thread.__init__(self)
        self.bus = bus

    def run(self):
        self.speed_cmd = 0
        self.move = 0
        self.turn = 0
        self.enable = 0

        while True:
            self.speed_cmd = 60
            print("speed is fixed to ", self.speed_cmd)
            if (DATA_OUT.Message == FORWARD):
                self.move = 1
                self.turn = 0
                self.enable = 1
                print("send cmd move forward")
            elif (DATA_OUT.Message == FORWARD_LEFT):
                self.move = 1
                self.turn = -1
                self.enable = 1
                print("send cmd move forward_left")
            elif (DATA_OUT.Message == FORWARD_RIGHT):
                self.move = 1
                self.turn = 1
                self.enable = 1
                print("send cmd move forward_right")
            elif (DATA_OUT.Message == BACKWARD):
                self.move = -1
                self.turn = 0
                self.enable = 1
                print("send cmd move backward")
            elif (DATA_OUT.Message == BACKWARD_LEFT):
                self.move = -1
                self.turn = -1
                self.enable = 1
                print("send cmd move backward_left")
            elif (DATA_OUT.Message == BACKWARD_RIGHT):
                self.move = -1
                self.turn = 1
                self.enable = 1
                print("send cmd move backward_right")
            elif (DATA_OUT.Message == LEFT):
                self.move = 0
                self.turn = -1
                self.enable = 1
                print("send cmd turn left")
            elif (DATA_OUT.Message == RIGHT):
                self.move = 0
                self.turn = 1
                self.enable = 1
                print("send cmd turn right")
            elif (DATA_OUT.Message == STOP):
                self.move = 0
                self.turn = 0
                self.enable = 0
                print("send cmd move stop")

            print("Move: ", self.move)
            print("Turn: ", self.turn)
            print("Enable: ", self.enable)

            if self.enable:
                cmd_mv = (50 + self.move * self.speed_cmd) | 0x80
                cmd_turn = 50 + self.turn * 20 | 0x80
            else:
                cmd_mv = (50 + self.move * self.speed_cmd) & ~0x80
                cmd_turn = 50 + self.turn * 20 & 0x80

            print("mv:", cmd_mv, "turn:", cmd_turn)

            msg = can.Message(arbitration_id=MCM, data=[cmd_mv, cmd_mv, cmd_turn, 0, 0, 0, 0, 0], extended_id=False)

            # msg = can.Message(arbitration_id=0x010,data=[0xBC,0xBC,0x00, 0x00, 0x00, 0x00,0x00, 0x00],extended_id=False)
            # msg = can.Message(arbitration_id=MCM,data=[0xBC,0xBC,0x00, 0x00, 0x00, 0x00,0x00, 0x00],extended_id=False)
            print(msg)
            self.bus.send(msg)

