import subprocess
import threading
import queue
import time

class script_interface:
    def __init__(self, command="") -> None:
        self.proc = subprocess.Popen(command, 
            stdin=subprocess.PIPE, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            shell=True)
        self.q = queue.Queue()
        self.output_handle = threading.Thread(target=self.__scan_output, args=(self.proc.stdout, self.q))
        self.output_handle.daemon = True
        self.output_handle.start()

    def __scan_output(self, output, queue) -> None:
        for line in iter(output.readline, b''):
            queue.put(line)
        output.close()
    
    def write(self, command) -> None:
        self.proc.stdin.write((command +"\n").encode('utf-8'))
        self.proc.stdin.flush()

    def read(self) -> str:
        # yeild for a little so the other thread can execute
        time.sleep(0.00000000001)
        # get the output
        output = b"nothing found yet"
        try:
            output = self.q.get_nowait()
        except:
            pass
        return output.decode("utf-8")

    def get_response(self, timeout=10) -> str:
        starttime = time.time()
        while time.time() - starttime < timeout:
            try:
                output = self.q.get_nowait()
                time.sleep(0.000000001)
                return output.decode("utf-8")
            except:
                pass
        return "nothing was recieved"

    def yeild_to(self, time=0.00000000001) -> None:
        time.sleep(time)

    def close(self) -> None:
        self.yeild_to(0.0001)
        self.proc.stderr.close()
        self.proc.stdin.close()
        self.proc.stdout.close()
        self.proc.terminate()

    def __get_queue_length(self) -> int:
        return self.q.qsize()

    def clear(self) -> None:
        with self.q.mutex:
            self.q.queue.clear()