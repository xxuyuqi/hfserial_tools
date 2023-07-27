from atexit import register
from os.path import dirname, join
import serial
import serial.tools.list_ports
import threading
import time

class MySerial(serial.Serial):
    def __new__(cls, bps=115200, timeout=3):
        cls.print_serial()
        return super(MySerial,cls).__new__(cls)


    def __init__(self, bps=115200, timeout=3) -> None:
        register(self.del_func)
        portx = input("需要打开的串口：")
        super().__init__(portx, baudrate=bps, timeout=timeout)
        if self.isOpen():                                           # 判断串口是否成功打开
            print("打开串口成功。")
            print(self.name)                                        # 输出串口号          
        else:
            raise Exception("打开串口失败")
        try:
            with open("mpy.ini", 'r') as f:
                self.data_ix = int(f.read())
        except:
            self.data_ix = 0
        self.runningflag = True

    @classmethod
    def print_serial(cls):
        ports_list = list(serial.tools.list_ports.comports())
        if len(ports_list) <= 0:
            raise Exception("No port")
        else:
            print("可用的串口设备如下：")
            for comport in ports_list:
                print(list(comport)[0], list(comport)[1])
     
    def Send_data(self):
          keyword = input("请输入需要测试的命令:(q退出)")
          if keyword == "q" or keyword == "Q":
               self.runningflag = False
               try:
                    self.t1.join()
               except:
                    pass
          else:
               keyword += '\r\n'
               self.write(keyword.encode())

    def Data(self):
        file_path = rf"D:\feihuang\log\data{self.data_ix}.txt"
        self.data_ix += 1
        print('输出'+self.name + '串口信息')
        self.file = open(file_path, "w")
        while self.runningflag:               
            if self.in_waiting > 0:
                data = self.readline().decode().strip()
                print(data)
                print('正在写入中')
                self.file.write(data.encode("utf-8").decode('utf-8')+'\n')
                self.file.flush()

    def run_process(self):
        self.Send_data()
        self.t1 = threading.Thread(target=self.Data)
        self.t1.start()
        while self.runningflag:
            time.sleep(10)
            self.Send_data()
        
    
    def del_func(self) -> None:
        with open("mpy.ini", 'w') as f:
            f.write(f"{self.data_ix}")                              # 可以有更好的方法保存参数，包括扫描文件夹的文件数，然后设置ix
        self.file.close()
         

if __name__ == '__main__':
    ser = MySerial()
    ser.run_process()